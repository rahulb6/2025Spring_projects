**FORMULA ONE LOGISTICS FOR RED BULL RACING**

Formula One is as much a race off the track as it is on it. Each F1 season spans from March to December, with races scheduled across continents - including North America, South America, Europe, Australia, and the Middle East. The limited downtime between races poses a tremendous challenge in transporting critical and non-critical cargo across the globe. The equipment that must arrive on time includes **spare parts, pit stop jacks, telemetry and communication equipment, broadcasting setups, construction gear for motorhomes, tools, hospitality furniture (tables, chairs, cutlery), and more**. With anywhere between **2 days to 1 week** available for turnaround, Formula One teams partner with logistics giants like **DHL** and **Ceva Logistics** to execute this operation with surgical precision.

Pre-Season Setup:
Before the first Grand Prix of the year, teams pre-position **non-critical equipment** via **sea freight** to key international hubs. From there, these materials are distributed to race venues using a combination of **air freight** (cargo planes) and **road freight** (specialized trucks).

Race Weekend Timing:
Each race happens on **Sunday**, with **qualifying sessions** on **Saturday** or **Friday** (in sprint weekends), and promotional or media events beginning as early as **Thursday**. This schedule gives teams **Wednesday and Thursday** to build and organize the garage, pit wall, and hospitality areas.

The real logistical test comes during:
* **Double-Headers**: two races on back-to-back weekends.
* **Triple-Headers**: three consecutive race weekends.
In these scenarios, cargo must be disassembled after Sunday’s race and transported overnight. The race may end at **1:00 PM** or as late as **1:00 AM**, leaving a transport window of roughly **48–58 hours** depending on local regulations and proximity. Although more time is available between spaced-out races, teams **do not take the full week** - doing so would be inefficient and risky. For this simulation, we use **65 hours as the upper limit** for all logistics scenarios to reflect the actual operational benchmark.

**DESIGN PHASE**  
**Hypotheses**  
This simulation explores multiple real-world scenarios Red Bull Racing could face when transporting critical equipment between Formula 1 races, based on the 2025 calendar [4]. Each hypothesis reflects a plausible operational challenge in tight race-to-race turnaround windows.    
**H₀: Baseline Scenario (Validation Hypothesis)**: No crash occurred in the previous race, no breakdowns during transport, and no external disturbances. This serves as a reference case to validate the normal logistics pipeline under ideal conditions.    
**H₁: Crash and Spare Part Depletion**: A crash occurred at the previous race, and the team's spare parts inventory has been exhausted. New components must be fabricated at Red Bull’s headquarters in **Milton Keynes** and transported to the next race venue in time for assembly.    
**H₂: Breakdown During Transport**: A mechanical failure occurs during transport - either in road-based trucking or air cargo - causing delays. The simulation models the time taken to resolve the breakdown and resume delivery.    
**H₃: Unplanned External Disturbance**: Unexpected delays arise from events such as local protests, customs issues, or adverse weather all of which could lead to race cancellations. These are modeled using a **severity multiplier** which gets multiplied with base **disturbance duration** to reflect real-world variability of different disturbances. This hypothesis is meant to be general to compensate for all other misfortunes we did not design within this system.  

**Simulation Setup**  
Fixed Variables:
  * Focused team: Red Bull Racing
  * Headquarters: Milton Keynes, UK
  * Reference calendar: F1 2025 schedule
  * Delivery deadline: 58 hours for standard triple/double-headers; 65 hours for longer windows
  
Randomized Variables (with PERT distributions[5]):
  * Roadway and airway speeds [7][8][9]
  * Fabrication time (for parts post-crash)
  * Breakdown duration
  * Disturbance duration and severity multiplier

We chose **PERT distributions** for randomization because they allow modeling of uncertainty using **best-case, most-likely, and worst-case** estimates - which we feel is a good fit for logistics scenarios. It also allowed for those values we weren't able to find, such as the fabrication time for various parts. The facility to define a range of values and cause the randomization to skew towards the most likely value, and stay within the worst case and worst case values made PERT both intuitive and interpretable.

This simulation system for Red Bull Racing focuses exclusively on in-season logistics, modeling transport between races via roadways and airways. While pre-season shipments, handled through waterways fall outside the scope of this project. The simulation initiates once a race concludes. Based on the date of the next race, the system calculates whether there is a tight turnaround window (58 hours) as in the case of double-headers or triple-headers, or a more flexible window (65 hours) when no race is scheduled the following weekend. 
Next, the simulator evaluates transportation mode. If the next race is on the **same continent and the distance between tracks is under 4000 km**, road transport is preferred. Otherwise, the system defaults to air transport. This logic aligns with real-world F1 logistics practices, ensuring that the simulation mimics operational decisions made by logistics teams under time and distance constraints with sustainability in mind.

