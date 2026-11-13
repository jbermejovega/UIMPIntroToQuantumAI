from __future__ import annotations

from dataclasses import dataclass, field
from enum import StrEnum
from hashlib import sha256
import json
from typing import Any, Iterable


SCHEMA_ID = "PACA_CCMS_KUIR_QUAZRIS_SOURCE_BINDING_V1"


class BindOp(StrEnum):
    BIND = "BIND"
    DEBIND = "DEBIND"
    REBIND = "REBIND"
    REKONTRA_BIND = "REKONTRA_BIND"


class SemiOp(StrEnum):
    SEMI_FUSION = "SEMI_FUSION"
    SEMI_JOIN = "SEMI_JOIN"
    SEMI_MEET = "SEMI_MEET"
    SEMI_PUSHOUT = "SEMI_PUSHOUT"
    SEMI_PULLBACK = "SEMI_PULLBACK"


@dataclass(frozen=True)
class SourceRef:
    source_id: str
    repository: str
    path: str | None
    role: str
    provenance: tuple[str, ...] = ()


@dataclass(frozen=True)
class BindingWitness:
    operation: BindOp
    left: str
    right: str | None
    result_id: str
    preserves: tuple[str, ...]
    drops: tuple[str, ...]
    note: str
    digest: str


@dataclass(frozen=True)
class BoundSource:
    binding_id: str
    sources: tuple[SourceRef, ...]
    witnesses: tuple[BindingWitness, ...]
    authority_transport: bool = False
    identity_transport: bool = False


@dataclass(frozen=True)
class PrimalDualProjection:
    projection_id: str
    primal: dict[str, Any]
    dual: dict[str, Any]
    kuir_interface: str = "KUIR"
    quazris_external_api: str = "QUAZRIS"
    krone_internal_api: str = "KRONE"


@dataclass(frozen=True)
class LearningTrace:
    observations: tuple[dict[str, Any], ...]
    integrated_state: dict[str, Any]
    learned_state: dict[str, Any]
    reconstruction: dict[str, Any]
    error: float
    exact: bool
    notes: tuple[str, ...] = ()


def _digest(value: Any) -> str:
    payload = json.dumps(value, sort_keys=True, separators=(",", ":"), default=str)
    return "sha256:" + sha256(payload.encode("utf-8")).hexdigest()


def _witness(
    operation: BindOp,
    left: str,
    right: str | None,
    result_id: str,
    *,
    preserves: Iterable[str],
    drops: Iterable[str] = (),
    note: str,
) -> BindingWitness:
    core = {
        "operation": operation,
        "left": left,
        "right": right,
        "result_id": result_id,
        "preserves": tuple(preserves),
        "drops": tuple(drops),
        "note": note,
    }
    return BindingWitness(
        **core,
        digest=_digest(core),
    )


def bind(left: SourceRef, right: SourceRef, *, note: str = "") -> BoundSource:
    result_id = f"BIND::{left.source_id}::{right.source_id}"
    witness = _witness(
        BindOp.BIND,
        left.source_id,
        right.source_id,
        result_id,
        preserves=("provenance", "source_identity", "authority_boundary"),
        note=note or "typed composition; no identity or authority transport",
    )
    return BoundSource(result_id, (left, right), (witness,))


def debind(bound: BoundSource, source_id: str) -> BoundSource:
    kept = tuple(source for source in bound.sources if source.source_id != source_id)
    if len(kept) == len(bound.sources):
        raise ValueError(f"source not present: {source_id}")
    result_id = f"DEBIND::{bound.binding_id}::{source_id}"
    witness = _witness(
        BindOp.DEBIND,
        bound.binding_id,
        source_id,
        result_id,
        preserves=("remaining_provenance", "authority_boundary"),
        drops=("selected_binding_edge",),
        note="removes one composition edge without rewriting source history",
    )
    return BoundSource(result_id, kept, bound.witnesses + (witness,))


def rebind(bound: BoundSource, replacement: SourceRef) -> BoundSource:
    base_ids = {source.source_id for source in bound.sources}
    sources = tuple(source for source in bound.sources if source.source_id != replacement.source_id)
    sources = sources + (replacement,)
    result_id = f"REBIND::{bound.binding_id}::{replacement.source_id}"
    witness = _witness(
        BindOp.REBIND,
        bound.binding_id,
        replacement.source_id,
        result_id,
        preserves=("lineage", "provenance", "authority_boundary"),
        note=(
            "replacement is a fresh witnessed occurrence"
            if replacement.source_id in base_ids
            else "adds a fresh witnessed source occurrence"
        ),
    )
    return BoundSource(result_id, sources, bound.witnesses + (witness,))


