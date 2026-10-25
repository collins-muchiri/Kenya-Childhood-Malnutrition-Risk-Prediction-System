# AUDIT.md - Phase 0 Forensic Audit

Repo: Kenya-Childhood-Malnutrition-Risk-Prediction-System
Audit date: 2026-10-24 (UTC, execution-environment clock)
Auditor: autonomous agent session (principal-engineer mission), account collins-muchiri
Status of this document: Phase 0 complete for this repo. No production code was changed during the audit.

## 1. Method

All commands were run in this session on a clean clone at `/home/user/audit_ws/Kenya-Childhood-Malnutrition-Risk-Prediction-System` (main @ 6e731bf). Raw outputs are committed verbatim under `docs/evidence/audit-phase0/`:

| Evidence file | Command | Result |
|---|---|---|
| `2026-10-24-install.log` | `uv venv /tmp/venvs/mal --python 3.12` + `uv pip install -e '.[dev]'` | SUCCESS (CPython 3.12.15, editable install) |
| `2026-10-24-tests.log` | `python -m pytest tests/ -v --cov=src --cov=kam_forecast` | 14 passed, 7 failed, coverage 31% |
| `2026-10-24-app-run.log` | `streamlit run app/app.py --server.headless true --server.port 8599` + HTTP GET `/healthz`, `/` | Both endpoints returned HTTP 200 |

Additional live check: `https://kmal.vercel.app` returned HTTP 200 (96,376 bytes) on 2026-10-24.

Environment limits disclosed: the audit sandbox has no Docker daemon and no macOS runner, so container and cross-OS gates could not be executed locally; GitHub Actions is the system of record for those.

## 2. Inventory (machine-derived, see repo-level inventory in PHASE0_SUMMARY)

- Python 5,846 LOC (53 files) under `src/`, `kam_forecast/`, `app/`, plus 4 stray `generate_test_data*.py` scripts at root.
- TypeScript/TSX 4,947 LOC (`web/` Next.js 15 dashboard), JS 112 LOC.
- 14 test files (`tests/`), 1 CI workflow (`.github/workflows/ci.yml`, py3.9/3.10/3.11 matrix).
- 21 markdown docs, 8 tags (v1.0.0..v6.0.0 plus remediation v1.1.0), 4 branches.
- Licence: MIT (`LICENSE`, valid text). GitHub licence detection returns none because the copyright holder is "Community Contributors" - cosmetic, flagged below.
- Authorship (git log emails): 30 x `83084745+collins-muchiri@users.noreply.github.com`, 15 x `z@container`, 4 x `83084745+bucky-ops@users.noreply.github.com`, 2 x `auto@example.com`. See `docs/PROVENANCE.md`.

## 3. Run results (verbatim summaries; full logs in docs/evidence/audit-phase0/)

### 3.1 Install - PASS
Editable install of `kam_forecast` + dev extras on Python 3.12.15 succeeded with zero manual steps.

### 3.2 Tests - FAIL (7 of 21)

Side-effect finding: running pytest modified the tracked file `data/processed/validation_report.csv` in the working tree (observed via `git status` immediately after the run). Tests must not mutate committed artefacts; scheduled for fix in P1 (write to tmp_path).

Failures concentrate in pandas-2.x incompatibilities and data-path assumptions:

- `ValueError: Invalid frequency: M ... Please use 'ME' instead` (pandas >= 2.2 removed the `M` offset alias). Affects `test_data_cleaning`, `test_feature_engineering`, `test_model_training`, `test_validation`.
- `test_data_loading` failures stem from load paths expecting files not present in a clean clone.

Coverage: TOTAL 31% (824 stmts, 568 missed). Core modelling modules (`src/models/predict.py` 16%, `train_model.py` 23%) are barely exercised. Many `src/` subpackages (`alerts`, `dqr`, `governance`, `reporting`, `scenarios`, `system`, `uncertainty`) show 0% - they are never imported by tests.

