# Noble Password Manager

Noble Password Manager (NPM) is a Offine local Windows password manager designed to keep credential data in an encrypted vault stored on the user's computer.

> **Status:** Beta — `v0.0.4`
>
> This project is closed-source. The public repository contains release information and downloadable binaries; the application source code is maintained separately in a private repository.

## Download

[Download the latest release]

For a beta release, download the installer unless you specifically need the portable package.

## Current release

### v0.0.4 Beta

- Fixed application path/resource handling for installed builds.
- Added additional interface themes.
- Fixed minor bugs and UI glitches.

See [CHANGELOG.md](CHANGELOG.md) for release notes.

## Features

- Local encrypted password vault
- Master-password unlock
- Password generator
- Password-strength indicator
- Categories and favorites
- Search
- Encrypted vault backup/export
- Encrypted vault import
- Master-password change
- Automatic inactivity lock
- English and Farsi interface
- Multiple appearance themes

## Security

Noble Password Manager currently uses **Fernet** authenticated encryption and **PBKDF2-HMAC-SHA256 with 600,000 iterations** to derive a 32-byte Fernet key from the master password. A random 16-byte salt is stored with each vault file; the salt is not a secret.

The cryptographic design is documented in [docs/SECURITY_MODEL.md](docs/SECURITY_MODEL.md).

**Important:** this beta has not undergone an independent professional security audit. A password manager should be treated as security-sensitive software, and users should keep independent backups of important encrypted vaults.

## Storage

On Windows, the application stores its vault and configuration under the user's `%APPDATA%` directory:

```text
%APPDATA%\NoblePasswordManager\
```

The encrypted vault file is:

```text
noble_vault.enc
```

## License

Noble Password Manager is proprietary software. See [LICENSE.txt](LICENSE.txt).

## Security reports

Please do **not** report security vulnerabilities in public Issues or Discussions. See [SECURITY.md](SECURITY.md) for the reporting process.

## Disclaimer

Noble Password Manager is provided as beta software. Use it at your own risk and maintain independent backups of your encrypted vault.

