-- ============================================================
-- India GDP Fact-Check Project
-- The Data Desk | Salim Arshad
-- SQL Schema + Analytical Queries
-- ============================================================

-- TABLE 1: Countries reference
CREATE TABLE IF NOT EXISTS countries (
    country_id   INTEGER PRIMARY KEY AUTOINCREMENT,
    country_name TEXT NOT NULL,
    iso_code     TEXT,
    region       TEXT,
    economy_type TEXT  -- 'Advanced', 'Emerging', 'Developing'
);

-- TABLE 2: GDP growth data (IMF + MoSPI)
CREATE TABLE IF NOT EXISTS gdp_growth (
    id           INTEGER PRIMARY KEY AUTOINCREMENT,
    country_id   INTEGER,
    year         INTEGER,
    growth_rate  REAL,
    data_type    TEXT,   -- 'actual' or 'forecast'
    source       TEXT,   -- 'MoSPI', 'IMF_WEO_Apr2026', 'WorldBank'
    fiscal_period TEXT,  -- 'FY26', 'CY2026' etc.
    FOREIGN KEY (country_id) REFERENCES countries(country_id)
);

-- TABLE 3: Viral chart claims
CREATE TABLE IF NOT EXISTS viral_claims (
    id            INTEGER PRIMARY KEY AUTOINCREMENT,
    country_name  TEXT,
    claimed_rate  REAL,
    source_label  TEXT,
    imf_actual    REAL,
    discrepancy   REAL,   -- claimed minus IMF actual
    is_overstated INTEGER -- 1 = yes, 0 = no
);

-- ============================================================
-- ANALYTICAL QUERIES
-- ============================================================

-- Q1: Which countries are most overstated in the viral chart?
SELECT
    country_name,
    claimed_rate,
    imf_actual,
    discrepancy,
    CASE
        WHEN discrepancy > 0.5 THEN 'HIGH OVERSTATEMENT'
        WHEN discrepancy > 0.1 THEN 'MINOR OVERSTATEMENT'
        WHEN discrepancy < -0.1 THEN 'UNDERSTATED'
        ELSE 'ACCURATE'
    END AS verdict
FROM viral_claims
ORDER BY discrepancy DESC;

-- Q2: Fair comparison — India vs peers using same IMF source
SELECT
    c.country_name,
    c.economy_type,
    g.growth_rate,
    g.data_type,
    g.source,
    RANK() OVER (ORDER BY g.growth_rate DESC) AS growth_rank
FROM gdp_growth g
JOIN countries c ON g.country_id = c.country_id
WHERE g.source = 'IMF_WEO_Apr2026'
  AND g.year = 2026
ORDER BY g.growth_rate DESC;

-- Q3: India's historical trend
SELECT
    fiscal_period,
    growth_rate,
    data_type,
    LAG(growth_rate) OVER (ORDER BY year) AS prev_year_rate,
    growth_rate - LAG(growth_rate) OVER (ORDER BY year) AS yoy_change
FROM gdp_growth
WHERE country_id = (SELECT country_id FROM countries WHERE iso_code = 'IND')
ORDER BY year;

-- Q4: Summary verdict table
SELECT
    v.country_name,
    v.claimed_rate       AS viral_claim,
    v.imf_actual         AS imf_verified,
    v.discrepancy        AS gap,
    CASE
        WHEN ABS(v.discrepancy) <= 0.1  THEN '✅ Accurate'
        WHEN v.discrepancy > 0.1
         AND v.discrepancy <= 0.5       THEN '⚠️ Minor overstatement'
        WHEN v.discrepancy > 0.5        THEN '🔴 Significant overstatement'
        ELSE '✅ Accurate'
    END AS fact_check_result
FROM viral_claims v
ORDER BY v.discrepancy DESC;
