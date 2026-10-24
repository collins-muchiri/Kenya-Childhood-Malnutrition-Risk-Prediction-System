# PROVENANCE

## Origin

- Not a fork. `gh repo view --json isFork,parent` returns `false / none` (checked 2026-10-24).
- Owned by `collins-muchiri`. The account was formerly named `bucky-ops`; GitHub noreply addresses for both names appear in history.

## Authorship (git log email census, 51 commits on main at audit time)

| Email | Commits | Interpretation |
|---|---|---|
| `83084745+collins-muchiri@users.noreply.github.com` | 30 | Owner, current account name |
| `z@container` | 15 | Commits authored inside a tool/container environment (AI-assisted session); committer identity not a real person's mailbox |
| `83084745+bucky-ops@users.noreply.github.com` | 4 | Owner, former account name |
| `auto@example.com` | 2 | Automated/tool-generated commits; placeholder identity |

Disclosure: a substantial share of history was produced by AI-assisted tooling under the owner's direction, including commits authored from container identities (`z@container`, `auto@example.com`). This is recorded here per mission integrity rule 0.1/0.9 so no reader mistakes the commit census for 51 distinct human work sessions.

## Prior-name artefacts

- `pyproject.toml` still contains 3 `https://github.com/bucky-ops/...` URLs (dead; the account was renamed). Scheduled for fix in P1. All README/doc occurrences were purged in the 2026-10-24 remediation.
- Releases v4.0.0-v6.0.0 predate remediation; release notes may reference the old branding. Releases are immutable history and are not rewritten (rule 0.8); v1.1.0 (latest) supersedes them and says so.

## Licence

- MIT, `LICENSE` present, copyright holder "Community Contributors" (2024). Compatible with all data sources currently planned (KDHS public aggregates, CHIRPS, WorldPop: see DATA_PROVENANCE.md and future DATA.md). GitHub's licence detector does not badge the repo because the holder string is non-standard; acceptable, no change needed.

## Third-party code

- No vendored third-party source trees detected. Dependencies are declared in `pyproject.toml`/`requirements.txt` (pandas, numpy, scikit-learn, matplotlib, seaborn, streamlit, reportlab, python-pptx, dotenv, openpyxl, xlrd) - all permissive licences. A `licensecheck`/pip licence policy gate is scheduled for P1 CI.

## Data

- See `DATA_PROVENANCE.md` (existing) and the planned `DATA.md` data cards. As of this audit, data under `data/` is generated test data, NOT KDHS microdata. No individual-level KDHS data has ever been committed (rule 0.5 respected). Synthetic labelling enforcement is a P2 task.
