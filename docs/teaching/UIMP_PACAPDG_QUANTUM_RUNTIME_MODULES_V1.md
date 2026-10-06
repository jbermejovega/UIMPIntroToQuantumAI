# UIMP PACAPDG QUANTUM RUNTIME MODULES V1

Author: Jara Juana Bermejo Vega  
Original synk: `7d9cafee6916072cd82b6b2811cb9714689827cf`  
Status: **historical teaching contract · revised 2026 · source-level projection**

## Correction to the original synk

The original document used closure labels such as `compiled`, `stable` and
`UIMP_ready` without carrying a course syllabus, executable teaching
certificate or hosted CI/runtime evidence.

Those labels are therefore not treated as certification.

```text
presentation != certification
source document != executed runtime
course intent != replay evidence
```

The 2026 teaching state is represented by:

- `ccms/paca_docencia_superlattice_v1.json`
- `docs/PACA_DOCENCIA_CCMS_KUIR_FACET_V1.md`
- `tutorials/practica-2026-ising-duality/`
- `tools/koko_docencia.py`
- `site/course.wml.json`

## Course syllabus

### General introduction to AI — Juani

- what is learning?
- supervised vs unsupervised learning
- trainability and generalization
- automata / Ising model as the practice spine
- current topics

### Classical models — Daniel / David

- PCA — Daniel
- trees and random forests — Daniel
- neural networks — Daniel
- k-means / clustering — David, 1h
- support vector machines — David, 1h

### Quantum Machine Learning — Juani

- quantum advantage
- re-quantization / quantum representations
- quantum-inspired methods
- quantum optimization
- trainability and limitations
- duality as a change of representation

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
- **Daniel:** classical neural networks for entanglement detection
- **David:** SVM classification with classical and PennyLane quantum feature spaces
- **Roberta:** critical assessment of QNN design

## Juani practice spine

```text
Ising / Metropolis
-> Onsager / Kramers-Wannier
-> Hopfield
-> transverse-field Ising
-> genus-2 Z2 sectors
-> Montonen-Olive comparison
-> contextual kernel
-> Anderson / Aubry-André
-> Kuramoto / circle map
-> Jaranian swarmalators 1D/2D
```

The comparisons are typed and witnessed. They are not claims that these are the
same physical theory.

## CCMS / KUIR runtime chain

```text
course source
-> CCMS manifest
-> KUIR typed interface
-> primal + dual projections
-> PACAPDG
-> RULEZERO
-> UAP
-> public codebook/browser/CLI projection
```

The local preworkflow is:

```bash
python tools/koko_docencia.py preworkflow
```

It validates source structure and scientific smoke tests. It must not be
described as hosted CI unless a hosted job actually ran.

## Public/private boundary

```text
private SIGILBOOK zero-source
!= public UIMP repository
```

The public repository may carry typed projections and provenance references.
It must not publish private SIGILBOOK source or transport its authority.

## Replay-safe educational constraints

- deterministic seeds where stochastic examples are used;
- traceable model equations and parameters;
- executable notebook witnesses;
- provenance preservation;
- attribution preservation;
- physics/analogy boundaries stated explicitly;
- no identity or authority transport.

## Current closure

```yaml
state:
  syllabus_integrated: true
  codebook_source_present: true
  ccms_manifest_present: true
  kuir_facet_present: true
  web_projection_present: true
  public_install_path_present: true
  source_validation_available: true
  hosted_ci_claimed: false
  physics_certification_claimed: false
  private_source_published: false
```
