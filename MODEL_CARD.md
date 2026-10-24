# Model card: childhood malnutrition risk prediction, Kenya

## Model
Gradient-boosted classifier over household and county-level features predicting acute childhood
malnutrition risk. Exact estimator and hyperparameters are recorded in train_model.py output manifest.

## Intended use
Priority-setting support for nutrition programme planning at county level in Kenya. Not a clinical
or household-level diagnostic tool. Must not be used to determine individual eligibility for
services.

## Training data
See DATA_PROVENANCE.md. Every dataset row there must carry a source, licence and retrieval date
before this card is considered complete. Rows marked TO VERIFY block sign-off.

## Validation
Metric, holdout scheme and confidence interval are produced by train_model.py and written to
models/metrics.json. A metric without an interval is not published. Stratification is by county
and by survey year so that temporal leakage is visible rather than hidden.

## Known failure modes
- Counties with sparse survey coverage inherit model priors rather than local signal; the prediction
  interval widens but the point estimate does not announce that. Treat low-coverage counties as
  model opinion, not measurement.
- The deployed web application currently reads a static prediction snapshot. Between retraining runs
  the dashboard ages silently. See docs/DATA_RELEASES.md.
- Feature set includes administrative boundaries that changed in 2013 and 2019; joins across boundary
  versions are a known source of error.

## Out of scope
Application to countries other than Kenya, to age groups outside the trained range, and to
non-nutrition outcomes.

## Reproduction
python3 train_model.py --seed 42 produces models/model.joblib and models/metrics.json. Committed
pickle artifacts are deprecated by this card and are removed by cleanup script in this release.

## Ethics and protection
Aggregate public data only. No individual-level beneficiary data is present. See docs/DPIA.md.
