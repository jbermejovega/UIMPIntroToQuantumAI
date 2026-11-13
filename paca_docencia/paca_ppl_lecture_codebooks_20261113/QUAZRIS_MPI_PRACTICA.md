# QUAZRIS · MPI · Nine Jupyter activities

**Immediate student distribution**: [nine notebooks](codebooks/) and [paired lecture notes](lecture_notes/). Branch: `feat/paca-ppl-authorial-lecture-codebooks-20261113`, [PR #7](https://github.com/jbermejovega/Quantum-AI-for-Queens/pull/7).

## Allocation (no MPI dependency)

```bash
python quazris_mpi_distribution.py --ranks 3
python quazris_mpi_distribution.py --ranks 3 --rank 0
```

This deterministic modulo partition maps nine activities to logical MPI ranks. With 3 ranks: rank 0 gets 01,04,07; rank 1 gets 02,05,08; rank 2 gets 03,06,09. It **does not launch MPI**, execute notebooks, or certify a Kan horn filler. If an MPI runtime is available, an instructor can use the rank mapping to distribute tasks; actual parallel execution and safety gates require independent implementation.

The notebook files are original **activity scaffolds** (TODOs), not fully solved implementations or the nine original third-party notebooks. Use the four previously [native-tested reference codebooks](../codebooks_20261113/) for immediately runnable numerical demonstrations.

## Rights and trace

© 2026 JJBV for original contributions as applicable. Third-party source materials are referenced, not redistributed; future textbook rights reserved. `PIORNALEGO_ES_CANON`.
