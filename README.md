# Introduction to Quantum Artificial Intelligence

**Jara Juana Bermejo Vega · UIMP Quantum Machine Learning**

This repository is the public teaching/release surface for the course. The
private SIGILBOOK metaproject is not published by implication; only typed
teaching projections and provenance references are exposed here.

## Start here

- [PACADOC](PACADOC.md) — student first-use guide
- [Web/WML landing](site/index.html) — course map and codebook browser
- [Juani QML lecture notes — abridged 2026](docs/teaching/JUANI_QML_LECTURE_NOTES_ABRIDGED_2026.md)
- [2026 Ising/Duality Codebook](tutorials/practica-2026-ising-duality/README.md)
- [Research Sync — TFG/TFM/PhD focus areas](docs/teaching/RESEARCH_SYNC_TFG_TFM_PHD_V1.md)
- [CCMS source](ccms/paca_docencia_superlattice_v1.json)
- [PACA DOCENCIA CCMS/KUIR facet](docs/PACA_DOCENCIA_CCMS_KUIR_FACET_V1.md)
- [Full 2025 course guide](docs/legacy/README_2025_FULL.md) — restored historical setup/tutorial documentation

## 2026 syllabus

### General introduction to AI — Juani

- what is learning?
- paradigms: supervised vs unsupervised learning
- training, validation, generalization and trainability
- automata / Ising model as the practice spine
- current topics in ML and QML

Campus-ready description: [General introduction to AI / ML](docs/teaching/JUANI_QML_LECTURE_NOTES_ABRIDGED_2026.md#campus-description--general-introduction-to-ai--ml)

### Classical models — Daniel / David

- PCA — Daniel
- trees and random forests — Daniel
- neural networks — Daniel
- k-means and clustering — David, 1h
- support vector machines — David, 1h

### Quantum Machine Learning — Juani

- quantum advantage
- re-quantization / quantum representations
- quantum-inspired methods
- quantum optimization
- learning from quantum data and experiments
- trainability, noise and resource accounting

Campus-ready description: [Quantum Machine Learning](docs/teaching/JUANI_QML_LECTURE_NOTES_ABRIDGED_2026.md#campus-description--quantum-machine-learning)

Research-frontier topics are **not** automatically part of the base syllabus. They are synchronized only for [TFG/TFM/PhD projects](docs/teaching/RESEARCH_SYNC_TFG_TFM_PHD_V1.md).

### Quantum Machine Learning Models

- HHL / linear fitting — David, 1h
- quantum kernels — David, 1h
- ML for and with quantum — Roberta, 1h
- quantum perceptron — Roberta, 1h
- quantum associative memory — Roberta, 1h
- quantum reservoir computing — Roberta, 2h
- hands-on lecture — 2h

## Exercises

- **Juani:** contextual kernel — classical/quantum Ising and duality codebook
- **Daniel:** neural networks for entanglement detection (classical)
- **David:** SVM classification with classical and PennyLane quantum feature spaces
- **Roberta:** critical assessment of QNN design

## 2026 practice

The Juani practice is one executable textbook/codebook for Physics,
Mathematics and Computer Science:

```text
Ising / Metropolis
-> Onsager / Kramers-Wannier
-> Hopfield
-> transverse-field Ising
-> genus-2 Z2 sectors
-> Montonen-Olive comparison
-> contextual kernels
-> Anderson / Aubry-André
-> circle map / Kuramoto
-> swarmalators 1D and 2D
```

The codebook keeps analogy, duality and physical equivalence distinct.

### Minimal install

```bash
git clone https://github.com/jbermejovega/UIMPIntroToQuantumAI.git
cd UIMPIntroToQuantumAI/tutorials/practica-2026-ising-duality
python -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
jupyter lab ising_duality_codebook.ipynb
```

Optional public SIGIL semantic/replay layer, when available from the configured
package source:

```bash
python -m pip install sigil4py
```

The scientific calculations do not require access to the private SIGILBOOK
repository.

## Existing tutorials retained

- `tutorials/tutorial1-quantum-linear-solvers/hhl_tutorial.ipynb`
- `tutorials/tutorial2-quantum-linear-solvers-and-data-fitting/data-fitting.ipynb`
- `tutorials/tutorial2-quantum-linear-solvers-and-data-fitting/hhl-sandbox.ipynb`

The full older setup guide has been restored under
`docs/legacy/README_2025_FULL.md` instead of being lost behind the shorter
normalization landing page.

## CCMS / KOKO local control plane

```bash
python tools/koko_docencia.py validate
python tools/koko_docencia.py science-smoke
python tools/koko_docencia.py notebook-smoke
python tools/koko_docencia.py db-build
python tools/koko_docencia.py jauria
python tools/koko_docencia.py preworkflow
```

Tool facets:

```text
CLICK · CLIT · ZELDA · POLES · KIT · QIT · GIT · JAURIA · BROWSER · DB
```

The scheduler is an acyclic DAG. Cocyclic/chiral structures are semantic
overlays with explicit witnesses, not causal back-edges.

## First student rule

```text
one error
one change
one rerun
one note
```

Record the exact error, notebook/cell, Python version, environment and relevant
parameters before changing the environment.
