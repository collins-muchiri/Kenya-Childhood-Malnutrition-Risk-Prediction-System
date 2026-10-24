# DECISIONS.md

Stop-and-log register (mission rule 0.11). Each entry: assumption, rationale, reversibility.

## D-001 Audit executed on CPython 3.12.15 via uv, not the CI matrix (3.9-3.11)

- Assumption: Python 3.12 is the mission stack default and the harshest reasonable target.
- Rationale: the 7 test failures are pandas-2.x-on-3.12 issues; auditing on 3.11 would have hidden fewer of them but 3.12 is where the repo must land per Section 2.
- Reversibility: trivial; re-run evidence commands on 3.11 to compare.

## D-002 No Docker/macOS execution locally

- Assumption: sandbox has no docker daemon and no macOS runner.
- Rationale: container/matrix gates are delegated to GitHub Actions as system of record; local absence is disclosed rather than papered over.
- Reversibility: full - CI will produce the authoritative artefacts.

## D-003 Streamlit `/healthz` accepted as the Phase 0 app-health signal

- Assumption: framework healthz proves boot, not dependency health.
- Rationale: sufficient for Phase 0 "does it run"; DoD-compliant /healthz /readyz /livez with real checks is scheduled for P4.
- Reversibility: full.

## D-004 Web dashboard not built locally in Phase 0

- Assumption: npm install/build of the Next.js app exceeds Phase 0 budget; deployed instance (kmal.vercel.app, HTTP 200) is live evidence of buildability at some past commit.
- Rationale: rule 0.12 - cut scope (frontend build), never evidence honesty; the gap is recorded in AUDIT.md D1 row instead of being claimed as verified.
- Reversibility: full - P1/P4 will add the clean-clone gate that builds web/ in CI.

## D-005 Token handling

- Assumption: the GitHub credential is supplied out-of-band and must never appear in outputs (mission token rule).
- Rationale: all gh/git operations use the ambient credential helper; the token is never echoed, written to the repo, or committed. gitleaks/trufflehog gates are scheduled for P1. Owner has been reminded to rotate the credential at mission end.
- Reversibility: n/a (policy).

## D-006 Evidence timestamps use the execution environment clock (2026-10-24 UTC)

- Assumption: evidence must match the machine that produced it.
- Rationale: avoids fabricated dates; logs include the command line in their headers.
- Reversibility: full.
