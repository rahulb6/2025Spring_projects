**FORMULA ONE LOGISTICS FOR RED BULL RACING**

Formula One is as much a race off the track as it is on it. Each F1 season spans from March to December, with races scheduled across continents — including North America, South America, Europe, Australia, and the Middle East. The limited downtime between races poses a tremendous challenge in transporting critical and non-critical cargo across the globe. The equipment that must arrive on time includes **spare parts, pit stop jacks, telemetry and communication equipment, broadcasting setups, construction gear for motorhomes, tools, hospitality furniture (tables, chairs, cutlery), and more**. With anywhere between **2 days to 1 week** available for turnaround, Formula One teams partner with logistics giants like **DHL** and **Ceva Logistics** to execute this operation with surgical precision.

Pre-Season Setup:
Before the first Grand Prix of the year, teams pre-position **non-critical equipment** via **sea freight** to key international hubs. From there, these materials are distributed to race venues using a combination of **air freight** (cargo planes) and **road freight** (specialized trucks).

Race Weekend Timing:
Each race happens on **Sunday**, with **qualifying sessions** on **Saturday** or **Friday** (in sprint weekends), and promotional or media events beginning as early as **Thursday**. This schedule gives teams **Wednesday and Thursday** to build and organize the garage, pit wall, and hospitality areas.

The real logistical test comes during:
* **Double-Headers**: two races on back-to-back weekends.
* **Triple-Headers**: three consecutive race weekends.
In these scenarios, cargo must be disassembled after Sunday’s race and transported overnight. The race may end at **1:00 PM** or as late as **1:00 AM**, leaving a transport window of roughly **48–58 hours** depending on local regulations and proximity. Although more time is available between spaced-out races, teams **do not take the full week** — doing so would be inefficient and risky. For this simulation, we use **65 hours as the upper limit** for all logistics scenarios to reflect the actual operational benchmark.

**DESIGN PHASE**
**Hypotheses**
This simulation explores multiple real-world scenarios Red Bull Racing could face when transporting critical equipment between Formula 1 races, based on the 2025 calendar. Each hypothesis reflects a plausible operational challenge in tight race-to-race turnaround windows.
**H₀: Baseline Scenario (Validation Hypothesis)**: No crash occurred in the previous race, no breakdowns during transport, and no external disturbances. This serves as a reference case to validate the normal logistics pipeline under ideal conditions.
**H₁: Crash and Spare Part Depletion**: A crash occurred at the previous race, and the team's spare parts inventory has been exhausted. New components must be fabricated at Red Bull’s headquarters in **Milton Keynes** and transported to the next race venue in time for assembly.
**H₂: Breakdown During Transport**: A mechanical failure occurs during transport — either in road-based trucking or air cargo — causing delays. The simulation models the time taken to resolve the breakdown and resume delivery.
**H₃: Unplanned External Disturbance**: Unexpected delays arise from events such as local protests, customs issues, or adverse weather all of which could lead to race cancellations. These are modeled using a **severity multiplier** which gets multiplied with base **disturbance duration** to reflect real-world variability of different disturbances. This hypothesis is meant to be general to compensate for all other misfortunes we did not design within this system.

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

We chose **PERT distributions** for randomization because they allow modeling of uncertainty using **best-case, most-likely, and worst-case** estimates — which we feel is a good fit for logistics scenarios. It also allowed for those values we weren't able to find, such as the fabrication time for various parts. The facility to define a range of values and cause the randomization to skew towards the most likely value, and stay within the worst case and worst case values made PERT both intuitive and interpretable.

This system we have created for Redbull will consider 2 ways of transportation: roadways and airways. The transportation leg before the season begins, through waterways is out of the scope of this project. Our intention is to optimize transport during the race season itself. Once a race is over, looking at the date of the next race, it will decide if we have 58hours or 65 hours to transport the material. In case of double/ triple - headers, we will have 58 hours and when there is no race next week, we will have 65 hours. Then the simulator will choose between roadways and airways. If the next race is happening on the same continent as the previous race, and if the distance between the tracks is less than 4000km, then roadways is preferred, otherwise airways.

Reasoning for the constraints: 
1. Roadways - if the next race is in the same continent: Viable roadways is necessary to deliver the material. 
2. 4000km - You may ask what if we have time to slowly make the delivery even across 6000km. It is possible to make the delivery through roadways by driving the trucks for 6000Km, but it would rather be inefficient. A big trademark of Formula One and the teams partnering with them is sustainability. It wouldn't be a good choice to drive trucks for such a long distance when another efficient choice is available. airways can make that delivery in a fraction of that time, more sustainable.

In case of the Crash Hypothesis, the delivery of the fabricated part from the headquarters is always considered "urgent" or "priority" and thus is always transported through airways. This leg of transportation includes both airtime and fabrication time. because airways take lesser time than roadways. But the other non-damaged parts will also be transported from the previous race location appropriately.

In case of the Breakdown Hypothesis, the mechanical failure in the trucks or the cargo plane will cause a delay.
In case of Disturbance Hypothesis, a "severity" factor will first simulate the cancellation of the next race. If the next race is cancelled, then the material will be transported to the following race. This leg of delivery again experiences another disturbance of lesser severity. Note: the cancellation case might not occur in 500 iterations or may not happen even in 5000 iterations. Turn the verbose True for the simulate_disturbance() function and run it to see if it happens.

**VALIDATION PHASE**
H₀: Baseline Scenario was executed and the 
