from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Any, Generic, Iterable, TypeVar

import numpy as np

T = TypeVar("T")


class Localization(str, Enum):
    HIGGS = "higgs"
    ANDERSON = "anderson"
    AUBRY_ANDRE = "aubry_andre"
    MOTT = "mott"
    MODE_LOCK = "mode_lock"
    OTHER = "other"


@dataclass(frozen=True)
class QUNO(Generic[T]):
    """Plural typed carrier: alternatives coexist without quotienting identity."""

    values: tuple[T, ...]

    @classmethod
    def of(cls, *values: T) -> "QUNO[T]":
        if not values:
            raise ValueError("QUNO needs at least one value")
        return cls(tuple(values))


@dataclass(frozen=True)
class SIGILITAS(Generic[T]):
    """Toy semantic kernel wrapper used by the course.

    This is an abstract teaching schema, not a claim that all physical theories
    are literally instances of one physical model.
    """

    syntax: T
    semantics: Any
    provenance: tuple[str, ...] = ()


@dataclass(frozen=True)
class QUAZRIS(Generic[T]):
    """Typed dual/proxy view of a primal object."""

    primal: SIGILITAS[T]
    dual_syntax: Any
    dual_semantics: Any
    witness: str


@dataclass(frozen=True)
class ExchangeWitness:
    before_syntax: Any
    before_semantics: Any
    after_syntax: Any
    after_semantics: Any
    localization: Localization
    note: str


def exchange_J(
    obj: SIGILITAS[Any],
    *,
    localization: Localization = Localization.OTHER,
    note: str = "",
) -> tuple[SIGILITAS[Any], ExchangeWitness]:
    """Toy syntax/semantics exchange map with an explicit witness.

    The operation is involutive at the level of this data container:
    exchange_J(exchange_J(x)[0])[0] recovers the original pair.
    """
    out = SIGILITAS(
        syntax=obj.semantics,
        semantics=obj.syntax,
        provenance=obj.provenance + ("exchange_J",),
    )
    witness = ExchangeWitness(
        before_syntax=obj.syntax,
        before_semantics=obj.semantics,
        after_syntax=out.syntax,
        after_semantics=out.semantics,
        localization=localization,
        note=note,
    )
    return out, witness


def quazris_twist(
    obj: SIGILITAS[T],
    *,
    dual_syntax: Any,
    dual_semantics: Any,
    witness: str,
) -> QUAZRIS[T]:
    """Inject a primal teaching object into an explicitly witnessed dual view."""
    if not witness:
        raise ValueError("QUAZRIS twist requires a witness")
    return QUAZRIS(
        primal=obj,
        dual_syntax=dual_syntax,
        dual_semantics=dual_semantics,
        witness=witness,
    )


def anderson_hamiltonian(
    onsite: np.ndarray,
    hopping: float = 1.0,
    periodic: bool = False,
) -> np.ndarray:
    """1D tight-binding Anderson Hamiltonian with user-supplied onsite disorder."""
    e = np.asarray(onsite, dtype=float)
    n = e.size
    H = np.diag(e.astype(complex))
    for i in range(n - 1):
        H[i, i + 1] = H[i + 1, i] = -hopping
    if periodic and n > 2:
        H[0, -1] = H[-1, 0] = -hopping
    return H


def aubry_andre_hamiltonian(
    n: int,
    *,
    J: float = 1.0,
    lam: float = 2.0,
    beta: float = (1.0 + np.sqrt(5.0)) / 2.0,
    phi: float = 0.0,
    periodic: bool = False,
) -> np.ndarray:
    """Finite Aubry-André tight-binding Hamiltonian."""
    sites = np.arange(n)
    onsite = lam * np.cos(2.0 * np.pi * beta * sites + phi)
    return anderson_hamiltonian(onsite, hopping=J, periodic=periodic)


def inverse_participation_ratio(state: np.ndarray) -> float:
    psi = np.asarray(state, dtype=complex)
    norm = np.vdot(psi, psi).real
    if norm <= 0:
        raise ValueError("state norm must be positive")
    p = np.abs(psi) ** 2 / norm
    return float(np.sum(p**2))


