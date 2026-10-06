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


class SwarmalatorState(str, Enum):
    STATIC_SYNC = "static_sync"
    STATIC_ASYNC = "static_async"
    STATIC_PHASE_WAVE = "static_phase_wave"
    SPLINTERED_PHASE_WAVE = "splintered_phase_wave"
    ACTIVE_PHASE_WAVE = "active_phase_wave"
    ASYNC_1D = "async_1d"
    PHASE_WAVE_1D = "phase_wave_1d"
    MIXED_1D = "mixed_1d"
    SYNC_1D = "sync_1d"


@dataclass(frozen=True)
class JaranianJauria:
    """Primitive swarmalator carrier with coupled spatial and phase degrees of freedom."""

    position: np.ndarray
    phase: np.ndarray
    J: float
    K: float
    provenance: tuple[str, ...] = ("O'Keeffe-Hong-Strogatz-2017",)

    def __post_init__(self) -> None:
        x = np.asarray(self.position, dtype=float)
        th = np.asarray(self.phase, dtype=float)
        if x.ndim != 2 or x.shape[1] != 2:
            raise ValueError("position must have shape (N, 2)")
        if th.shape != (x.shape[0],):
            raise ValueError("phase must have shape (N,)")
        object.__setattr__(self, "position", x)
        object.__setattr__(self, "phase", th)


def swarmalator_2d_rhs(
    position: np.ndarray,
    phase: np.ndarray,
    *,
    J: float = 1.0,
    K: float = 0.0,
    eps: float = 1e-9,
) -> tuple[np.ndarray, np.ndarray]:
    """Canonical 2D swarmalator flow used in the codebook.

    dx_i/dt = mean_j [ r_ji/|r_ji| * (1 + J cos(theta_j-theta_i))
                       - r_ji/|r_ji|^2 ]
    dtheta_i/dt = K * mean_j [ sin(theta_j-theta_i) / |r_ji| ]

    Self terms are excluded. This is the standard pedagogical form of the
    O'Keeffe-Hong-Strogatz model; variants use other attraction/repulsion
    kernels.
    """
    x = np.asarray(position, dtype=float)
    th = np.asarray(phase, dtype=float)
    if x.ndim != 2 or x.shape[1] != 2 or th.shape != (x.shape[0],):
        raise ValueError("expected position (N,2) and phase (N,)")
    n = x.shape[0]
    dx = np.zeros_like(x)
    dth = np.zeros_like(th)
    for i in range(n):
        r = x - x[i]
        dist = np.linalg.norm(r, axis=1)
        mask = np.arange(n) != i
        rr = r[mask]
        dd = np.maximum(dist[mask], eps)
        dphi = th[mask] - th[i]
        attraction = rr / dd[:, None] * (1.0 + J * np.cos(dphi))[:, None]
        repulsion = rr / (dd[:, None] ** 2)
        dx[i] = np.mean(attraction - repulsion, axis=0)
        dth[i] = K * np.mean(np.sin(dphi) / dd)
    return dx, dth


def swarmalator_1d_rhs(
    position_angle: np.ndarray,
    phase: np.ndarray,
    *,
    nu: np.ndarray | None = None,
    omega: np.ndarray | None = None,
    J: float = 1.0,
    K: float = 1.0,
) -> tuple[np.ndarray, np.ndarray]:
    """1D ring swarmalator model.

    xdot_i = nu_i + J/N sum_j sin(x_j-x_i) cos(theta_j-theta_i)
    thdot_i = omega_i + K/N sum_j sin(theta_j-theta_i) cos(x_j-x_i)
    """
    x = np.asarray(position_angle, dtype=float)
    th = np.asarray(phase, dtype=float)
    if x.shape != th.shape:
        raise ValueError("position_angle and phase must have the same shape")
    n = x.size
    nu_arr = np.zeros(n) if nu is None else np.asarray(nu, dtype=float)
    om_arr = np.zeros(n) if omega is None else np.asarray(omega, dtype=float)
    if nu_arr.shape != x.shape or om_arr.shape != x.shape:
        raise ValueError("natural-frequency arrays must match position shape")
    dx = np.empty(n, dtype=float)
    dth = np.empty(n, dtype=float)
    for i in range(n):
        dx_i = x - x[i]
        dphi = th - th[i]
        dx[i] = nu_arr[i] + J * np.mean(np.sin(dx_i) * np.cos(dphi))
        dth[i] = om_arr[i] + K * np.mean(np.sin(dphi) * np.cos(dx_i))
    return dx, dth


def swarmalator_sum_difference(
    position_angle: np.ndarray,
    phase: np.ndarray,
) -> tuple[np.ndarray, np.ndarray]:
    """Return xi=x+theta and eta=x-theta coordinates on the ring."""
    x = np.asarray(position_angle, dtype=float)
    th = np.asarray(phase, dtype=float)
    if x.shape != th.shape:
        raise ValueError("position_angle and phase must have the same shape")
    return x + th, x - th


def swarmalator_coupled_kuramoto_rhs(
    xi: np.ndarray,
    eta: np.ndarray,
    *,
    nu: np.ndarray | None = None,
    omega: np.ndarray | None = None,
    J: float = 1.0,
    K: float = 1.0,
) -> tuple[np.ndarray, np.ndarray]:
    """Equivalent sum/difference-coordinate form of the 1D model."""
    xi = np.asarray(xi, dtype=float)
    eta = np.asarray(eta, dtype=float)
    if xi.shape != eta.shape:
        raise ValueError("xi and eta must have the same shape")
    n = xi.size
    nu_arr = np.zeros(n) if nu is None else np.asarray(nu, dtype=float)
    om_arr = np.zeros(n) if omega is None else np.asarray(omega, dtype=float)
    a = 0.5 * (J + K)
    b = 0.5 * (J - K)
    dxi = np.empty(n, dtype=float)
    deta = np.empty(n, dtype=float)
    for i in range(n):
        sx = np.mean(np.sin(xi - xi[i]))
        se = np.mean(np.sin(eta - eta[i]))
        dxi[i] = nu_arr[i] + om_arr[i] + a * sx + b * se
        deta[i] = nu_arr[i] - om_arr[i] + b * sx + a * se
    return dxi, deta


def rainbow_order_parameters(
    position_angle: np.ndarray,
    phase: np.ndarray,
) -> tuple[complex, complex]:
    """W_+ and W_- = <exp(i(x +/- theta))> for 1D swarmalators."""
    xi, eta = swarmalator_sum_difference(position_angle, phase)
    return complex(np.mean(np.exp(1j * xi))), complex(np.mean(np.exp(1j * eta)))


def swarmalator_order_summary(
    position_angle: np.ndarray,
    phase: np.ndarray,
) -> dict[str, float]:
    """Global phase coherence plus the two rainbow amplitudes."""
    R = abs(kuramoto_order_parameter(np.asarray(phase, dtype=float)))
    wp, wm = rainbow_order_parameters(position_angle, phase)
    return {"R_phase": float(R), "S_plus": float(abs(wp)), "S_minus": float(abs(wm))}


SWARMALATOR_OPEN_PUZZLES = (
    "melting point from static async to active phase wave",
    "splitting point from active to splintered phase wave",
    "analytic supercritical rainbow-order branches",
    "cluster-count selection in the splintered phase wave",
)
