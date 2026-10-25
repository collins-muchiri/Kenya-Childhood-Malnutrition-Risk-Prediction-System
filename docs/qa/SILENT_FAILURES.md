# SILENT_FAILURES.md - grep sweep with dispositions

Repo: Kenya-Childhood-Malnutrition-Risk-Prediction-System
Sweep date: 2026-10-25 (sandbox clock, UTC). Raw output: `docs/qa/artifacts/sweep_raw.md`.
Command class: `rg -n <pattern>` over tracked source (exclusions: node_modules, docs/qa, logs).

| # | Pattern class | Hits | Disposition |
|---|---|---|---|
| 1 | `\|\| true`, `set +e`, `continue-on-error`, `allow_failure`, `--no-verify` | 1 | The 1 hit was this doc's own pattern list (sweep_raw). CI contains no continue-on-error/allow_failure. Clean. |
| 2 | bare `except:`, `contextlib.suppress`, `soft_fail`, `best_effort`, `ignore_errors` | 0 | Clean. |
| 3 | `except Exception` | 24 | All 24 dispositioned: (a) 5 CLI `__main__` boundaries now `logger.exception(...)` + `sys.exit(1)` (non-zero propagation kept); (b) 3 Streamlit UI loaders log full traceback + surface `st.error` + return documented None/empty sentinel that callers check; (c) debug scripts log traceback + return False consumed by runner; (d) `train_model.git_hash` narrowed to `(OSError, subprocess.SubprocessError)`; (e) `system_health_check` CSV probe narrowed to `(OSError, ValueError)` - this previously masked a real F821 NameError (`pd` not imported), fixed; (f) health-check module-import aggregator keeps Exception by design (collecting failures is its function) and now logs; (g) alerts email path narrowed to `(KeyError, TypeError, ValueError)` + re-raise; loop in `run_alerts` continues per-alert but exits non-zero if any failed; (h) test_configuration try/except-fail anti-pattern removed (direct call + effect assertion). |
| 4 | unobserved async/thread work | 1 | `system_launcher.launch_dashboards` threads: `subprocess.run(..., check=False)` now records and prints non-zero return codes (was: exit code discarded, PLW1510). |
| 5 | `seed=` / `random_state` | 10 | Model training uses `random_state` from config `MODEL_PARAMS` - reproducibility seeds declared in config, not test-tuned luck. Tests use fixed synthetic frames. Disposition: legitimate; documented here. |
| 6 | `catch {}`, `@ts-ignore`, `eslint-disable` (web/) | 0 | Clean (eslint config sets warnings, not disables). |
| 7 | `dropna(`, `drop_duplicates(`, `errors="coerce"` | 5+2 | `clean_data.py:72 dropna(subset=[target])`: standard supervised-learning practice (rows without target cannot train); validation module independently reports missing percentages so volume loss is visible, not silent. `build_features.py:86 dropna()`: post-lag NaN drop, same visibility. `errors="coerce"` (load_data, data_quality_app): malformed dates become NaT and are counted by validation's missing-data check. Disposition: legitimate, visible downstream. |
| 8 | `if df.empty` / `len(..)==0` guards | 12 | Reviewed: guards display UI messages or raise; none returns fake success. The one real silent-success defect found: `run_test_pipeline.py` caught pipeline exceptions, printed a traceback, and exited 0. FIXED: now `raise SystemExit(1)`. |
| 9 | health endpoints returning 200 without probing deps | n/a | No HTTP service in Python surface (Streamlit dashboards only); web/ API routes covered in PR #2 scope. |

## Fabricated-data defect (worst hit)

`system_launcher.py` step 8 previously caught scoring failures and **fabricated
`score = 85` "dummy scores"** so report generation could continue. Invented quality
scores flowing into donor/county reports is data fabrication. FIXED: the pipeline now
logs the traceback and exits non-zero. Decision recorded in `docs/DECISIONS.md`.

## Exit-code propagation check

- `run_test_pipeline.py`: exit 1 on failure (fixed this pass; verified by reading control flow).
- `system_launcher.py`: SystemExit(1) on scoring failure; dashboard return codes printed.
- CI: no `|| true`, no `set +e`; drift guard uses `git diff --exit-code`.
