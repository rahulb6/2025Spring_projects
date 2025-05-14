IS597 Spring 2025 - Final Project
F1 Logistics using Monte Carlo Simulation

Libraries Used:

| Library       | Purpose                           |
|---------------|-----------------------------------|
| numpy         | Random sampling and statistics    |
| matplotlib    | Plotting results                  |
| geographiclib | Great-circle distance calculation |
| folium        | Interactive circuit map generation|


HOW TO RUN:
1. Install the required Python libraries:
   pip install -r requirements.txt

2. Edit any configuration values if needed in config.yaml (example: number of simulations, HQ coordinates, distance thresholds).

3. Run the simulation:
   python main.py

Notes:
- PERT distributions were used to simulate randomness with a bias toward the most likely outcome.
- All distances between tracks were calculated using real-world latitude-longitude coordinates and official F1 2025 calendar dates.
- We introduced a config.yaml file for easily adjusting global simulation settings like number of simulations or threshold values. This gives you control without changing the code.
- The simulation mimics decision-making by a real F1 team’s logistics and risk management department to decide whether to use road or air based on distance and continent logic.

--------------------------------------------------------------------------------
