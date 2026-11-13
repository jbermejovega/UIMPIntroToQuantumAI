"""QUAZRIS finite horn-candidate / MPI work partition for nine Jupyter activities.

Source-bound scheduling only. No MPI runtime or categorical Kan proof claimed.
"""
from __future__ import annotations
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
NAMES = tuple(f"{i:02}.ipynb" for i in range(1, 10))


def distribute(size: int) -> dict[int, tuple[str, ...]]:
    if not isinstance(size, int) or isinstance(size, bool) or size < 1:
        raise ValueError("MPI_SIZE_MUST_BE_POSITIVE")
    return {rank: tuple(name for i, name in enumerate(NAMES) if i % size == rank)
            for rank in range(size)}


def check_horn_candidate() -> dict:
    """Check the finite incidence of nine tasks, not a Kan filler."""
    missing = [name for name in NAMES if not (ROOT / "codebooks" / name).is_file()]
    return {"status": "HOLD_MISSING_NOTEBOOK" if missing else "FINITE_HORN_CANDIDATE",
            "missing": missing, "kan_filler_certified": False, "mpi_executed": False}


def main():
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--ranks", type=int, default=3)
    parser.add_argument("--rank", type=int, default=None)
    args = parser.parse_args()
    partitions = distribute(args.ranks)
    if args.rank is not None and args.rank not in partitions:
        parser.error("rank outside range")
    print(json.dumps({"distribution": {str(k): list(v) for k, v in partitions.items()
                        if args.rank is None or args.rank == k},
                      "horn": check_horn_candidate(),
                      "mode": "PLAN_ONLY"}, sort_keys=True))


if __name__ == "__main__":
    main()
