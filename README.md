# Introduction to Quantum Artificial Intelligence

**Jara Juana Bermejo Vega · UIMP Quantum Machine Learning**

This repository is the public teaching/release surface for the course. The
private SIGILBOOK metaproject is not published by implication; only typed
teaching projections and provenance references are exposed here.

## 1 Table of Contents

Historical root anchors are preserved so old course links keep working. The
complete setup text lives in the restored legacy guide; current teaching
material stays on this landing page.

- [1 Table of Contents](#1-table-of-contents)
- [2 About](#2-about)
- [3 Preliminaries: setting up your computer](#3-preliminaries-setting-up-your-computer)
  - [3.1 Linux](#31-linux)
  - [3.2 MacOS](#32-macos)
  - [3.3 Windows](#33-windows)
    - [3.3.1 Package Managers](#331-package-managers)
  - [3.4 Development environment Visual Studio Code](#34-development-environment-visual-studio-code)
    - [3.4.1 VS Code Command Palette](#341-vs-code-command-palette)
    - [3.4.2 Default Terminal](#342-default-terminal)
    - [3.4.3 VS Code Extensions](#343-vs-code-extensions)
  - [3.5 Python](#35-python)
    - [3.5.1 Anaconda (Miniconda)](#351-anaconda-miniconda)
    - [3.5.2 Python Environments](#352-python-environments)
  - [3.6 Version control with Git](#36-version-control-with-git)
- [4 Installing Python packages, Jupyter and QisKit](#4-installing-python-packages-jupyter-and-qiskit)
  - [4.1 Create a Python environment](#41-create-a-python-environment)
  - [4.2 Installing Python packages](#42-installing-python-packages)
  - [4.3 Setting up IJupyter kernels](#43-setting-up-ijupyter-kernels)
  - [4.4. Python tools for scientific computing](#44-python-tools-for-scientific-computing)
- [5 Try the tutorials](#5-try-the-tutorials)
- [6 Python for Scientific computing](#6-python-for-scientific-computing)
  - [6.1 Randomized algorithms and concentration inequalities](#61-randomized-algorithms-and-concentration-inequalities)
- [EXERCISE](#exercise)
- [MATERIALS](#materials)
- [2026 syllabus](#2026-syllabus)
- [2026 practice](#2026-practice)
- [CCMS / KOKO local control plane](#ccms--koko-local-control-plane)

Typed navigation sources:

- [SIGIL/KRONE/KUIR navigation atlas](ccms/sigil_course_navigation_v1.json)
- [Web/WML landing](site/index.html)
- [PACADOC](PACADOC.md)

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

Research-frontier topics are **not** automatically part of the base syllabus.
They are synchronized only for
[TFG/TFM/PhD projects](docs/teaching/RESEARCH_SYNC_TFG_TFM_PHD_V1.md).

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
-> classical reference and critical resource accounting
```

Advanced localization, oscillator and SIGIL semantic material remains in the
notebook as **research appendices** for TFG/TFM/PhD routes.

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

The full older setup guide is preserved under
`docs/legacy/README_2025_FULL.md`.

## CCMS / KOKO local control plane

```bash
python tools/koko_docencia.py validate
python tools/koko_docencia.py toc-check
python tools/koko_docencia.py toc
python tools/koko_docencia.py localize linux
python tools/koko_docencia.py science-smoke
python tools/koko_docencia.py notebook-smoke
python tools/koko_docencia.py db-build
python tools/koko_docencia.py preworkflow
```

Tool facets:

```text
CLICK · CLIT · ZELDA · POLES · KIT · QIT · GIT
JAURIA · BROWSER · BIND · TOC · LOCALIZE
```

Navigation is represented geometrically as an **atlas**: documents are charts,
anchors/artifacts are local sections, hyperlinks are seams, and missing
files/anchors are obstructions. Localization selects the narrowest interface
needed for a section; it does not change semantic authority.

The scheduler remains an acyclic DAG. Cocyclic/chiral structures are semantic
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

---

## Historical anchor compatibility

The sections below intentionally preserve the old GitHub root anchors. Each
heading redirects to the restored full guide.

## 2 About

[Open the full historical section](docs/legacy/README_2025_FULL.md#2-about).

## 3 Preliminaries: setting up your computer

[Open the full historical section](docs/legacy/README_2025_FULL.md#3-preliminaries-setting-up-your-computer).

### 3.1 Linux

[Open section 3.1](docs/legacy/README_2025_FULL.md#31-linux).

### 3.2 MacOS

[Open section 3.2](docs/legacy/README_2025_FULL.md#32-macos).

### 3.3 Windows

[Open section 3.3](docs/legacy/README_2025_FULL.md#33-windows).

#### 3.3.1 Package Managers

[Open section 3.3.1](docs/legacy/README_2025_FULL.md#331-package-managers).

### 3.4 Development environment Visual Studio Code

[Open section 3.4](docs/legacy/README_2025_FULL.md#34-development-environment-visual-studio-code).

#### 3.4.1 VS Code Command Palette

[Open section 3.4.1](docs/legacy/README_2025_FULL.md#341-vs-code-command-palette).

#### 3.4.2 Default Terminal

[Open section 3.4.2](docs/legacy/README_2025_FULL.md#342-default-terminal).

#### 3.4.3 VS Code Extensions

[Open section 3.4.3](docs/legacy/README_2025_FULL.md#343-vs-code-extensions).

### 3.5 Python

[Open section 3.5](docs/legacy/README_2025_FULL.md#35-python).

#### 3.5.1 Anaconda (Miniconda)

[Open section 3.5.1](docs/legacy/README_2025_FULL.md#351-anaconda-miniconda).

#### 3.5.2 Python Environments

[Open section 3.5.2](docs/legacy/README_2025_FULL.md#352-python-environments).

### 3.6 Version control with Git

[Open section 3.6](docs/legacy/README_2025_FULL.md#36-version-control-with-git).

## 4 Installing Python packages, Jupyter and QisKit

[Open the full historical section](docs/legacy/README_2025_FULL.md#4-installing-python-packages-jupyter-and-qiskit).

### 4.1 Create a Python environment

[Open section 4.1](docs/legacy/README_2025_FULL.md#41-create-a-python-environment).

### 4.2 Installing Python packages

[Open section 4.2](docs/legacy/README_2025_FULL.md#42-installing-python-packages).

### 4.3 Setting up IJupyter kernels

[Open section 4.3](docs/legacy/README_2025_FULL.md#43-setting-up-ijupyter-kernels).

### 4.4. Python tools for scientific computing

[Open section 4.4](docs/legacy/README_2025_FULL.md#44-python-tools-for-scientific-computing).

## 5 Try the tutorials

[Open the historical tutorial section](docs/legacy/README_2025_FULL.md#5-try-the-tutorials).

## 6 Python for Scientific computing

[Open the historical scientific-Python section](docs/legacy/README_2025_FULL.md#6-python-for-scientific-computing).

### 6.1 Randomized algorithms and concentration inequalities

[Open section 6.1](docs/legacy/README_2025_FULL.md#61-randomized-algorithms-and-concentration-inequalities).

## EXERCISE

[Open the historical exercise section](docs/legacy/README_2025_FULL.md#exercise).

## MATERIALS

[Open the historical materials section](docs/legacy/README_2025_FULL.md#materials).
