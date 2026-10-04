# Security Policy

## Supported Versions

Security fixes are applied to the current default branch. Archived versions are
not patched.

## Reporting a Vulnerability

**Please do not open a public issue for security problems.**

Use GitHub's private reporting channel:
**Security → Report a vulnerability** (https://github.com/morphagent-textbook/security/advisories/new),
or contact the maintainer directly.

Please include:

- what the issue is and which component is affected
- steps to reproduce, or a proof-of-concept
- the impact you believe it has

## Response

A human-readable acknowledgement within a few business days, best effort.
Triage and a fix timeline depend on severity; no SLA is promised. Confidentiality
is maintained for reporters throughout.

## Scope

This repository is developer tooling that runs locally with your own API keys. Reports about dependencies with a published CVE
are welcome and will be tracked; issues in upstream services are out of scope.

Keys are read from the environment and never committed; a report that a key was committed is in scope.
