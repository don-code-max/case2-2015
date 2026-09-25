# case2-2015 — Philippine Customs Data Pipeline (Q4 2015)

## Setup & Run Instructions

1. Clone the repo and enter the folder:

git clone https://github.com/don-code-max/case2-2015.git
cd case2-2015

2. Set up the Python environment:

python3 -m venv venv
source venv/bin/activate # on Windows: venv\Scripts\activate
pip install -r requirements.txt

3. Download `2015.csv` from the data source below and place it at `data/2015.csv`.
4. Run the pipeline (processing -> aggregation -> plotting) to regenerate all outputs in `outputs/`.

## Data Source

- **File:** `2015.csv`
- **Source:** BetterGov.PH Open Customs Data collection (Bureau of Customs, Philippines)
- **URL:** https://huggingface.co/datasets/bettergovph/open-customs-data
- **Size:** 493.5 MB
- **Download date:** September 25, 2026

## Filter & Transformation Rules

- **Filter:** `tq == '2015q4' AND dutiablevaluephp > 0`
- **Rows with missing `tq` or `dutiablevaluephp`** are excluded and tracked separately (not silently dropped).
- **Grouping columns:** `countryorigin_iso3`, `tq`
- **Measure column:** `dutiablevaluephp`
- **Derived numeric column:** `dutiablevaluephp_million` (measure divided by 1,000,000)
- **Derived flag column:** `value_tier` — "high" or "low", split on the median of `dutiablevaluephp`

## Field Meanings & Units

- `countryorigin_iso3` — ISO3 country code of origin. Note: some rows use non-standard values such as `"MANY"` (36,152 rows in the raw dataset), representing shipments with multiple countries of origin rather than a single ISO3 code. These are retained in the analysis as their own category rather than excluded, since they represent real transactions.
- `tq` — year-quarter identifier (e.g. "2015q4")
- `dutiablevaluephp` — Dutiable value in Philippine Pesos (PHP)

## Plots

- **Bar Chart:** The bar chart shows the ten countries with the highest total dutiable value in Q4 2015, in millions of PHP.
- **Heatmap:** The heatmap displays the total dutiable value by country and quarter (PHP), excluding margin totals.