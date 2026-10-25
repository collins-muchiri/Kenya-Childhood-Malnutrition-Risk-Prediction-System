# Silent-failure sweep - Kenya-Childhood-Malnutrition-Risk-Prediction-System
Date: 2026-10-25T13:03:06Z  Branch: fix/zero-red-python-gates

```
PATTERN: \|\|\s*true|set\s+\+e|continue-on-error|allow_failure|--no-verify
./web/package.json:13:    "prepare": "cd .. && husky web/.husky || true"

1 matches
1 matched lines
1 files contained matches
149 files searched
73 bytes printed
2427504 bytes searched
0.005827 seconds spent searching
0.008505 seconds
```

```
PATTERN: except\s*:|contextlib\.suppress|soft_fail|best_effort|ignore_errors

0 matches
0 matched lines
0 files contained matches
149 files searched
0 bytes printed
2427504 bytes searched
0.003095 seconds spent searching
0.006813 seconds
```

```
PATTERN: except\s+Exception
./src/utils/file_utils.py:57:    except Exception as e:
./src/utils/file_utils.py:92:    except Exception as e:
./src/data/clean_data.py:104:    except Exception as e:
./src/data/load_data.py:63:    except Exception as e:
./src/data/load_data.py:181:        except Exception as e:
./src/data/load_data.py:217:    except Exception as e:
./src/data/load_data.py:237:    except Exception as e:
./src/utils/model_utils.py:57:    except Exception as e:
./src/utils/model_utils.py:90:    except Exception as e:
./src/features/build_features.py:122:    except Exception as e:
./run_test_pipeline.py:84:    except Exception as e:
./debug/debug_data_quality.py:93:    except Exception as e:
./debug/debug_data_quality.py:287:    except Exception as e:
./debug/debug_system.py:215:    except Exception as e:
./PROJECT_REVIEW.md:71:    except Exception as e:
./PROJECT_REVIEW.md:622:        except Exception as e:
./PROJECT_REVIEW.md:645:    except Exception as e:
./app/data_quality_app.py:40:    except Exception as e:
./app/executive_dashboard.py:43:    except Exception as e:
./app/app.py:39:    except Exception as e:
./system_launcher.py:111:    except Exception as e:

24 matches
24 matched lines
16 files contained matches
149 files searched
1362 bytes printed
2427504 bytes searched
0.002657 seconds spent searching
0.007068 seconds
```

```
PATTERN: asyncio\.create_task\(|threading\.Thread\(
./system_launcher.py:161:        thread = threading.Thread(target=run_dashboard, args=(dashboard_path, url))

1 matches
1 matched lines
1 files contained matches
149 files searched
109 bytes printed
2427504 bytes searched
0.002270 seconds spent searching
0.006331 seconds
```

```
PATTERN: seed\s*=|random_state
./train_model.py:104:        X, y, test_size=0.3, stratify=y, random_state=a.seed
./train_model.py:107:    model = HistGradientBoostingClassifier(random_state=a.seed, max_iter=300)
./config/config.py:63:                "random_state": 42,
./PROJECT_REVIEW.md:34:        "random_state": 42,
./PROJECT_REVIEW.md:445:- Hardcoded random_state
./PROJECT_REVIEW.md:542:        "random_state": 42,
./PROJECT_REVIEW.md:715:        random_state=model_params['random_state']
./tests/test_utils.py:47:            model = RandomForestRegressor(n_estimators=2, random_state=42)
./web/components/MapClient.tsx:130:    const seed = selectedCounty.length * 7;

10 matches
9 matched lines
5 files contained matches
149 files searched
644 bytes printed
2427504 bytes searched
0.002528 seconds spent searching
0.006655 seconds
```

```
PATTERN: catch\s*\(\s*\)?\s*\{\s*\}|@ts-ignore|eslint-disable

0 matches
0 matched lines
0 files contained matches
149 files searched
0 bytes printed
2427504 bytes searched
0.002714 seconds spent searching
0.006262 seconds
```

```
PATTERN: dropna\(|drop_duplicates\(|errors=..ignore.|skip_bad|strict=False
./src/validation/validate_data.py:86:    date_diffs = df_sorted["date"].diff().dt.days.dropna()
./src/data/clean_data.py:72:    df = df.dropna(subset=[target_col])
./src/features/build_features.py:86:    df = df.dropna().reset_index(drop=True)
./debug/debug_system.py:198:            limited_data = features_data[cols_to_keep].dropna()
./tests/test_model_training.py:36:        df = df.dropna()

5 matches
5 matched lines
5 files contained matches
149 files searched
395 bytes printed
2427504 bytes searched
0.025247 seconds spent searching
0.028799 seconds
```

```
PATTERN: if\s+df\.empty|len\(.+\)\s*==\s*0
./src/validation/validate_data.py:56:    return {"passed": len(issues) == 0, "issues": issues}
./src/validation/validate_data.py:99:    return {"passed": len(issues) == 0, "issues": issues}
./src/validation/validate_data.py:133:    return {"passed": len(issues) == 0, "issues": issues}
./src/validation/validate_data.py:177:    return {"passed": len(issues) == 0, "issues": issues}
./src/validation/validate_data.py:205:        "passed": len(issues) == 0,
./src/validation/validate_data.py:260:    return {"passed": len(issues) == 0, "issues": issues}
./src/scoring/compute_scores.py:38:    if df.empty:
./src/system/system_health_check.py:122:                    if df.empty:
./src/utils/file_utils.py:47:    if df.empty:
./src/data/clean_data.py:36:    if df.empty:
./src/features/build_features.py:42:    if df.empty:
./app/data_quality_app.py:52:    if df.empty:

12 matches
12 matched lines
7 files contained matches
149 files searched
867 bytes printed
2427504 bytes searched
0.002798 seconds spent searching
0.006718 seconds
```

```
PATTERN: errors="coerce"|errors='coerce'
./src/data/load_data.py:169:                df["date"] = pd.to_datetime(df["date"], errors="coerce")
./app/data_quality_app.py:33:            df["date"] = pd.to_datetime(df["date"], errors="coerce")

2 matches
2 matched lines
2 files contained matches
149 files searched
199 bytes printed
2427504 bytes searched
0.004342 seconds spent searching
0.006513 seconds
```

```
PATTERN: HTTP_200_OK|status_code=200

0 matches
0 matched lines
0 files contained matches
149 files searched
0 bytes printed
2427504 bytes searched
0.002703 seconds spent searching
0.006847 seconds
```
