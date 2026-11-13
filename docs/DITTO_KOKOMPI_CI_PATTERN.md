# DITTO KOKOMPI CI Pattern

```yaml
id: DITTO_KOKOMPI_CI_PATTERN_V1
repo: jbermejovega/UIMPIntroToQuantumAI
branch_surface: main
ruleset: 24718913
status:
  canonical_candidate: true
  ci_stabilization: true
  safe_replay_admissible: true
  append_only: true
```

## Purpose

The DITTO KOKOMPI pattern defines a repeatable way to stabilize document-first or course-first repositories under a protected `main` ruleset.

It is called `ditto` because the same CI skeleton can be reused across related repositories without assuming that every repository is already a full Python package.

It is called `kokompi` because the pattern composes minimal checks as a small execution kernel:

```text
checkout -> setup-python -> optional-install -> optional-compile -> optional-pytest -> markdown-readability
```

## Canonical law

```text
CI must be stable before it is strict.
```

That means:

```text
No pyproject.toml? skip package install.
No requirements.txt? skip requirements install.
No Python files? skip compile check.
No test_*.py files? skip pytest.
Markdown files present? require non-empty readability.
```

## Ruleset alignment

The protected branch ruleset should target `main` and may require the stable check name:

```text
ci
```

This check name is intentionally short and stable so it can be added to GitHub branch rulesets without depending on a changing matrix label.

## Safe replay behavior

The pattern does not publish packages, does not require secrets, and does not rewrite source files.

It is suitable for:

- lecture repositories
- document-first teaching material
- gradual Python migration
- protected branch bootstrapping

## Compact canon

```text
DITTO repeats.
KOKOMPI composes.
CI stabilizes.
Ruleset protects.
Main witnesses.
UNUM TENET.
```
