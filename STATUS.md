# STATUS.md

Last updated: 2026-10-24 (UTC) by Phase 0 audit session.

## Where this repo stands

- Phase 0 (forensic audit): COMPLETE. See `AUDIT.md`, `docs/PROVENANCE.md`, evidence in `docs/evidence/audit-phase0/`.
- Phases P1-P8 (mission Section 5): NOT STARTED.
- Honest completion vs Section 4 Definition of Done: ~30% (D11 live demo present; D5/D6/D9/D10/D12 partial; D2/D3/D4/D7/D13 absent or failing).

## What actually runs right now (verified this session)

| Command | Result |
|---|---|
| `uv venv --python 3.12 && uv pip install -e '.[dev]'` | PASS |
| `pytest tests/ --cov=src --cov=kam_forecast` | 14 passed, 7 FAILED (pandas>=2.2 `'M'` offset removal), coverage 31% |
| `streamlit run app/app.py --server.headless true` + GET /healthz | PASS (HTTP 200) |
| GET https://kmal.vercel.app | PASS (HTTP 200) |

## Known-broken

1. Tests fail on modern pandas (fix: `M` -> `ME` offsets). P1, first commit.
2. Coverage 31% vs required 85/75.
3. No Makefile contract, no uv.lock, CI matrix is py3.9-3.11 ubuntu-only, no security/evidence/clean-clone gates.
4. Dead `bucky-ops` URLs in pyproject.toml.
5. Synthetic data not labelled SYNTHETIC in filenames/schema/UI (rule 0.5 gap).

## Exact next commands for the next operator

```bash
git clone https://github.com/collins-muchiri/Kenya-Childhood-Malnutrition-Risk-Prediction-System
cd Kenya-Childhood-Malnutrition-Risk-Prediction-System
uv venv --python 3.12 && uv pip install -e '.[dev]'
uv run pytest tests/ -x            # reproduce the 7 failures
# then start P1 per AUDIT.md section 7
```

## Checkpoint log

- 2026-10-24 Phase 0: install/tests/app-run executed and captured verbatim; AUDIT.md + PROVENANCE.md + STATUS.md + DECISIONS.md committed on branch `audit/phase-0`; PR opened. Nothing merged to main yet.
