# Codebook 2026 — Ising, duality and contextual kernels

**Course:** Quantum Machine Learning · UIMP  
**Format:** SIGILBOOK / PLURALTYPE textbook codebook  
**Audience:** Physics · Mathematics · Computer Science  
**Status:** public teaching projection

## Install

The public codebook has a deliberately small scientific base:

```bash
git clone https://github.com/jbermejovega/UIMPIntroToQuantumAI.git
cd UIMPIntroToQuantumAI/tutorials/practica-2026-ising-duality

python -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
jupyter lab ising_duality_codebook.ipynb
```

On Windows PowerShell, activate with:

```powershell
.venv\Scripts\Activate.ps1
```

### SIGIL4Py layer

The notebook is scientifically self-contained. If a public `sigil4py` distribution is available in your configured package source, install it as an optional semantic/replay layer:

```bash
python -m pip install sigil4py
```

The notebook detects it with a guarded import. Absence of `sigil4py` does **not** change the Ising/Hopfield/TFIM calculations.

This separation is intentional:

```text
scientific result != private SIGILBOOK availability
public codebook + optional sigil4py projection
```

## Textbook type

The codebook follows the textbook grammar used by the SIGILBOOK computational-physics masterbook:

```text
chapter
-> mathematical kernel
-> observables
-> executable model
-> experiment
-> interpretation
-> reproducibility witness
-> exercises
```

The typed pedagogical carriers are:

```text
SIGIL[chapter]
PLURALTYPE[valid representations]
QUNO[coexisting alternatives]
CODEBOOK[executable witness]
```

Here, **QUNO means plurality without identity collapse**. Distinct physical mechanisms remain distinct even when they are compared through the same pedagogical interface.

## Base-course path

1. Classical Ising model and local Metropolis dynamics.
2. Onsager critical scale and Kramers–Wannier dual coupling.
3. Hopfield associative memory as an Ising-like energy model.
4. Transverse-field quantum Ising model.
5. Genus-2 homology sectors and non-contractible logical loops.
6. Montonen–Olive as an advanced strong/weak electric–magnetic comparison.
7. Contextual feature maps, PSD kernels and a classical reference.
8. Critical resource accounting before any quantum-advantage claim.

## Research appendices — not assessed in the base course

The notebook also keeps optional research bridges for TFG/TFM/PhD work:

- Anderson and Aubry–André localization;
- circle map, Arnold tongues and Kuramoto order;
- 1D/2D swarmalators;
- Bose/Jaynes–Cummings–Hubbard vocabulary;
- SIGILITAS / QUAZRIS / QUNO semantic adapters.

These sections are synchronized through [Research Sync](../../docs/teaching/RESEARCH_SYNC_TFG_TFM_PHD_V1.md), not through the ordinary course syllabus.

## Scientific boundary

The codebook distinguishes these statements:

- Kramers–Wannier duality is **not** a Metropolis update rule.
- A non-contractible loop operation is **not generically energy-neutral** for an arbitrary Ising Hamiltonian.
- Hopfield and square-lattice Onsager Ising share an energy-language analogy, but are different models.
- Anderson, Aubry–André, Mott/Higgs and mode-locking are different localization/locking mechanisms.
- Montonen–Olive is used as a conceptual example of strong/weak electric–magnetic duality; the notebook does not simulate N=4 supersymmetric Yang–Mills.

## Upstream teaching lineage

The classical statistical-physics section is aligned with:

```text
jbermejovega/fisicacomputacional
  -> 06_Monte_Carlo_Ising
  -> Modelo Hopfield
```

The UIMP repository adds the QML, duality, contextual-kernel and typed-codebook layers.

## Replay

Run:

```bash
cd ../..
python tools/koko_docencia.py preworkflow
```

The preworkflow validates the CCMS manifest, the acyclic execution DAG, the scientific core, the notebook structure and the SQLite knowledge-base projection.
