# Changelog

## [0.1.1] - 2026-04-24

### Changed
- Official package name changed to `ftw-securify` on PyPI to avoid naming conflicts.
- Updated `project.optional-dependencies` in `pyproject.toml` to use the correct package name for self-referencing extras.

### Fixed
- Fixed a circular dependency issue where the package tried to install its own dev-extras under the old name.

## [0.1.0] - 2026-04-24
### Added
- **First Official Release**: Transitioned from experimental to the first stable minor version.
- **Python 3.15 Support**: Verified compatibility across Linux, Windows, and macOS via GitHub Actions.
- **CI/CD Integration**: Full automation for testing (Tox) and deployment (PyPI/TestPyPI).
- **TTY Security**: Added `require_terminal` check to `PasswordDoubleCheck` to enforce interactive usage.
- **Bot Protection**: Implemented minimum time delay logic to prevent automated inputs.
- **Documentation**: Comprehensive guides and technical notes on TTY handling in automated environments.

### Changed
- Refined exception hierarchy for clearer error handling.
- Updated metadata to reflect 'Development Status 4 - Beta'.

## [0.0.1] - 2026-04-21
### Added
- **Initial Project Structure**: Base implementation of `PasswordDoubleCheck` and exceptions.
- **Version Automation**: Established as the baseline version for `setuptools-scm` to enable tag-based versioning.
