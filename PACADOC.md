# PACADOC — UIMP Intro to Quantum AI

```yaml
capsule:
  id: PACADOC_UIMP_INTRO_TO_QUANTUM_AI_V1_0_0
  type: first_user_student_landing_document

  status:
    canonical: true
    normalized: true
    stable_release: true
    release_number: "1.0.0"
    student_facing: true
    UIMP_ready: true
    safety_first: true
    accessibility_first: true
    reproducibility_first: true
    no_open_branch: true

  repository:
    owner: jbermejovega
    name: UIMPIntroToQuantumAI
    default_branch: main

  audience:
    - UIMP students
    - first-time quantum AI learners
    - teaching assistants
    - course reviewers

  kernel:
    - PACA_CORE
    - PACA_PDG
    - SIGIL
    - UAP
    - TRACE
    - JUPYTER
    - PYTHON
    - QISKIT
```

## 1. What this repository is

This repository is a first-user educational repository for an introduction to Quantum Artificial Intelligence.

It contains teaching material, setup instructions, notebooks, exercises, and supporting resources for students who may be using different operating systems and Python environments.

The normalized rule is:

```text
many machines
many environments
one replay-stable learning path
```

## 2. First-user path

Start here:

```text
1. Read README.md.
2. Install Python or Miniconda.
3. Create a clean course environment.
4. Install Jupyter and required packages.
5. Open notebooks in order.
6. Run cells slowly.
7. Save errors and fixes.
8. Ask for help with the exact error message.
```

## 3. Student safety rule

Do not debug by changing many things at once.

Use:

```text
one error
one change
one rerun
one note
```

If something fails, record:

```text
operating system
Python version
environment name
notebook name
cell number
error message
last command executed
```

## 4. Accessibility rule

Learning material should remain readable under student conditions:

- small screens;
- fatigue;
- multilingual reading;
- unstable internet;
- first-time terminal use;
- anxiety around programming errors.

Operational writing rule:

```text
one step per line
one command per block
no hidden assumptions
```

## 5. Reproducibility rule

A notebook result is considered course-stable only if the execution path can be explained and replayed.

```text
no replay → no certified result
```

Minimum reproducibility record:

```yaml
replay_record:
  repository: UIMPIntroToQuantumAI
  notebook: path/to/notebook.ipynb
  environment: course_environment_name
  python_version: "..."
  package_manager: conda_or_pip
  status: pass_or_error
```

## 6. PACA/PACAPDG interpretation

Different systems may render the same educational object differently:

- Linux terminal;
- macOS terminal;
- Windows PowerShell;
- VS Code;
- JupyterLab;
- browser notebook.

The invariant is:

```text
Π(quo(r_i(X))) = Π(quo(r_j(X)))
```

Meaning:

```text
different student environments
same learning identity
```

## 7. Course conduct

Allowed:

- ask for help early;
- share error messages;
- compare outputs;
- document fixes;
- rerun notebooks;
- use accessible settings.

Forbidden:

- hiding errors;
- copying outputs without running or understanding the path;
- changing many dependencies without recording changes;
- presenting non-reproducible output as final.

## 8. Minimal command discipline

Use commands in small blocks.

```bash
python --version
```

```bash
conda --version
```

```bash
jupyter --version
```

Do not paste long unknown command chains without reading them.

## 9. Teaching assistant checklist

```text
student can open terminal
student can identify environment
student can launch Jupyter
student can run first notebook
student can copy exact error
student can reset/recreate environment if needed
```

## 10. Final law

```text
quantum AI learning is valid when the student can replay the path,
not when the notebook merely appears to have output.
```

## 11. Final statement

This repository is PACADOC-normalized for first users: it prioritizes clear entry, accessibility, safe debugging, reproducible notebooks, and traceable learning.
