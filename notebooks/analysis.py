# ============================================================
# India GDP Fact-Check — Data Analysis Pipeline
# The Data Desk | Salim Arshad
# Tools: Python (pandas) + SQLite
# ============================================================

import pandas as pd
import sqlite3
import os

# ── 1. LOAD RAW DATA ─────────────────────────────────────────

viral_df = pd.read_csv("data/raw/viral_claims.csv")
imf_df   = pd.read_csv("data/raw/imf_weo_apr2026.csv")
india_df = pd.read_csv("data/raw/india_gdp_trend.csv")

print("✅ Raw data loaded")
print(f"   Viral claims: {len(viral_df)} rows")
print(f"   IMF WEO:      {len(imf_df)} rows")
print(f"   India trend:  {len(india_df)} rows")


# ── 2. MERGE VIRAL vs IMF ────────────────────────────────────

# Standardise country names for joining
name_map = {
    "United States": "United States",
    "United Kingdom": "United Kingdom",
}

merged = viral_df.merge(
    imf_df[["country", "imf_weo_apr2026_rate", "data_type", "economy_type"]],
    left_on="country",
    right_on="country",
    how="left"
)

merged["discrepancy"]   = merged["viral_claimed_rate"] - merged["imf_weo_apr2026_rate"]
merged["is_overstated"] = (merged["discrepancy"] > 0.1).astype(int)

merged["verdict"] = merged["discrepancy"].apply(
    lambda x:
        "🔴 Significant overstatement" if x > 0.5
        else ("⚠️  Minor overstatement" if x > 0.1
        else ("✅ Accurate"             if abs(x) <= 0.1
        else  "🔵 Understated"))
)

print("\n📊 Viral Claim vs IMF Data:")
print(merged[["country", "viral_claimed_rate", "imf_weo_apr2026_rate",
              "discrepancy", "verdict"]].to_string(index=False))


# ── 3. FACT-CHECK SCORECARD ──────────────────────────────────

total      = len(merged.dropna(subset=["imf_weo_apr2026_rate"]))
overstated = (merged["discrepancy"] > 0.5).sum()
minor      = ((merged["discrepancy"] > 0.1) & (merged["discrepancy"] <= 0.5)).sum()
accurate   = (merged["discrepancy"].abs() <= 0.1).sum()

print(f"\n📋 Scorecard:")
print(f"   Total countries compared : {total}")
print(f"   Significantly overstated : {overstated}")
print(f"   Minor overstatement      : {minor}")
print(f"   Accurate (±0.1%)         : {accurate}")


# ── 4. SAVE PROCESSED DATA ───────────────────────────────────

os.makedirs("data/processed", exist_ok=True)

merged.to_csv("data/processed/viral_vs_imf_comparison.csv", index=False)
india_df.to_csv("data/processed/india_trend_clean.csv", index=False)

print("\n✅ Processed data saved to data/processed/")


# ── 5. LOAD INTO SQLITE ──────────────────────────────────────

os.makedirs("data/sql", exist_ok=True)
conn = sqlite3.connect("data/sql/india_gdp_factcheck.db")

# Countries table
countries = imf_df[["country", "iso_code", "economy_type", "region"]].copy()
countries.columns = ["country_name", "iso_code", "economy_type", "region"]
countries["country_id"] = range(1, len(countries) + 1)
countries.to_sql("countries", conn, if_exists="replace", index=False)

# GDP growth table
gdp_rows = []
for _, row in imf_df.iterrows():
    cid = countries.loc[countries["country_name"] == row["country"], "country_id"].values
    if len(cid):
        gdp_rows.append({
            "country_id":    int(cid[0]),
            "year":          2026,
            "growth_rate":   row["imf_weo_apr2026_rate"],
            "data_type":     row["data_type"],
            "source":        "IMF_WEO_Apr2026",
            "fiscal_period": row["fiscal_period"]
        })

gdp_df = pd.DataFrame(gdp_rows)
gdp_df.to_sql("gdp_growth", conn, if_exists="replace", index=False)

# Viral claims table
viral_clean = merged.dropna(subset=["imf_weo_apr2026_rate"])[[
    "country", "viral_claimed_rate", "source_label",
    "imf_weo_apr2026_rate", "discrepancy", "is_overstated"
]].copy()
viral_clean.columns = [
    "country_name", "claimed_rate", "source_label",
    "imf_actual", "discrepancy", "is_overstated"
]
viral_clean.to_sql("viral_claims", conn, if_exists="replace", index=False)

# India trend table
india_df.to_sql("india_trend", conn, if_exists="replace", index=False)

conn.close()
print("✅ SQLite database created: data/sql/india_gdp_factcheck.db")
print("\n🎯 Pipeline complete. Ready for Tableau.")
