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
   Step1: Try map.py
   Step2: Run gen_circuit_details.py
   STep3: Run main.py

Notes:
- All distances between tracks were calculated using real-world latitude-longitude coordinates and official F1 2025 calendar dates as seen in gen_circuit_details.py
- We introduced a config.yaml file for easily adjusting global simulation settings like number of simulations or threshold values. It also allows you to easily change the assumed thresholds in one place without changing the code.
--------------------------------------------------------------------------------
