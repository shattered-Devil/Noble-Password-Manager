# Changelog

All notable changes to Noble Password Manager are documented here.

## [0.0.4] - Beta

### Added

- Additional application interface themes.

### Fixed

- Application path/resource handling for installed builds.
- Minor bugs and UI glitches.

### Security / release notes

- The application continues to use Fernet authenticated encryption with
  PBKDF2-HMAC-SHA256 (600,000 iterations) and a per-vault random salt.
- This release should be treated as beta software and has not been presented as
  independently audited security software.
