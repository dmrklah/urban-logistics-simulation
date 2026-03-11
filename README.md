# Hybrid Simulation of Urban Last-Mile Logistics under Peak Demand

**Module:** Advanced Simulation Techniques  
**Degree:** BSc Computer Science and Digitization  

---

## Overview

This project implements a hybrid simulation model to analyse urban last-mile delivery performance under normal and peak demand conditions. The model combines two complementary simulation techniques:

- **Discrete Event Simulation (DES)** — models the structured flow of orders through the logistics network (warehouse → micro-hub → customer)
- **Monte Carlo Simulation** — introduces stochastic variability in order arrivals and travel durations

---

## Scenarios

| Scenario | Description |
|----------|-------------|
| Normal Day | Baseline demand with standard arrival rates and fixed fleet |
| Peak Day | High-demand period (e.g. promotional event) with increased order volume, same fleet size |

---

## Key Findings

- Average delivery time increased from **42.5 min** (Normal Day) to **78.3 min** (Peak Day)
- Fleet capacity was identified as the dominant bottleneck
- Non-linear performance degradation observed as demand approaches system limits
- The hybrid approach captured congestion effects that a purely deterministic model would miss

---

## Files

| File | Description |
|------|-------------|
| `simulation.py` | Full hybrid simulation implementation (SimPy + Monte Carlo) |
| `report.pdf` | Full assignment report with conceptual model, results, and analysis |

---

## How to Run
```bash
pip install simpy numpy matplotlib pandas
python simulation.py
```

Or open in Google Colab:  
🔗 [View Colab Notebook](https://colab.research.google.com/drive/13v3WZWQwdc-Fjsx8pblSYpVZNd5H5xt1?usp=sharing)

---

## Technologies

- Python 3 · SimPy · NumPy · Matplotlib · Google Colab
