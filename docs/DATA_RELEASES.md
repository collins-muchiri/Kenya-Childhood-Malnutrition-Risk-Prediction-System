# Data and prediction releases

The public dashboard must never show an undated prediction set.

Scheme adopted:
1. Every prediction run writes web/data/predictions_<YYYY-MM-DD>.json plus a RELEASE.json carrying
   retrieval_date, training_date, model git hash and metrics hash.
2. The web interface renders the release date in the header on every page.
3. Releases are immutable. A correction is a new release with a note naming the previous one.
4. Retention: keep the last twelve releases; archive older ones with their RELEASE.json.

Migration note: the current static web/data/malnutrition_data.json becomes release 0 with its
retrieval date recorded as unknown, labelled as such in the interface until superseded.
