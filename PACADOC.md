# PACADOC — UIMP Intro to Quantum AI

```yaml
capsule:
  id: PACADOC_UIMP_INTRO_TO_QUANTUM_AI_2026_V1
  type: first_user_student_landing_document
  status:
    candidate: true
    student_facing: true
    accessibility_first: true
    reproducibility_first: true
    hosted_ci_claimed: false
    physics_certification_claimed: false
  repository:
    owner: jbermejovega
    name: UIMPIntroToQuantumAI
    target_branch: main
  public_private_boundary:
    zero_source: jbermejovega/sigilbook
    public_course_projection: jbermejovega/UIMPIntroToQuantumAI
    authority_transport: false
    private_source_publication: false
```

## 1. First path

For the 2026 QML practical:

```text
1. Read README.md.
2. Open tutorials/practica-2026-ising-duality/README.md.
3. Create a clean Python environment.
4. Install requirements.txt.
5. Open ising_duality_codebook.ipynb.
6. Run cells in order.
7. Change one parameter at a time.
8. Record outputs, errors and interpretation.
```

The web/WML projection is available at `site/index.html`.

## 2. Minimal install

```bash
git clone https://github.com/jbermejovega/UIMPIntroToQuantumAI.git
cd UIMPIntroToQuantumAI/tutorials/practica-2026-ising-duality
python -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
jupyter lab ising_duality_codebook.ipynb
```

Windows PowerShell activation:

```powershell
.venv\Scripts\Activate.ps1
```

Optional public semantic/replay layer:

```bash
python -m pip install sigil4py
```

The scientific notebook remains executable without private SIGILBOOK access.

## 3. Course map

### Juani

General introduction to AI:

- what is learning?
- supervised vs unsupervised learning
- trainability and generalization
- automata / Ising model
- current topics

Quantum Machine Learning:

- quantum advantage
- re-quantization / representations
- quantum-inspired methods
- quantum optimization
- trainability and limitations

Practice:

```text
Ising
-> Onsager/Kramers-Wannier
-> Hopfield
-> quantum Ising
-> topology
-> electric/magnetic duality comparison
-> contextual kernel
-> localization
-> oscillators
-> swarmalators
```

### Daniel / David / Roberta

The complete shared syllabus is maintained in `README.md` and in the CCMS
manifest.

## 4. Textbook/codebook rule

The standard public codebook form is:

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

Typed pedagogical vocabulary:

```text
SIGIL[chapter]
PLURALTYPE[representations]
QUNO[coexisting alternatives]
CODEBOOK[executable witness]
```

Plurality does not imply identity collapse.

## 5. Physics boundary

The codebook explicitly keeps these distinctions:

```text
Kramers-Wannier duality != Metropolis update rule
Hopfield != Onsager square-lattice Ising
Anderson != Aubry-André != Mott/Higgs localization
Kuramoto != circle-map mode locking
Kuramoto != swarmalator dynamics
Montonen-Olive comparison != simulation of N=4 SYM
```

A typed map or shared interface is not by itself a physical equivalence theorem.

## 6. CCMS / KUIR

The public teaching source is:

`ccms/paca_docencia_superlattice_v1.json`

The architectural explanation is:

`docs/PACA_DOCENCIA_CCMS_KUIR_FACET_V1.md`

Local validation:

```bash
python tools/koko_docencia.py preworkflow
```

Core tool facets:

```text
CLICK · CLIT · ZELDA · POLES · KIT · QIT · GIT · JAURIA · BROWSER · DB
```

## 7. Replay rule

```text
one error
one change
one rerun
one note
```

Minimum record:

```yaml
replay_record:
  repository: UIMPIntroToQuantumAI
  commit: "<git sha>"
  notebook: tutorials/practica-2026-ising-duality/ising_duality_codebook.ipynb
  python_version: "..."
  package_versions: "..."
  random_seed: "..."
  parameters: "..."
  status: pass_or_error
```

## 8. Historical material

The full earlier course guide has been restored at:

`docs/legacy/README_2025_FULL.md`

Existing HHL/data-fitting notebooks remain under `tutorials/`.

## 9. Student debugging rule

Do not alter many dependencies at once. Record:

```text
operating system
Python version
environment name
notebook
cell
parameters
exact error
last successful step
```

## 10. Final law

```text
no replay -> no certified result
presentation != certification
public projection != private authority
```
