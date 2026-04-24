# Changelog

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
