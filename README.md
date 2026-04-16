# The Moderation Effect of Cost Stickiness in Digital Transformation 
# on Management Earnings Forecast Accuracy

> **Bachelor of Economics Thesis**  
> Paja Taftazani | 2101102010192  
> Faculty of Economics, Universitas Syiah Kuala  
> Banda Aceh, 2026

---

## 📌 About This Research

This thesis investigates the relationship between **digital transformation** 
and **management earnings forecast accuracy (MEFA)** in Indonesian listed 
banking companies, with **cost stickiness** as a moderating variable.

### Research Questions
1. Does digital transformation affect management earnings forecast accuracy?
2. Does cost stickiness affect management earnings forecast accuracy?
3. Does cost stickiness moderate the relationship between digital 
   transformation and management earnings forecast accuracy?

### Hypotheses
- **H1:** Digital transformation has a significant positive effect on MEFA
- **H2:** Cost stickiness has a significant negative effect on MEFA
- **H3:** Cost stickiness moderates the relationship between 
  digital transformation and MEFA

---

## 📊 Dataset Overview

| Item | Detail |
|---|---|
| **Sample** | 43 Indonesian Commercial Banks listed on IDX |
| **Period** | 2019 – 2024 (6 years) |
| **Observations** | 256 firm-year observations |
| **Data Source** | Annual Reports (IDX), Bloomberg |

### Banks Studied (Sample)
- Bank Central Asia (BCA) — BBCA
- Bank Rakyat Indonesia (BRI) — BBRI
- Bank Negara Indonesia (BNI) — BBNI
- Bank Mandiri — BMRI
- *(and 40 other listed banks)*

---

## 📐 Variable Measurement

### 1. Dependent Variable: MEFA
MEFA = |Forecast Net Profit - Actual Net Profit| / |Actual Net Profit|

*Source: Zeng & Wang (2025)*
### 2. Independent Variable: Digital Transformation (LDigital)
LDigital = ln(1 + Digital Keyword Frequency in Annual Report)

*Source: Zeng & Wang (2025); Wu et al. (2021)*
### 3. Moderating Variable: Cost Stickiness (CS)
STICKY = log(|ΔCost/ΔSale|)_τ⁻ - log(|ΔCost/ΔSale|)_τ⁺

Where τ⁻ = most recent year with sales decrease  
      τ⁺ = most recent year with sales increase  
*Source: Weiss (2010); Li & Sun (2023)*
### 4. Control Variable
SIZE = ln(Total Assets)



---
## 🔢 Regression Model
### Main Model
MEFA_it = β₀ + β₁DT_it + β₂CS_it + β₃(DT × CS)_it + β₄SIZE_it + ε_it



### Panel Data Selection Tests
- Chow Test → CEM vs FEM
- Lagrange Multiplier Test → CEM vs REM
- Hausman Test → FEM vs REM
---
## 📈 Key Results (BCA Sample — 2019–2024)
| Year | LDigital | Cost Stickiness | Actual Profit (Rp Bn) | MEFA (%) |
|------|----------|-----------------|----------------------|----------|
| 2019 | —        | —               | 13,050               | 1.15%    |
| 2020 | —        | −0.4238         | 12,900               | 3.88%    |
| 2021 | 4.5218   | −0.3567         | 13,250               | 2.64%    |
| 2022 | 4.7449   | −0.4740         | 13,550               | 2.58%    |
| 2023 | 4.5951   | −0.4910         | 14,100               | 2.84%    |
| 2024 | 4.7536   | −0.3697         | 14,800               | 2.70%    |
---

## 🛠️ How to Run the Code
### Prerequisites
```bash
# Install required packages
pip install -r requirements.txt
# Step 1: Collect and clean raw data
python code/01_data_collection.py

# Step 2: Calculate MEFA
python code/02_mefa_calculation.py

# Step 3: Calculate Cost Stickiness
python code/03_cost_stickiness.py

# Step 4: Calculate Digital Transformation Index
python code/04_digital_transformation.py

# Step 5: Run panel regression (export to EViews)
python code/05_panel_regression.py

# Step 6: Generate charts
python code/06_visualization.py

pandas==2.0.0
numpy==1.24.0
scipy==1.10.0
matplotlib==3.7.0
seaborn==0.12.0
openpyxl==3.1.0
statsmodels==0.14.0

No.,Author,Year,Title,Journal

1,Zeng & Wang,2025,The Impact of Corporate Digital Transformation on the Accuracy of Management's Earnings Forecasts,International Review of Economics and Finance
2,Li & Sun,2023,"Cost Stickiness, Earnings Forecast Accuracy, and the Informativeness of Stock Prices",Humanities and Social Sciences Communications
3,"Anderson, Banker & Janakiraman",2003,"Are SG&A Costs ""Sticky""?",Journal of Accounting Research
4,Weiss,2010,Cost Behavior and Analysts' Earnings Forecasts,The Accounting Review
5,"He, Li & Lin",2025,Does Digitalization Imply Uncertainty About the Future Prospects of a Firm?,Financial Review

---

## 4. data/raw/README.md — Copy This

```markdown
# Raw Data Sources

The raw annual report PDFs are NOT stored in this repository 
due to file size and copyright restrictions.

## How to Download the Data

### For each bank, download the annual reports for 2019–2024:

| Bank | Stock Code | Investor Relations URL |
|------|------------|----------------------|
| BCA  | BBCA | https://www.bca.co.id/id/Tentang-BCA/Hubungan-Investor |
| BRI  | BBRI | https://ir.bri.co.id/ |
| BNI  | BBNI | https://ir.bni.co.id/ |
| Mandiri | BMRI | https://ir.bankmandiri.co.id/ |
| *(others)* | — | https://www.idx.co.id/ |

## Data Points to Collect from Each Annual Report

### For MEFA:
- Management's Forecast Net Profit (from MD&A section)
- Actual Net Profit After Tax (from Income Statement)

### For Cost Stickiness:
- Total Operating Revenue (Income Statement)
- Net Profit Before Extraordinary Items (Income Statement)

### For Digital Transformation:
- Count of digital-related keywords in the MD&A section
  (AI, big data, cloud, blockchain, digital banking, fintech, etc.)

## File Naming Convention
Save files as: `{BANK_CODE}_{YEAR}_annual_report.pdf`
Example: `BBCA_2021_annual_report.pdf`

