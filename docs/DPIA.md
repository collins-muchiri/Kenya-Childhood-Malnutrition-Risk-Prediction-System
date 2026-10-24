# Data protection impact assessment, summary

Scope: aggregate public survey and administrative data for county-level nutrition risk prediction.
No individual-level data. No beneficiary data. No profiling of identifiable persons.

Lawful basis: not applicable for personal data, because none is processed. If household-level data
is ever introduced, processing stops until a lawful basis and a full DPIA are recorded.

Risks assessed:
- Re-identification from small-area aggregates: mitigated by suppressing cells below the threshold
  stated in train_model.py config.
- Misuse of outputs for eligibility denial: mitigated by MODEL_CARD.md intended-use and out-of-scope
  statements, reproduced in the dashboard footer.
- Silent ageing of predictions: mitigated by docs/DATA_RELEASES.md.

Review trigger: any introduction of individual-level data, any change of geographic granularity
below county, or any use in an allocation decision.
