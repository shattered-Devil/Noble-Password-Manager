# Security Model

This document describes the cryptographic and local-storage behavior of Noble
Password Manager `v0.0.4` as implemented in the release-preparation source.
It is a technical description, not a claim of formal security certification.

## Vault encryption

The vault uses the `cryptography` Python package's **Fernet** construction for
authenticated encryption.

The application derives the Fernet key from the user-supplied master password
using:

```text
KDF:        PBKDF2-HMAC-SHA256
Iterations: 600,000
Output:     32 bytes, then URL-safe Base64 encoding for Fernet
Salt:       16 random bytes per vault
```

The 16-byte salt is written in plaintext at the beginning of the vault file.
It is required for key derivation but is not itself a secret.

The remaining bytes are the Fernet token containing the encrypted JSON vault.

## Password handling

The master password is not stored in the vault file. While the vault is
unlocked, the current application keeps the master password in process memory
to support normal read/write operations. Locking the vault removes the Python
reference used by the application, but Python does not provide a guaranteed
cryptographic memory-zeroization primitive for ordinary string objects.

## Failed-attempt lockout

The current UI records failed-attempt counters and a lockout timestamp in the
user configuration file. This is a **local user-interface rate limit**, not a
cryptographic protection against an attacker who can modify application files.
An attacker with local write access could alter that configuration.

The primary protection against offline guessing is therefore the strength of
the user's master password and the cost of PBKDF2.

## Clipboard behavior

When a credential is copied, the application places it on the system clipboard
and automatically attempts to clear it after a short timeout. Clipboard data
can still be exposed to other software while it remains on the system
clipboard, so users should avoid copying credentials on untrusted machines.

## Backups

Vault backups are copies of the encrypted vault file. A backup is not decrypted
by the application during export. Anyone obtaining a backup still needs the
master password to decrypt a valid vault, but a weak master password makes
offline password guessing more practical.

Keep backups in a location that is itself appropriately protected.

## Threats outside the current model

No local password manager can fully protect data when the operating system or
user session is already compromised. This implementation does not claim to
protect against:

- malware or keyloggers running with access to the user session;
- an attacker reading process memory while the vault is unlocked;
- compromised system components or administrator-level malware;
- malicious software reading the system clipboard during a copy operation;
- weak or reused master passwords; or
- data recovery from filesystems, backups, snapshots, or forensic tooling after
  deletion.

## Cryptographic disclosure

The cryptographic algorithms and parameters are intentionally documented.
Security should not depend on hiding algorithm names. The application's actual
secret material (passwords, derived keys, tokens, and user vault contents) is
not published.

## Audit status

Noble Password Manager `v0.0.4` has not undergone an independent professional
cryptographic or security audit. Do not interpret the use of established
cryptographic primitives as proof that the complete application is secure.