Reasoning Behind Simulation Constraints and Hypothesis Design
1. Roadways: Same Continent Constraint: For material to be transported efficiently via road, the presence of a viable and connected road network is essential. Thus, we only consider road transport when the next race is on the same continent as the previous one. 

2. 4000 km Distance Threshold: One might ask, Why not allow road transport for distances beyond 4000 km, especially if time allows? While it is technically possible to cover longer distances by road, such an approach would be inefficient and environmentally unsustainable. Formula One and its partners (e.g., DHL, Ceva Logistics) are committed to sustainability. Flying cargo over such long distances not only reduces time but also aligns with F1's broader carbon reduction goals by optimizing fuel usage and minimizing continuous overland emissions.

Flow of Events:
1. Crash Hypothesis: When a crash occurs, spare parts must be fabricated and delivered urgently from Red Bull HQ. This is treated as a priority shipment, and thus always uses air transport, regardless of location. Meanwhile, non-damaged components from the previous track are transported based on the standard route logic (road or air).

2. Breakdown Hypothesis: A mechanical failure in the transport vehicle (truck or cargo plane) is simulated. The failure is addressed and the delivery resumes after a while. The resulting delay is sampled using a PERT distribution to reflect the randomness in breakdown recovery duration.

3. Disturbance Hypothesis: Simulates events such as customs delays, protests, or severe weather. A "severity factor" determines the scale of the disturbance. If the severity exceeds a threshold (1 in our case), the following race is considered cancelled, and logistics are re-routed to the race after that. The new route also experiences a reduced disturbance to reflect real-world handling of back-to-back logistical shifts.
Note: This cancellation event is rare and might not appear even in 5000 simulation runs. For testing, set verbose=True in the simulate_disturbance() function to observe such occurrences when they occur.

**VALIDATION PHASE**  
In the baseline scenario, where no crash, breakdown, or external disturbance occurred, the logistics system completed transportation in an average of 15.63 hours (note that this value may vary slightly with each run) across 500 simulations. Importantly, not a single run exceeded the assigned deadlines. This validates that the transport decision system - where roadways are preferred under specific conditions and airways otherwise - is effective and robust under normal operating circumstances, with a 100% success rate in meeting time constraints. The results of other hypotheses—such as crash recovery, breakdowns, or disturbances - will be assessed relative to this baseline, allowing us to quantify the additional time and risk introduced by each specific challenge (hypothesis) in the logistics design.

**EXPERIMENT PHASE**  
Upon running the simulation for all hypothesis, these are the results and interpretations:
(Note that there is no numbers mentioned here, because they might differ every time you run the program)

1. Minimum Delivery Time Comparison: When analyzing the minimum delivery times across scenarios, we observe that both H2: Breakdown and H3: Disturbance cases yield delivery times that are close to the H0: Baseline scenario. However, in the case of a H1: Crash, the minimum delivery time is significantly higher. We believe,that this deviation is primarily attributed to the fabrication time required to replace damaged and depleted components, which inherently adds a delay even under the best conditions.
2. Convergence Behavior (Mean Delivery Time): The mean delivery time or convergence point across simulations reinforces this pattern. While H2: Breakdowns and H3: Disturbances introduce minor delays—adding just a few hours over the H0: Baseline - the H1: Crash scenario results in a notably higher mean delivery time. This again highlights the impact of fabrication on the overall delivery duration.

Note: The assumed values and the thresholds can be changed by accessing the config.yaml file

**REFERENCES:**  
To understand the stakes of logistics :
1. https://www.youtube.com/watch?v=n6uWuL4_pDI
2. https://www.youtube.com/watch?v=6OLVFa8YRfM
3. https://www.youtube.com/watch?v=m8p3vRsXz1k  
Be sure to check out the map.py too!
4. 2025 Race calendar: https://www.formula1.com/en/racing/2025
5. PERT: https://real-statistics.com/binomial-and-related-distributions/pert-distribution/
6. Geodesic s12: https://geographiclib.sourceforge.io/html/python/examples.html
7. Article used to assume roadways speed range: https://dhl-freight-connections.com/en/business/truck-speed-limits-europe/
8. Article used to assume roadways speed within city limits: https://www.bts.gov/browse-statistical-products-and-data/info-gallery/average-truck-speed-mph-bottleneck-locations
9. Article used to assume cargo plane speeds: https://www.freightcourse.com/largest-cargo-planes/  
Other references:
10. https://www.calculator.net/distance-calculator.html?la1=-37.8497&lo1=144.968&la2=31.3389&lo2=121.2189&lad1=38&lam1=53&las1=51.36&lau1=n&lod1=77&lom1=2&los1=11.76&lou1=w&lad2=39&lam2=56&las2=58.56&lau2=n&lod2=75&lom2=9&los2=1.08&lou2=w&type=3&ctype=dec&x=Calculate#latlog
