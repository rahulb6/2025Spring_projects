# F1 Logistics Simulation using Monte Carlo

## Project Overview

This project models the complex logistics of transporting F1 race equipment from one circuit to another using Monte Carlo simulation. Based on real F1 schedules and practical team constraints, the simulation predicts delivery delays under various risks such as vehicle breakdowns, disturbances, and crash-related part replacements.

## Authors
- Rahul Balasubramani (rahulb6)
- Anushree Udhayakumar (au11)
University of Illinois Urbana-Champaign — IS597 Spring 2025 Final Project

## Code Files

### `main.py`
The main simulation script:
- Decides transport mode (road or air) based on distance and continent.
- Simulates scenarios:
    - Baseline (no delays)
    - Crash + fabrication delay
    - Breakdown delay
    - Disturbance delay
- Generates results as histograms and convergence plots.

### `gen_circuit_details.py`
Data file containing official 2025 F1 race information:
- Race names
- Race dates
- Continents
- Track latitude/longitude

### `map.py`
Utility to generate an interactive HTML map of the 2025 race circuits using `folium`.

## Libraries Used

| Library | Purpose |
|--------|---------|
| numpy | Random sampling and statistics |
| matplotlib | Plotting results |
| geographiclib | Great-circle distance calculation |
| folium | Interactive circuit map generation |

## How to Run

1. Install the required Python libraries:
pip install -r requirements.txt

2. Run the simulation:
python main.py

Notes:
- PERT distributions were used to simulate randomness with a bias toward the most likely outcome.

- Race calendar and distances were calculated using actual coordinates and timelines.

- The simulation was designed to mimic the planning decisions a real F1 logistics manager would take.

Citation:
This project references:

 - DHL F1 Transport Logistics case studies

 - FIA regulations on race event timelines

 - Publicly available F1 documentaries