# Red Bull’s Race Day Delivery for Double-Headers  
### Monte Carlo Simulation to Explore Logistics Risks in Formula 1

## Project Overview:

Formula 1 teams face a substantial logistical challenge when they have to move equipment from one race location to the next, especially during back-to-back race weekends (double-headers). With tight FIA deadlines and unpredictable issues like traffic, weather, or equipment failures, a lot can go wrong.

In this project, we simulate what could happen during those race-to-race delivery windows. We model real-world delivery risks using a Monte Carlo approach to see how often things go smoothly and when and why they don’t. Our focus is on Red Bull Racing, and our goal is to understand better the impact of breakdowns, delays, and disruptions on meeting a strict 96-hour delivery deadline.


## Inputs:

These are the constants in our simulation that reflect reality as closely as possible:

- **Race Calendar:** Based on the actual 2024 F1 schedule  
- **Distances:** Calculated geodesically between tracks and from team HQ in Milton Keynes  
- **Number of Trucks:** 3 per team  
- **Air Cargo:** 1 shipment per team  
- **Delivery Deadline:** 96 hours (FIA rule for setup completion before race)

To Do:
1. work on making the baseline itself a bit more realistic or justify strongly why the current average delivery time is proper.
2. Use other statistics like median to compare hypothesis
3. do doctests
4. make loading-unloading dynamic using pert
5. do not assume 20kms between airport and track - include airport coordinates and calcualte distance dynamically
6. consider moving non-damaged parts from track_A to track_B
7. Do README



## Variables:




---

## Code Structure:

We’ve broken the simulation into modular functions to keep it structured and reusable:



---



## Hypotheses:


