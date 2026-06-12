# 🔍 India GDP Fact-Check Dashboard
### The Data Desk | Data Journalism Project

[![Tableau Public](https://img.shields.io/badge/Tableau-Public-blue?logo=tableau)](https://public.tableau.com/views/India_GDP_Factcheck/TheDataDeskIndiaGDPFactCheck)
[![IMF Data](https://img.shields.io/badge/Source-IMF%20WEO%202025-green)](https://www.imf.org/en/Publications/WEO)

---

## 📌 Project Overview

A viral infographic claiming "UNSTOPPABLE INDIA — 7.7% GDP Growth" circulated widely across social media in 2025. This project fact-checks those claims against **IMF World Economic Outlook (April 2025)** data for 10 major economies.

**Live Dashboard →** https://public.tableau.com/views/India_GDP_Factcheck/TheDataDeskIndiaGDPFactCheck

---

## 📊 What This Dashboard Shows

### Worksheet 1 — "What They Showed"
Recreates the viral chart using IMF-verified figures with proper source attribution.

### Worksheet 2 — "The Fair Picture"
Side-by-side comparison of viral claimed values vs IMF actual data for all 10 countries.

### Worksheet 3 — "India's Own Story"
India's GDP growth trajectory from 2019–2027 with key annotations:
- 2020: COVID-19 crash (-5.8%)
- 2021: V-shaped recovery (+9.7%)
- 2025: IMF-verified 7.618%

---

## 🔢 Key Findings

| Country | Viral Claim | IMF Actual | Gap |
|---------|------------|------------|-----|
| India | 7.7% | 7.618% | +0.08% |
| USA | 2.8% | 2.117% | **+0.68%** |
| China | 5.0% | 4.959% | +0.04% |
| Brazil | 3.5% | 2.286% | **+1.21%** |
| Malaysia | 5.2% | 5.171% | +0.03% |
| Indonesia | 5.1% | 5.108% | +0.01% |

**Verdict:** India is genuinely the fastest-growing major economy. The viral chart's India figure is marginally overstated. However, USA (+0.68%) and Brazil (+1.21%) figures are significantly inflated without methodology disclosure.

---

## 🗂️ Data Sources

| Source | Details |
|--------|---------|
| IMF World Economic Outlook | April 2025 edition, GDP growth forecasts |
| MoSPI | India national accounts, FY2025-26 estimate |
| Viral Chart | "UNSTOPPABLE INDIA" infographic, Source: MoSPI + Media Reports |

---

## 🛠️ Tools Used

- **Tableau Public** — visualization and dashboard
- **Microsoft Excel** — data cleaning and preparation
- **Python** — data pipeline (pandas, sqlite3)
- **SQLite** — fact-check database
- **IMF WEO Database** — primary data source

---

## 📁 Project Structure


india-gdp-factcheck/ ├── README.md # This file ├── data/ │ ├── processed/ │ │ └── gdp_growth_clean.csv # Cleaned IMF data, 10 countries, 2019-2027 │ └── sql/ │ └── gdp_factcheck.db # SQLite database (schema & queries) ├── scripts/ │ └── build_database.py # Python ETL pipeline ├── sql/ │ └── queries.sql # SQL analysis queries └── assets/ └── viral-chart-comparison.png # Dashboard screenshot


---

## 🚀 Getting Started

### Prerequisites
- Python 3.8+
- pandas
- openpyxl (for Excel reading)

### Installation

```bash
git clone https://github.com/salimarshad07/india-gdp-factcheck.git
cd india-gdp-factcheck
pip install pandas openpyxl

# Place WEOApr2026all.xlsx in data/raw/ first
python scripts/build_database.py

sqlite3 data/sql/gdp_factcheck.db < sql/queries.sql

📊 Key Queries
Query 1: Fair Comparison (IMF WEO 2025, same source)
SELECT country, imf_2025_forecast, data_type 
FROM gdp_growth 
WHERE year = 2025 
ORDER BY imf_2025_forecast DESC;

Query 2: Discrepancy Report (viral chart vs IMF)
SELECT country_name, claimed_rate, imf_rate, discrepancy, verdict 
FROM viral_claims 
ORDER BY discrepancy DESC;

Query 3: India Historical Trend
SELECT year, growth_rate, data_type 
FROM gdp_growth 
WHERE country_id = 'IND' 
ORDER BY year;

📝 Methodology Note
IMF WEO figures used are April 2025 forecasts. India's figure (7.618%) reflects IMF's forecast for calendar year 2025, while MoSPI's 7.7% figure refers to India's fiscal year 2025-26 (April 2025–March 2026). This methodological difference partly explains the 0.08% gap.

Why This Matters:

Comparing fiscal year actuals to calendar year forecasts is methodologically inconsistent
The viral chart mixes actual data (India) with forecasts (most others) without disclosure
USA and Brazil figures show larger discrepancies (0.68pp and 1.21pp) suggesting data selection bias
👤 Author
Salim Arshad | AWS Cloud Billing Associate | Data Journalist

🌐 Portfolio: salim-portfolio-amber.vercel.app
📊 Tableau Public: The Data Desk
💼 GitHub: @salimarshad07
📜 License
This project is open source under the MIT License. See LICENSE file for details.

Part of The Data Desk — where every viral claim meets a spreadsheet. 📊✨

