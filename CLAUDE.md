# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

This describes the repo's actual workflow (`pyproject.toml`, `uv`, `ruff`, `mypy`, `pytest`, GitHub
Actions) as of the v0.1.0 revival release. See
[`plans/2026-08-13-repo-revival-and-modernization.md`](./plans/2026-08-13-repo-revival-and-modernization.md)
for how it got there.

## Project Overview

**absynthe** ("A (Branching) Synthesizer") is a small Python library for synthesizing log-like
*behaviors* by traversing configurable control-flow graphs (CFGs) — trees, DAGs, and directed cyclic
graphs with loops. It's used to generate labeled, ground-truth test data for log analysis and anomaly
detection tooling, including interleaved logs from multiple graphs traversed simultaneously.

### Architecture
Reference architecture of the project, subject to updates.

```
pyproject.toml                 # Package metadata, build backend (hatchling), dependencies, tool config
absynthe/
├── __init__.py                # Top-level package init
├── version.py                  # VERSION string — single source of truth for the release version
│                                # (pyproject.toml reads it via hatchling's dynamic versioning)
├── graph_builder.py            # GraphBuilder ABC + TreeBuilder, DAGBuilder, DCGBuilder
├── behavior.py                  # Behavior ABC + concrete behaviors (e.g. MonospaceInterleaving, MonospaceSimple)
└── cfg/
    ├── __init__.py              # Re-exports: Node, UniformNode, BinomialNode, LoggerNode, SimpleLoggerNode, Graph
    ├── node.py                   # Node ABC + UniformNode, BinomialNode (successor-selection distributions)
    ├── logger_node.py            # LoggerNode ABC + SimpleLoggerNode (log message emission)
    ├── graph.py                   # Graph class — holds nodes/edges, supports traversal
    └── utils.py                    # Utils — random Node construction from registered concrete Node types
tests/                          # All test cases go here (pytest; existing unittest.TestCase classes run fine under it)
├── test_behavior.py
├── test_graph_builder.py
└── cfg/
    ├── test_Node.py
    ├── test_UniformNode.py
    ├── test_BinomialNode.py
    ├── test_Graph.py
    └── test_logger_node.py
examples/                       # Runnable usage examples (01 tree, 02 tree+DCG, 03 DCG with loops)
imgs/                            # Diagrams referenced from README.md
```

**`absynthe/__init__.py` has no top-level re-exports — this is intentional.** Users import via
`from absynthe.graph_builder import TreeBuilder` / `from absynthe.behavior import
MonospaceInterleaving`, not `import absynthe`. This deliberately follows the scikit-learn-style
convention of deep, module-qualified imports rather than a flat top-level namespace. Do not add
re-exports to `absynthe/__init__.py` to "fix" this.

## Development Instructions
Strictly follow the instructions in the relevant section(s).

### Common Instructions
These instructions apply regardless of the nature of the implementation task, whether it's implementing
a plan, an ad-hoc feature, a bug-fix, or anything else.

0. Feel free to use agents/teammates for steps that can be executed in parallel.
1. Always double check your work. Create a checklist of all the claims you make and tick off claims that
   you are able to verify.
2. Focus only on the task at hand. Do not create additional scope of work.
3. Always validate the correctness of the implementation using a test case.
4. CRITICAL: Never make any assumptions. Ask clarifying questions. Make sure you have complete
   information and are aligned with me on the exact requirements and next steps.
5. Use the following testing strategy and feel free to use agents/teammates for this.
    1. First look for existing test(s) that can be used to validate the implementation.
    2. Implement new test case(s) if no existing ones suffice.
    3. Execute the test(s) using `pytest` and leverage `pytest-cov` to ensure test coverage.
    4. Run `ruff check` and `mypy absynthe/` — both are CI gates (see `.github/workflows/ci.yml`), not
       optional.
    5. If all the test cases pass, create a git commit automatically with a brief description of changes.
    6. If any tests fail, think deeply about the root cause and the amount of change needed to fix it.
    7. Automatically debug the code if the debugging is limited to the most recent code changes.
    8. If debugging requires changes to code/files which are outside of the scope of the current
       task/context, provide a justification for the proposed changes and ask for permission BEFORE
       making those bugfixes.
6. If a new Python package is required, then add the dependency in `pyproject.toml`.
    1. Install any dependencies ONLY USING `uv pip install <package>`.
    2. It is safe to assume that `uv` is already available.
7. Use `ruff` for formatting and linting.
8. When managing context throughout implementation, follow these principles:
    1. Always preserve the current task description and checklist.
    2. Keep the full list of modified files.
    3. Retain any active test commands and their results.
    4. Summarize deep debugging logs but keep key decisions.

### Implementing Plans
Strictly follow the instructions below.
0. Always expect a path to a plan document to be provided whenever asked to implement a plan.
    1. Plan documents reside in the [plans folder](./plans/); an exact plan document will be pointed out.
    2. Expect one plan document at a time.
    3. Always stay consistent with the plan document which is provided.
1. Break down each class and each feature into multiple sub-features.
    1. The definition of a sub-feature is a minimal functionality that can be tested.
    2. From the perspective of a class, each method could be a sub-feature. However, it is possible that
       some methods can also be implemented incrementally with each incremental addition being a
       sub-feature.
    3. Add a package dependency in the `pyproject.toml` file only if the current sub-feature requires it.
2. Think about sub-features critically before starting the implementation.
    1. Create a logical order of (sub-)features to implement. If A depends on B, then implement B first
       and then A.
    2. Implement the sub-feature which is next in line.
    3. Follow the testing strategy defined above to test the sub-feature.
3. After each sub-feature implementation, proactively manage context to stay focused.

## Release Process
This repo uses GitHub flow (single `main` branch), not git-flow. When creating a release:

  1. Create a `release/vX.Y.Z` branch from `main`.
  2. Commit the version bump — update `VERSION` in `absynthe/version.py` only; `pyproject.toml` reads
     the version dynamically from that file via hatchling, so it does not need a separate edit.
  3. In `README.md`'s `## Release Notes` section: add a new `### Major changes in vX.Y.Z` entry
     summarizing what changed since the last release.
  4. Push the branch and open a PR into `main`.
  5. Wait for PR approval and merge — do NOT proceed until the PR is merged.
  6. After merge, create an annotated tag on `main`: `git tag -a vX.Y.Z -m "Release vX.Y.Z"`.
  7. Push the tag: `git push origin vX.Y.Z`.
  8. Create a GitHub release using `gh release create`.
  9. Publishing the GitHub release automatically triggers the `publish.yml` GitHub Actions workflow,
     which builds the package (hatchling) and uploads it to PyPI via Trusted Publishing (OIDC). A
     reviewer must approve the deployment in the GitHub Actions UI (under the `pypi` environment) before
     the upload proceeds. Monitor progress in the repository's Actions tab.

  Never commit version bumps or release prep directly to `main`.

## Common Commands
- Running tests: `pytest` (add `--cov=absynthe` for coverage)
- Dependency management: `uv`
- Linting and formatting: `ruff check` / `ruff format`
- Type checking: `mypy absynthe/`
- Building/packaging: `hatchling` (via `uv build`)
