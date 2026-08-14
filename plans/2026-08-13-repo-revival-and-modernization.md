# Repo Revival & Modernization Plan

**Status:** Complete — v0.1.0 released 2026-08-14 (https://pypi.org/project/absynthe/0.1.0/).
**Scope:** Infrastructure/tooling revival only. One exception (see decisions table). No other
behavioral/logic changes, no new features.

## Why

absynthe (last released v0.0.3, `e2dcc97`) predates GitHub Actions, targets Python 3.6, pins
`scipy==1.2.1`, and was published to PyPI/TestPyPI by hand under git-flow. This plan brings packaging,
testing, CI, and release process to current best practice.

## Decisions

| Area | Decision | Why |
|---|---|---|
| Branch workflow | GitHub flow: single `main` (renamed from `master`), short-lived `release/vX.Y.Z` branches. Git-flow retired. | Matches modern GH Actions release automation; simpler than develop/master/hotfix. |
| Python support | 3.10–3.13, CI matrix. | Oldest to newest actively maintained CPython at time of revival. |
| Build backend | `hatchling` via `pyproject.toml`. | Modern, minimal config. |
| PyPI auth | Trusted Publishing (OIDC), no stored secret. | Eliminates long-lived API tokens. |
| TestPyPI | Not used. | Was only ever a learning aid for the manual upload flow; unneeded now that publishing is automated and gated behind manual approval. |
| CI OS matrix | `ubuntu-latest` only. | Pure-Python library, no OS-specific code. |
| Test runner | `pytest` (existing `unittest.TestCase` classes run unchanged). | Coverage tooling, community convention. |
| Test directory | Rename `test/` → `tests/`. | Pytest/community convention; purely structural. |
| Lint/type gates | `ruff` (lint+format) + `mypy` as CI gates. | Catch issues from the Python 3.6→3.10-3.13 jump. |
| `numpy` dependency | Drop. | Declared (`==1.16.4`) but never imported; only `scipy.stats.binom` is used. |
| `scipy` version | Minimum-version bound `scipy>=1.14.1`, not an exact pin. | 1.14 is scipy's first release supporting Python 3.10–3.13 in one range (`>=3.10,<3.14`); 1.14.1 is the first patch with published 3.13 wheels. Exact pins on a library cause downstream resolution conflicts. |
| `develop` branch | Merge into `main` (Phase 0). | Contains real, tested, unreleased work (`MonospaceSimple` class, `Behavior` API cleanup). Verified: full `unittest` suite (24 tests) passes on `develop` under Python 3.12.10 / scipy 1.17.1. |
| Stray/stale branches | Delete `U2qtFrKTvffR2hwP`, `dependabot/pip/numpy-1.22.0`, `dependabot/pip/scipy-1.10.0`, `develop` (post-merge). | Dead weight from git-flow/Dependabot era. |
| `absynthe/__init__.py` re-exports | Leave as-is (all commented out). | Revival ≠ public API change. |
| `from __future__ import ...` statements | Remove via `ruff --fix` (rule UP010). | No-ops under Python 3.10+; pure lint cleanup, not a logic change. |
| `examples/01_generateSimpleBehavior.py` | Fix the stale `MonospaceInterleaving(wSessionID)` call (constructor arg moved to `.synthesize()` on `develop`, but this file was never updated — currently raises `TypeError`). | Only code edit in this plan beyond the `develop` merge itself; required to unbreak a shipped example. |
| Docs site | Out of scope; `README.md` remains sole documentation. | Keeps revival tightly scoped. |
| Revival version | `v0.1.0`. | Signals a real milestone (revival + merged feature work), still pre-1.0. |

## Phases

### Phase 0 — Branch & history cleanup
1. Merge `origin/develop` into `master`.
2. Fix `examples/01_generateSimpleBehavior.py` (see Decisions).
3. Rename `master` → `main` (local + push + GitHub default branch).
4. Delete branches: `U2qtFrKTvffR2hwP`, `dependabot/pip/numpy-1.22.0`, `dependabot/pip/scipy-1.10.0`, `develop`.
5. Update Travis badge / `master`-branch references in `README.md`.

### Phase 1 — Packaging modernization
1. Add `pyproject.toml`, `hatchling` build backend.
2. Move metadata from `setup.py` (name, url, license, author, description, classifiers, `python_requires`).
3. `[tool.hatch.version]` reads `VERSION` from `absynthe/version.py` — single source of truth.
4. `requires-python = ">=3.10"`, updated classifiers.
5. Drop `numpy`; `scipy>=1.14.1`.
6. Delete `setup.py`, `requirements.txt`.

### Phase 2 — Test suite modernization
1. Rename `test/` → `tests/`.
2. Add `pytest`, `pytest-cov` as dev dependencies.
3. Add `[tool.pytest.ini_options]`.
4. Confirm existing tests collect/pass unchanged under `pytest`.

### Phase 3 — Lint & type-check tooling
1. Add `[tool.ruff]`; run `ruff check`.
2. Add `[tool.mypy]`; run `mypy absynthe/`.
3. Auto-fix pure lint/format findings only. Any semantic finding (real type error) is flagged before touching it, not silently fixed.

### Phase 4 — CI (GitHub Actions)
1. `.github/workflows/ci.yml`: push/PR to `main` and `release/*`; matrix `python-version: ["3.10","3.11","3.12","3.13"]` on `ubuntu-latest`; steps: checkout → install `uv` → `uv sync` → `ruff check` → `mypy absynthe/` → `pytest --cov=absynthe`.
2. Delete `.travis.yml`.
3. Replace Travis badge with GitHub Actions badge in `README.md`.

### Phase 5 — Release automation
1. `.github/workflows/publish.yml`: triggers on GitHub Release `published` event, publishes to PyPI via `pypa/gh-action-pypi-publish` (OIDC), gated behind the `pypi` environment (manual reviewer approval).
2. Requires manual setup below to be complete before first use.

### Phase 6 — Documentation touch-ups
1. `README.md` Installation: drop the "developed with Python 3.6.*" caveat; state 3.10–3.13 support.
2. `README.md` Release Notes: add `### Major changes in v0.1.0` — packaging/CI/release modernization, dropped Python <3.10 support, merged `MonospaceSimple` class, `withSessionID` moved to `.synthesize()` (breaking change).
3. Carry over `develop`'s already-updated Usage example.

### Phase 7 — Version bump & first revival release
1. Bump `VERSION` in `absynthe/version.py` to `0.1.0`.
2. Follow `CLAUDE.md`'s Release Process: `release/v0.1.0` → PR into `main` → merge → tag `v0.1.0` → `gh release create` → verify `publish.yml` runs and, after manual approval, the package lands on PyPI.

## Manual Setup (GitHub / PyPI portals)

Required before Phase 5 can work; cannot be done via git/CLI:

1. **PyPI (pypi.org):** register a Trusted Publisher for `chaturv3di/absynthe` — workflow `publish.yml`, environment `pypi`.
2. **GitHub repo Settings → Environments:** create `pypi`, add yourself as required reviewer (manual approval gate).
3. **GitHub repo Settings → Branches:** rename default branch `master` → `main`.

## Non-goals

- No changes to graph/behavior/node algorithm logic.
- No mkdocs/docs site.
- No src-layout restructuring.
- No new features beyond what's already on `develop`.
- No pre-commit hooks or tooling beyond `ruff`/`mypy`/`pytest`.
