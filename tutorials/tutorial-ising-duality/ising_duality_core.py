from __future__ import annotations

from dataclasses import dataclass
from itertools import product
from typing import Iterable

import numpy as np

GENUS2_BASIS = ("a1", "b1", "a2", "b2")


def onsager_critical_temperature(J: float = 1.0, k_B: float = 1.0) -> float:
    """Critical temperature of the infinite square-lattice 2D Ising model at zero field."""
    if J <= 0 or k_B <= 0:
        raise ValueError("J and k_B must be positive")
    return 2.0 * J / (k_B * np.log(1.0 + np.sqrt(2.0)))


def kramers_wannier_dual_coupling(K: float) -> float:
    """Return K* defined by sinh(2K) sinh(2K*) = 1 for K > 0."""
    if K <= 0:
        raise ValueError("K must be positive")
    return 0.5 * np.arcsinh(1.0 / np.sinh(2.0 * K))


def montonen_olive_s_transform(tau: complex) -> complex:
    """Pedagogical S-duality map tau -> -1/tau; not a simulation of N=4 SYM."""
    if tau == 0:
        raise ValueError("tau must be non-zero")
    return -1.0 / tau


@dataclass
class Ising2D:
    n: int = 16
    J: float = 1.0
    beta: float = 0.4
    seed: int = 42

    def __post_init__(self) -> None:
        if self.n < 2:
            raise ValueError("n must be at least 2")
        if self.J <= 0 or self.beta <= 0:
            raise ValueError("J and beta must be positive")
        self.rng = np.random.default_rng(self.seed)
        self.spins = self.rng.choice((-1, 1), size=(self.n, self.n)).astype(np.int8)

    def energy(self) -> float:
        s = self.spins
        bonds = s * (np.roll(s, -1, axis=0) + np.roll(s, -1, axis=1))
        return float(-self.J * bonds.sum())

    def magnetization(self) -> float:
        return float(self.spins.mean())

    def delta_energy_flip(self, i: int, j: int) -> float:
        s = self.spins
        nn = (
            s[(i + 1) % self.n, j]
            + s[(i - 1) % self.n, j]
            + s[i, (j + 1) % self.n]
            + s[i, (j - 1) % self.n]
        )
        return float(2.0 * self.J * s[i, j] * nn)

    def metropolis_sweep(self) -> int:
        accepted = 0
        for _ in range(self.n * self.n):
            i, j = self.rng.integers(0, self.n, size=2)
            dE = self.delta_energy_flip(int(i), int(j))
            if dE <= 0.0 or self.rng.random() < np.exp(-self.beta * dE):
                self.spins[i, j] *= -1
                accepted += 1
        return accepted

    def sample(self, burn_in: int = 100, sweeps: int = 200, thin: int = 5) -> dict[str, np.ndarray]:
        if burn_in < 0 or sweeps <= 0 or thin <= 0:
            raise ValueError("invalid sampling parameters")
        for _ in range(burn_in):
            self.metropolis_sweep()
        energies: list[float] = []
        mags: list[float] = []
        accepts: list[float] = []
        for step in range(sweeps):
            accepted = self.metropolis_sweep()
            if step % thin == 0:
                energies.append(self.energy() / (self.n * self.n))
                mags.append(self.magnetization())
                accepts.append(accepted / (self.n * self.n))
        return {
            "energy_per_spin": np.asarray(energies),
            "magnetization": np.asarray(mags),
            "acceptance": np.asarray(accepts),
        }


def hebbian_weights(patterns: np.ndarray) -> np.ndarray:
    """Hopfield Hebbian matrix with zero diagonal."""
    p = np.asarray(patterns, dtype=float)
    if p.ndim != 2:
        raise ValueError("patterns must have shape (n_patterns, n_neurons)")
    if not np.all(np.isin(p, (-1.0, 1.0))):
        raise ValueError("patterns must contain only -1/+1")
    n = p.shape[1]
    W = (p.T @ p) / n
    np.fill_diagonal(W, 0.0)
    return W


def hopfield_energy(state: np.ndarray, W: np.ndarray) -> float:
    s = np.asarray(state, dtype=float)
    return float(-0.5 * s @ W @ s)


def hopfield_async_update(
    state: np.ndarray, W: np.ndarray, *, seed: int = 42, sweeps: int = 1
) -> np.ndarray:
    s = np.asarray(state, dtype=float).copy()
    if W.shape != (s.size, s.size):
        raise ValueError("W shape does not match state")
    rng = np.random.default_rng(seed)
    for _ in range(sweeps):
        for i in rng.permutation(s.size):
            field = float(W[i] @ s)
            if field > 0:
                s[i] = 1.0
            elif field < 0:
                s[i] = -1.0
    return s.astype(np.int8)


