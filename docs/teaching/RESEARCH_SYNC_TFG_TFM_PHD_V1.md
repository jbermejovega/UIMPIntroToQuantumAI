# Research Sync — TFG / TFM / PhD only · 2026

**Schema:** UIMP_QML_RESEARCH_SYNC_TFG_TFM_PHD_V1  
**Policy:** research synchronization does not mutate the base QML course automatically.

## 1. Scope gate

This layer is enabled only for:

~~~text
TFG
TFM
PhD
~~~

It is **not** part of the mandatory syllabus and must not silently change lectures, exercises or ordinary assessment.

~~~text
research frontier != base syllabus
research sync != automatic course rewrite
~~~

Promotion into the base course requires explicit teaching review.

## 2. KOKO research workflow

~~~text
research source
-> CCMS / knowledge view
-> KOKO status + sources + graph
-> evidence / code / literature
-> SYNKK checkpoint
-> supervisor review
-> TFG / TFM / PhD focus area
~~~

Hard boundaries:

~~~text
dynamic CCMS != repository canon
RAG evidence != proof
notebook/CLI != authority
~~~

## 3. Focus areas

### F1 — Foundations of quantum computational advantage

- complexity-theoretic vs practical advantage;
- classical simulation and verification;
- noise, data loading and resource accounting.

Course bridge:
[Quantum advantage](JUANI_QML_LECTURE_NOTES_ABRIDGED_2026.md#7-what-counts-as-quantum-advantage)

### F2 — Quantum kernels, representations and trainability

- quantum feature maps;
- kernel concentration/vanishing signal;
- structured parameterized circuits;
- classical↔quantum representation comparison;
- sample and measurement complexity.

Course bridge:
[Trainability](JUANI_QML_LECTURE_NOTES_ABRIDGED_2026.md#9-trainability-and-limits)

### F3 — Ising, optimization and classical↔quantum mappings

- classical and quantum Ising;
- Hopfield / energy-based models;
- QUBO/QAOA/VQE mappings;
- Kramers-Wannier and representation dualities;
- contextual/quantum kernels.

Executable bridge:
[Ising duality practice](../../tutorials/practica-2026-ising-duality/README.md)

### F4 — Tensor networks, renormalization and structured simulation

- MPS/PEPS/tensor trains;
- DMRG and compression;
- tensor representations of circuits;
- invariant-preserving renormalization;
- HPC execution and benchmarking.

### F5 — Topological phases, QEC and MBQC

- stabilizer/graph states;
- topological and twisted quantum-double models;
- SPT/SSPT phases;
- measurement-based computation;
- symmetry-based verification;
- QEC and decoding.

### F6 — Neural quantum states and reinforcement learning

- NQS representations;
- variational many-body states;
- reinforcement-learning control/state-preparation methods;
- hybrid policies;
- tensor-network baselines.

### F7 — Learning quantum systems

- tomography and shadow methods;
- Hamiltonian/Liouvillian learning;
- learning properties rather than full states;
- adaptive vs non-adaptive measurements.

### F8 — Differential geometry + derived/twisted categories

Research-only mathematical layer. The standard mathematical spine is fixed first:

~~~text
smooth manifolds
-> tangent / cotangent bundles
-> differential forms
-> exterior derivative d
-> closed forms: dω = 0
-> exact forms: ω = dη
-> d² = 0
-> de Rham cohomology H^•_dR
-> pullback / pushforward where defined
-> vector bundles + connections
-> curvature / holonomy
~~~

This gives the basic local/global distinction used in the research layer:

~~~text
exact => closed
closed != exact in general
local potential != global potential
cohomology class = obstruction/invariant to global exactness
~~~

The categorical extension is then layered on top, rather than used as a replacement for differential geometry:

~~~text
differential geometry
-> chain / cochain complexes
-> derived constructions
-> derived categories / derived functors
-> cocycle-twisted and graded categories
-> monoidal / braided / higher and polycategorical composition
-> twistor constructions
-> project-local "twisor" carriers
-> concept / Konzept categories
-> KUIR typed interfaces
-> QUAZRIS primal/dual projections
~~~

**Twist attitude** is treated as a project-local descriptor of which structure a twist changes or preserves. It may encode, for example, a cocycle, grading, connection/holonomy datum, orientation/chirality choice or a change of presentation. It never licenses an untyped identification between two theories.

Discipline:

- standard mathematical notions keep their standard definitions;
- pullback of differential forms is contravariant and preserves the exterior derivative;
- cohomological equivalence does not imply equality of representatives;
- derived equivalence, categorical duality, a cocycle twist and a twistor transform are distinct claims;
- project-local SIGIL notions such as "twisor", "twist attitude", KonzeptKategorie and KUIR/QUAZRIS carriers are typed adapters/presentations;
- a common interface does not establish an equivalence theorem.

Candidate TFG/TFM/PhD questions:

- geometric feature maps and kernels on manifolds;
- learning closed/exact differential forms or cohomology-sensitive observables from data;
- bundle/gauge-equivariant learning and connection-aware architectures;
- curvature/Laplacian descriptors for graph and manifold learning;
- categorical organization of primal/dual representations;
- derived/twisted invariants as data descriptors;
- twistor-inspired coordinates for structured quantum models;
- topological obstructions to globally consistent learned coordinates;
- diagrammatic/polykategorical semantics for hybrid workflows.

Course bridge:

~~~text
Ising / kernels / Laplacians
-> geometry of representations
-> topology / cohomological obstructions
-> advanced derived/twisted research questions
~~~

This bridge is **research-facing only**. It is not a mandatory learning outcome of the base QML course.

### F9 — Compositional semantics and research software architecture

- SIGIL/SIGILITAS;
- KUIR typed interfaces;
- QUAZRIS primal/dual projections;
- CCMS/polykategory organization;
- reproducible codebooks;
- typed runtime boundaries;
- evidence/provenance/replay.

This line studies research methodology and infrastructure; it does not by itself establish physical quantum advantage.

## 4. Level routing

### TFG

~~~text
one model
+ one reproducible implementation
+ one controlled comparison
+ one delimited research question
~~~

### TFM

~~~text
literature synthesis
+ reproducible code
+ nontrivial comparison/extension
+ research-grade evaluation
~~~

### PhD

~~~text
coherent research programme
+ plural papers/local sections
+ shared methodological spine
+ explicit provenance and reproducibility
~~~

## 5. Admission rule

A topic enters a final-project route only when the supervisor can bind:

~~~text
research question
+ prerequisites
+ source literature
+ executable/reproducible path
+ evaluation criterion
+ expected contribution
~~~

Otherwise it remains exploratory/HOLD.

## 6. Thesis-safe boundary

~~~text
interesting analogy != thesis result
diagrammatic correspondence != theorem
model output != experimental evidence
RAG retrieval != literature validation
software test != scientific certification
~~~
