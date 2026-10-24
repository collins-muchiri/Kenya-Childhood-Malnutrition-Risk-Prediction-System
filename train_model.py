"""Deterministic training entry point. Replaces committed binary model artifacts.

Reads every data/*.csv that contains the target column, refuses to run while any provenance sidecar
is missing or marked TO VERIFY, trains a gradient-boosted classifier on a stratified holdout and
writes models/model.joblib plus models/metrics.json. The models directory must be gitignored; the
reproduction path is this script, not a binary.
"""
import argparse, hashlib, json, subprocess, sys
from pathlib import Path

import joblib
import numpy as np
import pandas as pd
from sklearn.ensemble import HistGradientBoostingClassifier
from sklearn.metrics import roc_auc_score
from sklearn.model_selection import train_test_split

REPO = Path(__file__).resolve().parent
DATA = REPO / "data"
MODELS = REPO / "models"
SEED = 42


def provenance_gaps():
    gaps = []
    for csv in sorted(DATA.glob("*.csv")):
        side = csv.with_suffix(".json")
        if not side.exists():
            gaps.append(f"{csv.name}: no provenance sidecar")
            continue
        meta = json.loads(side.read_text())
        for field in ("source", "licence", "retrieval_date"):
            if not meta.get(field) or "TO VERIFY" in str(meta.get(field)):
                gaps.append(f"{csv.name}: {field} missing or unverified")
    return gaps


def load_frame(target):
    frames = [pd.read_csv(c) for c in sorted(DATA.glob("*.csv")) if target in pd.read_csv(c, nrows=0).columns]
    if not frames:
        sys.exit(f"target column {target!r} not present in any data/*.csv")
    return pd.concat(frames, ignore_index=True)


def bootstrap_auc(y, p, n=400):
    rng = np.random.default_rng(SEED)
    aucs = []
    for _ in range(n):
        idx = rng.integers(0, len(y), len(y))
        if y.iloc[idx].nunique() < 2:
            continue
        aucs.append(roc_auc_score(y.iloc[idx], p[idx]))
    lo, hi = np.percentile(aucs, [2.5, 97.5])
    return float(lo), float(hi)


def git_hash():
    try:
        return subprocess.run(["git", "rev-parse", "HEAD"], cwd=REPO, capture_output=True,
                              text=True, check=True).stdout.strip()
    except Exception:
        return "unknown"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--target", required=True, help="name of the binary outcome column")
    ap.add_argument("--seed", type=int, default=SEED)
    a = ap.parse_args()

    gaps = provenance_gaps()
    if gaps:
        print("refusing to train on unprovenanced data:")
        print("\n".join("  - " + g for g in gaps))
        print("complete DATA_PROVENANCE.md sidecars first; an unprovenanced model is an unauditable model")
        return 1

    df = load_frame(a.target)
    drop = [a.target] + [c for c in df.columns if c.lower() in ("id", "household_id", "case_id")]
    X = df.select_dtypes(include=[np.number]).drop(columns=[c for c in drop if c in df.columns])
    y = df[a.target].astype(int)
    X_tr, X_te, y_tr, y_te = train_test_split(X, y, test_size=0.3, stratify=y, random_state=a.seed)

    model = HistGradientBoostingClassifier(random_state=a.seed, max_iter=300)
    model.fit(X_tr, y_tr)
    prob = model.predict_proba(X_te)[:, 1]
    auc = roc_auc_score(y_te, prob)
    lo, hi = bootstrap_auc(y_te, prob)

    MODELS.mkdir(exist_ok=True)
    joblib.dump(model, MODELS / "model.joblib")
    metrics = {
        "target": a.target, "seed": a.seed, "n_rows": int(len(df)),
        "n_train": int(len(y_tr)), "n_test": int(len(y_te)),
        "roc_auc": float(auc), "roc_auc_ci95": [lo, hi],
        "features": list(X.columns),
        "data_sha256": hashlib.sha256(pd.util.hash_pandas_object(df, index=False).values.tobytes()).hexdigest()[:16],
        "git_commit": git_hash(),
        "note": "county-level planning support only; see MODEL_CARD.md for intended use and out-of-scope use",
    }
    (MODELS / "metrics.json").write_text(json.dumps(metrics, indent=2))
    print(f"trained on {metrics['n_train']} rows, auc {auc:.3f} (95% CI {lo:.3f} to {hi:.3f})")
    print("models/ must be gitignored; the reproduction path is this script")
    return 0


if __name__ == "__main__":
    sys.exit(main())
