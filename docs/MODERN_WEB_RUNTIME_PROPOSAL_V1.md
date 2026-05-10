# Modern Web Runtime Proposal V1

## Goal

Transform UIMPIntroToQuantumAI from a static repository into a modern student-facing web platform.

The repository should evolve toward:

- interactive browser-first learning
- reproducible notebooks
- replay-safe experiments
- modern ASGI deployment
- visualization-first pedagogy
- mobile compatibility
- live quantum/AI demos

---

## Recommended architecture

```text
Frontend
  ↓
Next.js / React
  ↓
FastAPI + Django ASGI
  ↓
QUO admissibility layer
  ↓
Replay runtime
  ↓
Experiment persistence
```

---

## Student-facing priorities

### 1. Interactive web UI

Recommended:

- React
- Next.js
- Tailwind
- JupyterLite
- Plotly
- Observable visualizations

Students should be able to:

- run notebooks in-browser
- manipulate quantum states visually
- inspect tensor networks
- visualize probability amplitudes
- replay experiments deterministically

---

### 2. Replay-safe notebooks

Introduce:

- append-only manifests
- deterministic notebook replay
- experiment hashes
- PACAPANDOC normalization

This prevents:

- notebook drift
- hidden state
- irreproducible execution

---

### 3. QUANTUMDJANGO runtime

The platform should evolve from:

```text
request → response
```

into:

```text
experiment → replay → visualization → persistence
```

---

### 4. Mobile-first deployment

Target:

- PinePhone
- Debian mobile
- tablets
- low-resource Linux devices

The platform should behave as:

```text
portable educational replay runtime
```

---

### 5. Federation-ready stack

Suggested repositories:

```text
UIMPIntroToQuantumAI
sigil4py
quoquantum
quantumdjango
pacapandoc
```

---

## Immediate modernization tasks

- modern README landing page
- Docker/Podman support
- FastAPI server
- WebSocket live sessions
- notebook gallery
- quantum visualization demos
- reproducible environments
- pyproject.toml migration
- GitHub Actions CI
- static docs deployment

---

## Long-term direction

The repository should become:

```text
web-native replay-safe quantum AI learning platform
```

rather than only a code archive.

---

## Final compression

```text
modern educational web runtime
```

```text
interactive replay-safe quantum AI pedagogy
```
