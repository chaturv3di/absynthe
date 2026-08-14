# Changelog

All notable changes to this project are documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/). This project is
still pre-1.0 (alpha), so breaking changes may occur in minor releases.

## [0.1.0] - 2026-08-14

### Added
- New `MonospaceSimple` behavior class.

### Changed
- Repo revival and modernization: packaging migrated from `setup.py` to `pyproject.toml`
  (`hatchling`), dependency management via `uv`, `ruff` for linting/formatting, `mypy` for type
  checking, `pytest` for tests, GitHub Actions for CI, and a Trusted Publishing (OIDC) release
  flow to PyPI — replacing the old, manual `twine upload` process and Travis CI.
- **Breaking:** `withSessionID` moved from `MonospaceInterleaving`'s constructor to its
  `synthesize()` method.

### Removed
- Dropped support for `Python < 3.10`; tested against 3.10–3.13.
- Dropped the unused `numpy` dependency; `scipy` is now the only runtime dependency.

## [0.0.3] - 2019-06-24

### Fixed
- Added the missing `requirements.txt` reference to `setup.py`.

## [0.0.2] - 2019-06-24

### Added
- New graph builders, `DAGBuilder` and `DCGBuilder`, adding skip-level edges and loops
  respectively.
- New node type, `BinomialNode`, using the binomial distribution to select successors.
- `Utils` class in `absynthe.cfg.utils` for constructing a random concrete `Node`.

## [0.0.1] - 2019-06-06

### Added
- Initial release.

[0.1.0]: https://github.com/chaturv3di/absynthe/compare/v0.0.3...v0.1.0
[0.0.3]: https://github.com/chaturv3di/absynthe/compare/v0.0.2...v0.0.3
[0.0.2]: https://github.com/chaturv3di/absynthe/compare/v0.0.1...v0.0.2
[0.0.1]: https://github.com/chaturv3di/absynthe/releases/tag/v0.0.1