### 3.3 App run - PASS (with caveat)
Streamlit dashboard boots headless; `/healthz` and `/` return 200. Caveat: Streamlit's `/healthz` is framework-provided, not a real dependency check (DoD requires `/healthz /readyz /livez` with real checks).

### 3.4 Web dashboard - NOT VERIFIED LOCALLY
`web/` (Next.js) was not built in this session (npm install budget). The deployed instance at kmal.vercel.app answers 200, but the clean-clone build path is unproven.

## 4. Gap matrix vs Section 4 Definition of Done

| DoD | State | Evidence | Fix cost |
|---|---|---|---|
| D1 clean-clone gate ubuntu+macos | PARTIAL | install+app pass locally on ubuntu-like sandbox; no CI clean-clone gate; macOS never run | M (CI work) |
| D2 full CI green incl. model-eval/data-contract/evidence-link/reproducibility/security/SBOM gates | ABSENT | ci.yml runs lint+pytest only; pytest currently fails on py3.12 pandas | L |
| D3 coverage >=85% core / >=75% overall | ABSENT | 31% total (tests.log) | L |
| D4 mypy --strict clean, ruff clean | ABSENT | not run in CI as gate; not attempted clean | M |
| D5 every numeric claim resolves to docs/evidence | PARTIAL | docs contain almost no numeric claims post-remediation; evidence dir now seeded by this audit | S |
| D6 mandatory docs set | PARTIAL | README, MODEL_CARD, DPIA, DATA_PROVENANCE, CODE_OF_CONDUCT exist; ARCHITECTURE, EVALUATION, THREAT_MODEL, RUNBOOK, DEPLOYMENT, ADRs, CHANGELOG, SECURITY, SUPPORT missing or scattered as root-level manuals | M |
| D7 adversarial QA suite | ABSENT | no docs/qa/ | L |
| D8 hostile self-review | PARTIAL | PROJECT_REVIEW.md / AUDIT_REPORT.md exist from earlier remediation, not this mission's gate | M |
| D9 SemVer release + GHCR image + SBOM | PARTIAL | tags exist (v1.1.0 latest); no container image, no SBOM | M |
| D10 repo metadata, >=8 topics, CODEOWNERS, dependabot, branch protection | PARTIAL | to verify/set in P1 | S |
| D11 live demo without login wall | PRESENT | kmal.vercel.app HTTP 200 (this session) | - |
| D12 STATUS.md accurate, lie detector resolved | PARTIAL | this document + STATUS.md created in Phase 0 | S |
| D13 15-minute evaluator path | ABSENT | QUICK_START.md exists but not the 4-command/3-screen format | S |
| D14 no theatre | PARTIAL | 4 near-duplicate `generate_test_data*.py` root scripts, `push_to_github.bat`, `debug/` dir, dead `bucky-ops` URLs in pyproject.toml | S |

## 5. Risk register

| ID | Risk | Class | Sev | Remediation |
|---|---|---|---|---|
| R1 | Tests fail on pandas>=2.2 (`'M'` offset) - repo does not build green on modern Python | correctness | P0 | Replace `M` with `ME` in src+tests, pin pandas floor, fix in P1 |
| R2 | Coverage 31%; uncertainty/governance/scoring modules untested | correctness | P0 | Test-alongside rewrite in P3/P5 |
| R3 | Synthetic vs real data paths: `data/` contains generated test data; README says "WHO + UNICEF + DHIS2 indicators" | data honesty (0.5) | P0 | Label all synthetic artefacts SYNTHETIC in filename+schema+UI; separate real/synthetic loaders; DATA.md data cards |
| R4 | No time-aware CV enforced in code; random splits possible via train_model.py | domain harm | P1 | Rolling-origin, geo-blocked CV as the only splitter; test that random split raises |
| R5 | Individual-level data risk: generators fabricate child-like records | privacy/legal (Kenya DPA) | P1 | Aggregate-only default; DPIA exists - enforce in schema; delete realistic-looking synthetic names |
| R6 | Dead `bucky-ops` URLs in pyproject.toml (3 occurrences) | hygiene | P2 | Point to collins-muchiri in P1 |
| R7 | Root-level script sprawl (4 test-data generators, .bat pusher) | hygiene | P2 | Consolidate under `scripts/` or delete in P1 |
| R8 | Streamlit `/healthz` is not a dependency check | ops | P2 | Real health endpoints in P4 service layer |

