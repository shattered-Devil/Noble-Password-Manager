# Security Policy

Noble Password Manager is security-sensitive software. Thank you for
reporting vulnerabilities responsibly.

## Supported version

| Version | Security support |
| --- | --- |
| `0.0.4` Beta | Best-effort security fixes |

Older versions may no longer receive security fixes.

## Reporting a vulnerability

**Do not open a public GitHub Issue or Discussion for a security vulnerability.**

Use GitHub's private vulnerability reporting / Security Advisory mechanism for
this repository when it is enabled. If private reporting is not available,
contact the project maintainer through the private contact method listed on the
maintainer's GitHub profile.

Please include:

- Noble Password Manager version
- Windows version
- A clear description of the issue
- Reproduction steps, where safe
- Security impact or affected component
- Screenshots or logs only when they contain no passwords, vault contents,
  tokens, or other sensitive information

Never send your real vault file or master password as part of a report.

## Responsible disclosure

Please allow reasonable time for investigation and a fix before publicly
sharing technical details of a vulnerability.

## Security scope

The security model currently focuses on protection of locally stored vault data
when the attacker has access to the encrypted vault file but does not already
control the user's unlocked application session or operating system.

See `SECURITY_MODEL.md` for implementation details and limitations.
