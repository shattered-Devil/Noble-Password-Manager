# Noble Password Manager v0.0.4 Beta

## Highlights

- Installed-build path/resource handling was improved.
- Additional interface themes were added.
- Minor bugs and UI glitches were fixed.

## Before installing

This is a **beta** release. Back up any existing encrypted vault before making
changes to your installation.

## Downloads

Use the GitHub release assets:

- `NoblePasswordManager-Setup-0.0.4.exe` — recommended for normal installation.
- `NoblePasswordManager-Portable-0.0.4.zip` — portable package.
- `SHA256SUMS.txt` — SHA-256 hashes for released files.

## Security note

The application uses Fernet authenticated encryption and PBKDF2-HMAC-SHA256
with 600,000 iterations and a per-vault random 16-byte salt. See
`docs/SECURITY_MODEL.md`.