No P0 security-secret findings: no credentials in tree (verified by grep during earlier remediation; re-verify with gitleaks in P1).

## 6. Lie detector (claims in README/docs vs runnable artefacts)

| CLAIM | EVIDENCE | VERDICT |
|---|---|---|
| "Live URL: https://kmal.vercel.app" | HTTP 200, 96,376 bytes, fetched 2026-10-24 (this audit) | SUPPORTED |
| "Random Forest model trained on WHO + UNICEF + DHIS2 indicators" | `src/models/train_model.py` exists; no committed trained artefact or metrics JSON; training data in repo is generated | NOT BACKED - retrain with provenance in P3/P5 or reword |
| "WHO DQR-compliant data quality validation and scoring" | `src/dqr/`, `src/validation/validate_data.py` exist; 0-29% coverage; no DQ report artefact committed | PARTIAL - code exists, compliance unproven |
| "Uncertainty quantification with confidence intervals" | `src/uncertainty/` present but 0% test coverage; no reliability/ECE artefact | NOT BACKED yet - P5 |
| "Quality-weighted training" | `src/models/train_model_weighted.py` present, 0% coverage, never imported by tests | PARTIAL |
| "Fully responsive (mobile-first)" web dashboard | Not verified (no Playwright/axe gate) | UNVERIFIED - P4 |
| "Digital Public Good" | No DPG registry listing evidenced | UNVERIFIED CLAIM - reword to "intended as" or register |
| Badge "python 3.9+" | CI matrix is 3.9-3.11; tests currently FAIL on 3.12 (pandas) | PARTIAL - true only after R1 fix |

## 7. Sequenced work plan (rough effort: S < 2h, M = half-day, L = 1-2 days)

1. P1 Foundations (M): fix R1 pandas `ME`, R6 URLs, R7 script sprawl; uv lockfile; Makefile contract; CI rewrite (3.11+3.12 x ubuntu+macos, lint/type/test/security/evidence-link/clean-clone skeletons); docs skeleton; .env.example; gitleaks+trufflehog; repo metadata + branch protection. PR.
2. P2 Data layer (M-L): `data/manifest.yaml` with licences/retrieval dates/checksums; SYNTHETIC labelling; pandera contracts; DQ rules as executable checks with report artefacts; offline-safe `make data`. PR.
3. P3 Core engine (L): WHO z-score implementation (WHZ/HAZ/WFA + plausibility flags) with property tests; time-aware CV only; baselines (window-average, persistence); gradient boosting; model registry; seeds. PR.
4. P4 Service/API + UI (L): FastAPI service with real /healthz /readyz /livez, OpenAPI export, typed client; Next.js wired to API with SYNTHETIC badges; Playwright + axe. PR.
5. P5 Evaluation (M-L): MAE/RMSE by lead month vs baselines, AUC-PR, Brier/ECE, interval coverage, per-county error parity; metrics JSON to docs/evidence/metrics/; model-eval + reproducibility gates; EVALUATION.md; update MODEL_CARD. PR.
6. P6 Hardening (M): bandit/semgrep/pip-audit/trivy; adversarial QA suite (docs/qa/); drift monitors + kill switch; THREAT_MODEL.md; PRIVACY/COMPLIANCE docs. PR.
7. P7 Presentation (M): 15-minute evaluator path, market pack, screenshots from real product, social preview, release + GHCR + SBOM, CHANGELOG. PR.
8. P8 Self-review (S-M): hostile-reviewer pass, docs/review/REVIEW.md, close P0/P1. Final PR.