I2 = np.eye(2, dtype=complex)
X = np.array([[0, 1], [1, 0]], dtype=complex)
Z = np.array([[1, 0], [0, -1]], dtype=complex)


def _operator_on_sites(n: int, mapping: dict[int, np.ndarray]) -> np.ndarray:
    op = np.array([[1.0 + 0.0j]])
    for site in range(n):
        op = np.kron(op, mapping.get(site, I2))
    return op


def tfim_hamiltonian(n: int, J: float = 1.0, h: float = 1.0, periodic: bool = True) -> np.ndarray:
    """Small transverse-field Ising Hamiltonian for exact diagonalization."""
    if n < 2:
        raise ValueError("n must be at least 2")
    dim = 2**n
    H = np.zeros((dim, dim), dtype=complex)
    last_bond = n if periodic else n - 1
    for i in range(last_bond):
        j = (i + 1) % n
        H -= J * _operator_on_sites(n, {i: Z, j: Z})
    for i in range(n):
        H -= h * _operator_on_sites(n, {i: X})
    return H


def tfim_ground_state_observables(
    n: int = 6, J: float = 1.0, h: float = 1.0, periodic: bool = True
) -> dict[str, float]:
    H = tfim_hamiltonian(n=n, J=J, h=h, periodic=periodic)
    vals, vecs = np.linalg.eigh(H)
    psi = vecs[:, 0]

    def expect(op: np.ndarray) -> float:
        return float(np.real(np.vdot(psi, op @ psi)))

    zz = np.mean(
        [
            expect(_operator_on_sites(n, {i: Z, (i + 1) % n: Z}))
            for i in range(n if periodic else n - 1)
        ]
    )
    xmag = np.mean([expect(_operator_on_sites(n, {i: X})) for i in range(n)])
    gap = float(vals[1] - vals[0])
    return {
        "ground_energy_per_spin": float(vals[0] / n),
        "gap": gap,
        "mean_zz": float(zz),
        "mean_x": float(xmag),
    }


def genus2_zero_two_sectors() -> list[tuple[int, int, int, int]]:
    """H_1(Sigma_2, Z_2) represented as four Z2 bits."""
    return list(product((0, 1), repeat=4))


def logical_loop_update(
    sector: Iterable[int], cycle: str
) -> tuple[int, int, int, int]:
    """Toggle one Z2 homology coordinate.

    This is a sector bookkeeping operation. Energy-neutrality is model-dependent
    and must not be assumed for a generic Ising Hamiltonian.
    """
    bits = [int(x) & 1 for x in sector]
    if len(bits) != 4:
        raise ValueError("a genus-2 Z2 sector needs four bits")
    try:
        idx = GENUS2_BASIS.index(cycle)
    except ValueError as exc:
        raise ValueError(f"cycle must be one of {GENUS2_BASIS}") from exc
    bits[idx] ^= 1
    return tuple(bits)


def contextual_features(
    *,
    temperature: float,
    energy_per_spin: float,
    magnetization: float,
    dual_coupling: float,
    sector: Iterable[int] = (0, 0, 0, 0),
) -> np.ndarray:
    sector_bits = np.asarray(list(sector), dtype=float)
    if sector_bits.shape != (4,):
        raise ValueError("sector must have four components")
    return np.concatenate(
        [
            np.asarray(
                [temperature, energy_per_spin, abs(magnetization), dual_coupling],
                dtype=float,
            ),
            sector_bits,
        ]
    )


def contextual_kernel(X: np.ndarray, gamma: float = 1.0) -> np.ndarray:
    """RBF Gram matrix on standardized contextual feature vectors."""
    A = np.asarray(X, dtype=float)
    if A.ndim != 2:
        raise ValueError("X must be a 2D feature matrix")
    scale = A.std(axis=0)
    scale[scale == 0] = 1.0
    Zs = (A - A.mean(axis=0)) / scale
    sq = np.sum((Zs[:, None, :] - Zs[None, :, :]) ** 2, axis=-1)
    return np.exp(-gamma * sq / max(1, A.shape[1]))


def assert_psd(K: np.ndarray, atol: float = 1e-10) -> np.ndarray:
    eig = np.linalg.eigvalsh(np.asarray(K, dtype=float))
    if eig.min() < -atol:
        raise AssertionError(f"kernel is not PSD: min eigenvalue={eig.min()}")
    return eig
