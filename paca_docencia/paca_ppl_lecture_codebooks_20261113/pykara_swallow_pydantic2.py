"""KOKO PYKARA SWALLOW · source-bound Pydantic 2 planning for PACA DOCENCIA.

The carrier validates an explicit, deterministic nine-unit teaching manifest.
No GitHub mutation, Monty execution or runtime certification occurs here.
See SIGILBOOK resident PYDANTIKA_PYKARA_KIRBY_SPOON_SQUASH_V1 and
KOKO3_MONTY_EFFECT_GATE_V1 for authority boundaries.
"""
from __future__ import annotations

from enum import StrEnum
from hashlib import sha256
import json
from pathlib import Path
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field, model_validator


class Status(StrEnum):
    SOURCE_PLAN = "SOURCE_PLAN"
    HOLD = "HOLD"


class Frozen(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True, strict=True)


class TeachingOccurrence(Frozen):
    index: int = Field(ge=1, le=9)
    note_path: str = Field(min_length=1)
    codebook_path: str = Field(min_length=1)
    source_reference: str = Field(min_length=1)
    editorial_author: Literal["JJBV"] = "JJBV"
    no_original_binary_transferred: Literal[True] = True
    source_rights_cleared: Literal[False] = False
    scientific_execution_verified: Literal[False] = False


class SwallowPlan(Frozen):
    schema_id: Literal["PACA_PYKARA_SWALLOW_DOCENCIA_V1"] = "PACA_PYKARA_SWALLOW_DOCENCIA_V1"
    source_repository: Literal["jbermejovega/sigilbook"] = "jbermejovega/sigilbook"
    target_repository: Literal["jbermejovega/Quantum-AI-for-Queens"] = "jbermejovega/Quantum-AI-for-Queens"
    target_branch: Literal["main"] = "main"
    protected_identity: Literal["PIORNALEGO_ES_CANON"] = "PIORNALEGO_ES_CANON"
    source_pr_number: Literal[7] = 7
    state: Literal["SOURCE_PLAN"] = "SOURCE_PLAN"
    source_head: str = Field(pattern=r"^[0-9a-f]{40}$")
    occurrences: tuple[TeachingOccurrence, ...]

    @model_validator(mode="after")
    def complete_distinct_sources(self):
        if tuple(x.index for x in self.occurrences) != tuple(range(1, 10)):
            raise ValueError("EXPECTED_NINE_ORDERED_UNITS")
        paths = [p for x in self.occurrences for p in (x.note_path, x.codebook_path)]
        if len(paths) != len(set(paths)):
            raise ValueError("DUPLICATE_TARGET_OCCURRENCE")
        return self

    def receipt(self):
        payload = self.model_dump(mode="json")
        digest = sha256(json.dumps(payload, sort_keys=True, separators=(",", ":")).encode()).hexdigest()
        return {"schema_id": self.schema_id, "sha256": digest, "status": Status.SOURCE_PLAN.value,
                "git_mutation": False, "monty_executed": False, "ci_certified": False}


SOURCES = (
    "QAOA_MaxCut(tutorial).ipynb",
    "VQE_on_1D_TFIM(tutorial).ipynb",
    "QAOA_DMRG.ipynb",
    "Quimb_DMRG_para_TFIM.ipynb",
    "Scaling_of_variational_quantum_circuit_depth_for_condensed_matter_systems.ipynb",
    "Clasificación_de_Imágenes_mediante_QTT.ipynb; Clasificación_de_Imágenes_mediante_Redes_de_Tensores (1).ipynb",
    "QUANTIC_MPS.ipynb",
    "Redes_tensoriales_MPO.ipynb",
    "article_𝚀𝚄𝙱𝙾 for training regression models.pdf",
)


def build_plan(source_head: str) -> SwallowPlan:
    return SwallowPlan(source_head=source_head, occurrences=tuple(
        TeachingOccurrence(
            index=i, note_path=f"lecture_notes/{i:02}.md",
            codebook_path=f"codebooks/{i:02}.ipynb", source_reference=source)
        for i, source in enumerate(SOURCES, 1)))


def inspect_local(root: Path, source_head: str) -> dict:
    """Validate paths and notebook shape only; never execute exercise placeholders."""
    plan = build_plan(source_head)
    missing = []
    malformed = []
    for item in plan.occurrences:
        for name in (item.note_path, item.codebook_path):
            path = root / name
            if not path.is_file():
                missing.append(name)
        nb = root / item.codebook_path
        if nb.is_file():
            try:
                data = json.loads(nb.read_text(encoding="utf-8"))
                if data.get("nbformat") != 4 or not isinstance(data.get("cells"), list):
                    malformed.append(item.codebook_path)
                elif any(c.get("outputs") or c.get("execution_count") is not None
                         for c in data["cells"] if c.get("cell_type") == "code"):
                    malformed.append(item.codebook_path)
            except (UnicodeError, ValueError):
                malformed.append(item.codebook_path)
    return {**plan.receipt(), "status": "HOLD" if missing or malformed else "SOURCE_PLAN",
            "missing": missing, "malformed": malformed,
            "notebook_science_tested": False, "rights_approved": False}


if __name__ == "__main__":
    print(json.dumps(inspect_local(Path(__file__).resolve().parent,
        "57026af5da039388d98478398825b4d7ad53393b"), sort_keys=True, ensure_ascii=False))