def circle_map_step(theta: float, omega: float, K: float) -> float:
    return float((theta + omega + (K / (2.0 * np.pi)) * np.sin(2.0 * np.pi * theta)) % 1.0)


def circle_map_orbit(
    theta0: float,
    omega: float,
    K: float,
    steps: int = 1000,
) -> np.ndarray:
    theta = float(theta0 % 1.0)
    orbit = np.empty(steps + 1, dtype=float)
    orbit[0] = theta
    for i in range(steps):
        theta = circle_map_step(theta, omega, K)
        orbit[i + 1] = theta
    return orbit


def circle_rotation_number(
    theta0: float,
    omega: float,
    K: float,
    steps: int = 5000,
    burn_in: int = 500,
) -> float:
    """Estimate the rotation number using the lifted (not mod-1) map."""
    theta = float(theta0)
    start = None
    start_step = None
    for i in range(steps + burn_in):
        theta = theta + omega + (K / (2.0 * np.pi)) * np.sin(2.0 * np.pi * theta)
        if i == burn_in - 1:
            start = theta
            start_step = i
    assert start is not None and start_step is not None
    return float((theta - start) / max(1, steps))


def kuramoto_rhs(theta: np.ndarray, omega: np.ndarray, coupling: float) -> np.ndarray:
    """All-to-all Kuramoto phase dynamics."""
    th = np.asarray(theta, dtype=float)
    om = np.asarray(omega, dtype=float)
    if th.shape != om.shape:
        raise ValueError("theta and omega must have the same shape")
    phase_diff = th[None, :] - th[:, None]
    return om + coupling * np.mean(np.sin(phase_diff), axis=1)


def kuramoto_order_parameter(theta: np.ndarray) -> complex:
    th = np.asarray(theta, dtype=float)
    return complex(np.mean(np.exp(1j * th)))


def bose_hubbard_site_term(n_occ: int, U: float, mu: float) -> float:
    """Single-site diagonal Bose-Hubbard energy contribution."""
    return float(0.5 * U * n_occ * (n_occ - 1) - mu * n_occ)


def jch_local_block(
    n_excitation: int,
    *,
    omega_c: float = 1.0,
    omega_a: float = 1.0,
    eta: float = 0.1,
) -> np.ndarray:
    """Two-state Jaynes-Cummings block for fixed total excitation n>=1.

    Basis: |n,g>, |n-1,e>. This is a local block, not the full JCH lattice.
    """
    n = int(n_excitation)
    if n < 1:
        raise ValueError("n_excitation must be >= 1")
    return np.array(
        [
            [n * omega_c, eta * np.sqrt(n)],
            [eta * np.sqrt(n), (n - 1) * omega_c + omega_a],
        ],
        dtype=float,
    )


def localization_bundle() -> QUNO[Localization]:
    """Plural localization vocabulary preserved as distinct tagged mechanisms."""
    return QUNO.of(
        Localization.HIGGS,
        Localization.ANDERSON,
        Localization.AUBRY_ANDRE,
        Localization.MOTT,
        Localization.MODE_LOCK,
        Localization.OTHER,
    )


def self_dual_closed_subtheory_example() -> dict[str, Any]:
    """Minimal toy witness for a closed self-dual SIGIL teaching object."""
    primal = SIGILITAS(
        syntax="onsite <-> hopping chart",
        semantics={"model": "Aubry-André", "critical_ratio": "lambda/J = 2"},
        provenance=("course-codebook",),
    )
    dual = quazris_twist(
        primal,
        dual_syntax="momentum <-> position chart",
        dual_semantics={"self_dual_surface": "lambda = 2 J"},
        witness="Fourier exchange of hopping and quasiperiodic potential scales",
    )
    return {
        "primal": primal,
        "dual": dual,
        "closed_under_named_duality": True,
        "claim_scope": "toy course schema / Aubry-André duality example",
    }