def rekontra_bind(bound: BoundSource) -> BoundSource:
    """Create a dual-order binding view without reversing repository history."""
    result_id = f"REKONTRA::{bound.binding_id}"
    witness = _witness(
        BindOp.REKONTRA_BIND,
        bound.binding_id,
        None,
        result_id,
        preserves=("all_source_identities", "all_provenance", "authority_boundary"),
        note="contravariant/dual presentation only; Git history is not rewound",
    )
    return BoundSource(
        result_id,
        tuple(reversed(bound.sources)),
        bound.witnesses + (witness,),
    )


def semi_compose(
    left: BoundSource,
    right: BoundSource,
    *,
    operation: SemiOp = SemiOp.SEMI_FUSION,
    witness_ref: str,
) -> BoundSource:
    if not witness_ref:
        raise ValueError("semi-operation requires a witness")
    unique: dict[str, SourceRef] = {}
    for source in (*left.sources, *right.sources):
        unique[source.source_id] = source
    result_id = f"{operation}::{left.binding_id}::{right.binding_id}"
    witness = _witness(
        BindOp.BIND,
        left.binding_id,
        right.binding_id,
        result_id,
        preserves=("plurality", "provenance", "noncollapse", "witness_ref"),
        note=f"{operation} with witness {witness_ref}; composition != identity merge",
    )
    return BoundSource(
        result_id,
        tuple(unique.values()),
        left.witnesses + right.witnesses + (witness,),
    )


def quazris_project(bound: BoundSource) -> PrimalDualProjection:
    """Project a bound source family through KUIR into primal/dual public views."""
    primal = {
        "route": "forward/public-capability",
        "sources": [source.source_id for source in bound.sources],
        "effects": "declared_only",
    }
    dual = {
        "route": "obstruction/trace",
        "witnesses": [w.digest for w in bound.witnesses],
        "authority_transport": False,
        "identity_transport": False,
    }
    return PrimalDualProjection(
        projection_id=f"QUAZRIS::{bound.binding_id}",
        primal=primal,
        dual=dual,
    )


@dataclass
class MoogiResynthesizer:
    """Small explicit-error observe/integrate/learn/resynthesize teaching runtime."""

    observations: list[dict[str, Any]] = field(default_factory=list)

    def observe(self, sample: dict[str, Any]) -> None:
        self.observations.append(dict(sample))

    def integrate(self) -> dict[str, Any]:
        return {
            "count": len(self.observations),
            "keys": sorted({k for row in self.observations for k in row}),
        }

    def learn(self) -> dict[str, Any]:
        numeric: dict[str, list[float]] = {}
        for row in self.observations:
            for key, value in row.items():
                if isinstance(value, (int, float)) and not isinstance(value, bool):
                    numeric.setdefault(key, []).append(float(value))
        return {
            key: {
                "mean": sum(values) / len(values),
                "min": min(values),
                "max": max(values),
            }
            for key, values in numeric.items()
            if values
        }

    def exact_resynthesize(self, target: dict[str, Any]) -> LearningTrace:
        integrated = self.integrate()
        learned = self.learn()
        reconstruction: dict[str, Any] = {}
        squared_error = 0.0
        count = 0
        notes: list[str] = []
        for key, value in target.items():
            if key in learned and isinstance(value, (int, float)) and not isinstance(value, bool):
                prediction = learned[key]["mean"]
                reconstruction[key] = prediction
                squared_error += (prediction - float(value)) ** 2
                count += 1
            else:
                reconstruction[key] = None
                notes.append(f"no learned numeric estimator for {key}")
        error = (squared_error / count) ** 0.5 if count else 0.0
        exact = error == 0.0 and not notes
        return LearningTrace(
            observations=tuple(self.observations),
            integrated_state=integrated,
            learned_state=learned,
            reconstruction=reconstruction,
            error=error,
            exact=exact,
            notes=tuple(notes),
        )


def reference_binding() -> tuple[BoundSource, PrimalDualProjection]:
    fisica = SourceRef(
        source_id="FISICA_COMPUTACIONAL",
        repository="jbermejovega/fisicacomputacional",
        path="06_Monte_Carlo_Ising",
        role="upstream_teaching_source",
    )
    uimp = SourceRef(
        source_id="UIMP_QML",
        repository="jbermejovega/UIMPIntroToQuantumAI",
        path="tutorials/practica-2026-ising-duality",
        role="public_course_projection",
    )
    bound = bind(fisica, uimp, note="Ising teaching lineage")
    return bound, quazris_project(bound)


__all__ = [
    "SCHEMA_ID",
    "BindOp",
    "SemiOp",
    "SourceRef",
    "BindingWitness",
    "BoundSource",
    "PrimalDualProjection",
    "LearningTrace",
    "bind",
    "debind",
    "rebind",
    "rekontra_bind",
    "semi_compose",
    "quazris_project",
    "MoogiResynthesizer",
    "reference_binding",
]
