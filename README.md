**FORMULA ONE LOGISTICS FOR RED BULL RACING**
Formula One is as much a race off the track as it is on it. Each F1 season spans from March to December, with races scheduled across continents — including North America, South America, Europe, Australia, and the Middle East. The limited downtime between races poses a tremendous challenge in transporting critical and non-critical cargo across the globe. The equipment that must arrive on time includes **spare parts, pit stop jacks, telemetric and communication equipment, broadcasting setups, construction gear for motorhomes, tools, hospitality furniture (tables, chairs, cutlery), and more**. With anywhere between **2 days to 1 week** available for turnaround, Formula One teams partner with logistics giants like **DHL** and **Ceva Logistics** to execute this operation with surgical precision.

Pre-Season Setup
Before the first Grand Prix of the year, teams pre-position **non-critical equipment** via **sea freight** to key international hubs. From there, these materials are distributed to race venues using a combination of **air freight** (cargo planes) and **road freight** (specialized trucks).

Race Weekend Timing
Each race happens on **Sunday**, with **qualifying sessions** on **Saturday** or **Friday** (in sprint weekends), and promotional or media events beginning as early as **Thursday**. This schedule gives teams **Wednesday and Thursday** to build and organize the garage, pit wall, and hospitality areas.

The real logistical test comes during:
* **Double-Headers**: two races on back-to-back weekends.
* **Triple-Headers**: three consecutive race weekends.
In these scenarios, cargo must be disassembled after Sunday’s race and transported overnight. The race may end at **1:00 PM** or as late as **1:00 AM**, leaving a transport window of roughly **48–58 hours** depending on local regulations and proximity. Although more time is available between spaced-out races, teams **do not take the full week** — doing so would be inefficient and risky. For this simulation, we use **65 hours as the upper limit** for all logistics scenarios to reflect the actual operational benchmark.

DESIGN PHASE
**Hypotheses**
This simulation explores multiple real-world scenarios Red Bull Racing could face when transporting critical equipment between Formula 1 races, based on the 2025 calendar. Each hypothesis reflects a plausible operational challenge in tight race-to-race turnaround windows.
**H₀: Baseline Scenario (Validation Hypothesis)**: No crash occurred in the previous race, no breakdowns during transport, and no external disturbances. This serves as a reference case to validate the normal logistics pipeline under ideal conditions.
**H₁: Crash and Spare Part Depletion**: A crash occurred at the previous race, and the team's spare parts inventory has been exhausted. New components must be fabricated at Red Bull’s headquarters in **Milton Keynes** and transported to the next race venue in time for assembly.
**H₂: Breakdown During Transport**: A mechanical failure occurs during transport — either in road-based trucking or air cargo — causing delays. The simulation models the time taken to resolve the breakdown and resume delivery.
**H₃: Unplanned External Disturbance**: Unexpected delays arise from external events such as local protests, customs issues, or adverse weather. These are modeled using a **disturbance duration** and a **severity multiplier** to reflect real-world variability. This hypothesis acts as a catch-all for disruptive events not explicitly modeled elsewhere.

**Simulation Setup**
Fixed Variables:
  * Focused team: Red Bull Racing
  * Headquarters: Milton Keynes, UK
  * Reference calendar: F1 2025 schedule
  * Delivery deadline: 58 hours for standard triple/double-headers; 65 hours for longer windows
Randomized Variables (with PERT distributions):
  * Roadway and airway speeds [add citation]
  * Fabrication time (for parts post-crash)
  * Breakdown duration
  * Disturbance duration and severity multiplier

We chose **PERT distributions** for randomization because they allow modeling of uncertainty using **best-case, most-likely, and worst-case** estimates — which we feel is a good fit for logistics scenarios. It also allowed for those values we werent able to find, such as the fabrication time for various parts. The facility to define a range of values and cause the randomization to skew towards the most likely value, and stay within the worst case and worst case values made PERT both intuitive and interpretable.
