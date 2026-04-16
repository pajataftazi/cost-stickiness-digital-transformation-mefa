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

