"""
IS597 Spring 2025 - Final Project
F1 Logistics using Monte Carlo Simulation
Author: Rahul Balasubramani(rahulb6) & Anushree Udhayakumar(au11)
To understand the stakes of logistics :
1. https://www.youtube.com/watch?v=n6uWuL4_pDI
2. https://www.youtube.com/watch?v=6OLVFa8YRfM
3. https://www.youtube.com/watch?v=m8p3vRsXz1k
Be sure to check out the map.py too!

Here is how we've designed the RedBull's logistics (Imagine you are the team's Logistics and Risk manager):
- We will prefer roadways transportation through custom trucks if the next race destination is in the same continent
and if the distance between the locations is less than 4000Km; airways in any other case.

TODO: include a suppress_output mode
TODO: combination hypothesis
TODO: configure
TODO: expand results
TODO: race cancellations
TODO: API and cache circuit_dict
TODO: document
"""
import random
import matplotlib.pyplot as plt
from geographiclib.geodesic import Geodesic
import numpy as np
from gen_circuit_details import circuit_dict as circuit_dict # another .py in github
from datetime import datetime

#-------------------------------------------------HELPER FNS-----------------------------------------------------------
def pert_sample(best_case, most_likely, worst_case):
    """
    For our F1 logistics project, this function returns a single expected value but random value everytime.
    Citation: https://real-statistics.com/binomial-and-related-distributions/pert-distribution/
    :param best_case: what we consider the best case (like least time or most speed)
    :param most_likely: what is most-likely to happen
    :param worst_case: what we consider the worst case (like most time or least speed)
    :return: floating value realistic value between best_case and worst_case and closer to most_likely

    >>> ans=pert_sample(10,20,30)
    >>> 10 <= ans <= 30
    True
    >>> type(ans)
    <class 'float'>

    >>> ans = pert_sample(200.456,557,909.321)
    >>> 200.456 <= ans <= 909.321
    True

    >>> ans = pert_sample(200.456,557,909.321)
    >>> type(ans)
    <class 'float'>
    """
    alpha = 4 * (most_likely - best_case) / (worst_case - best_case) + 1
    beta = 4 * (worst_case - most_likely) / (worst_case - best_case) + 1

    sample = random.betavariate(alpha, beta)  # returns float
    return best_case + sample * (worst_case-best_case)

def calculate_distance(lat1, lon1, lat2, lon2) -> float:
    """
    This function takes inputs of coordinates(lat-long) and computes the great-circle distance between.
    The expected distance between 2 coordinates were coded using https://www.calculator.net/distance-calculator.html?la1=-37.8497&lo1=144.968&la2=31.3389&lo2=121.2189&lad1=38&lam1=53&las1=51.36&lau1=n&lod1=77&lom1=2&los1=11.76&lou1=w&lad2=39&lam2=56&las2=58.56&lau2=n&lod2=75&lom2=9&los2=1.08&lou2=w&type=3&ctype=dec&x=Calculate#latlog
    :param lat1: Race location A latitude
    :param lon1: Race location A longitude
    :param lat2: Race location B latitude
    :param lon2: Race location B longitude
    :return: floating value that denotes the distance between the two points in km.

    >>> round(calculate_distance(-37.8497, 144.968, 31.3389, 121.2189), 1)
    8047.2

    >>> round(calculate_distance(31.3389, 121.2189, 34.8431, 136.5419), 1)  # Shanghai → Suzuka
    1480.6

    >>> round(calculate_distance(25.4892, 51.4531, 24.4672, 54.6031), 2) #lusail -> yas marina
    337.58
    """
    distance_meters = Geodesic.WGS84.Inverse(lat1, lon1, lat2, lon2)['s12']
    distance_km = distance_meters / 1000
    return distance_km

def fabrication():
    """
    This function is meant to return the total time it takes to fabricate the spare part(s)
    :return: floating value representing part's fabrication time - random each time.
    >>> time = fabrication()
    >>> isinstance(time, float)
    True
    >>> 12 <= time <= 36
    True

    >>> fabrication(10, 12, 36)
    Traceback (most recent call last):
    ...
    TypeError: fabrication() takes 0 positional arguments but 3 were given
    """
    fabrication_time = pert_sample(12, 18, 36)
    return fabrication_time

def valid_tracks():
    """
    This function is mean to pick random consecutive tracks from the dictionary - random each time
    :return: track_A and track_B's name, raceDate, Continent

    >>> result = valid_tracks()
    >>> isinstance(result, tuple) and len(result) == 6 # it returns 6 items
    True

    >>> result = valid_tracks()
    >>> track_A_name = result[0]
    >>> track_B_name = result[3]
    >>> track_A_date = result[1]
    >>> track_B_date = result[4]

    >>> # Check that track_B is the next race after track_A in circuit_dict order
    >>> circuit_names = list(circuit_dict.keys())
    >>> index_A = circuit_names.index(track_A_name)
    >>> circuit_names[index_A + 1] == track_B_name
    True

    >>> # Validate race dates match what's in the dictionary
    >>> track_A_date == circuit_dict[track_A_name]['RaceDate']
    True
    >>> track_B_date == circuit_dict[track_B_name]['RaceDate']
    True
    """
    circuit_names = list(circuit_dict.keys())

    # Pick a random index except the last one
    index = random.randint(0, len(circuit_names) - 2) #no last track

    track_A = circuit_names[index]
    track_B = circuit_names[index + 1]

    track_A_info = circuit_dict[track_A]
    track_B_info = circuit_dict[track_B]

    return (track_A, track_A_info["RaceDate"], track_A_info["Continent"],
            track_B, track_B_info["RaceDate"], track_B_info["Continent"])

def transport_time(loc_A, loc_B, mode):
    """
    Calculates transport time (in hours) from loc_A to loc_B. Simulator decided the mode (road/air) and sent it here.
    :param loc_A: name of circuit A, later changed to "HQ"
    :param loc_B: name of circuit B
    :param mode: air or road
    :return: time in hours (float)

    >>> time = transport_time("Hungaroring", "Circuit Zandvoort", "road") # both race tracks are in Europe
    >>> isinstance(time, float)
    True

    >>> 3 <= time # Hungaroring to Zandvoort by truck should be more than 3
    True

    >>> time_hq = transport_time("HQ", "Circuit Zandvoort", "air")
    >>> time_track = transport_time("Hungaroring", "Circuit Zandvoort", "road")
    >>> time_hq > time_track  # HQ to Zandvoort via air takes lesser time, because airways transport is quicker
    False

    >>> transport_time("Circuit de Monaco", "Circuit de Barcelona-Catalunya", "boat")  # doctest: +ELLIPSIS
    Traceback (most recent call last):
    ...
    ValueError: Unsupported mode: use 'road' or 'air'.
    """
    # HQ coordinates (Milton Keynes)
    hq_lat, hq_lon = 52.0406, -0.7594

    # Get coordinates for location A
    if loc_A == "HQ":
        lat_A, lon_A = hq_lat, hq_lon
    else:
        lat_A = circuit_dict[loc_A]["Latitude"]
        lon_A = circuit_dict[loc_A]["Longitude"]

    # Get coordinates for location B
    lat_B = circuit_dict[loc_B]["Latitude"]
    lon_B = circuit_dict[loc_B]["Longitude"]

    # Calculate distance in kilometers
    distance_km = calculate_distance(lat_A, lon_A, lat_B, lon_B)

    # Sample speed using PERT
    if mode == "road":
        speed_kmph = pert_sample(100, 80, 48) #most speed - most-likely speed - lowest speed (highways/ interstate)
        # https://dhl-freight-connections.com/en/business/truck-speed-limits-europe/
    elif mode == "air":
        speed_kmph = pert_sample(800, 700, 600) # Air speed (flight portion)

        # Local road speeds for track <-> airport connection
        # https://www.bts.gov/browse-statistical-products-and-data/info-gallery/average-truck-speed-mph-bottleneck-locations
        local_road_speed_kmph = pert_sample(32.19, 40.23, 48.28)

        # assumed distance between track and airport (~20 km *each side, can tweak later if needed)
        local_distance_km_per_leg = 20 #assumed

        # d/s = hrs # Total local road time (both departure + arrival sides)
        local_road_time = (2 * local_distance_km_per_leg) / local_road_speed_kmph

        # Main air transport time
        air_travel_time = distance_km / speed_kmph

        # Total transport time
        """
        loading_unloading_delay is added because when we choose airways, we'd have to load the cargo into trucks, 
        drive them to airports, unload from the trucks, load them into cargo planes, then transport them to the
        destination, unload from the plane at the destination, load them into trucks to transport them to the
        destination tracks. Thus we sample a random number between 4hrs and 10hrs and add them to the total travel
        time.
        """
        travel_time_hrs = air_travel_time + local_road_time
        loading_unloading_delay = pert_sample(4, 5, 10)
        travel_time_hrs += loading_unloading_delay

        return round(travel_time_hrs, 2)

    else:
        raise ValueError("Unsupported mode: use 'road' or 'air'.") # this should never occur, because the user does not specify the mode. simulator() does!

    travel_time_hrs = distance_km / speed_kmph
    return round(travel_time_hrs, 2)

#--------------------------------------------SIMULATORS----------------------------------------------------------------
#def simulate_crash(track_A, track_B, breakdown, disturbance):
def simulate_crash(track_A, track_B, mode, verbose=False):
    """
    Simulates a crash scenario where spare parts need to be fabricated and flown from HQ to the next track.
    Always assumes air transport due to urgency.
    :param: track_A: name of circuit A
    :param: track_B: name of circuit B
    :return: total delayed transportation time

    >>> simulate_crash("this circuit does not exist", "Baku City Circuit", "air", verbose=True)
    Traceback (most recent call last):
    ...
    KeyError: 'this circuit does not exist'

    >>> t = simulate_crash("Hungaroring", "Circuit Zandvoort", "road", verbose=True) # doctest: +ELLIPSIS
    Crash at Hungaroring. Spare parts flown from HQ to Circuit Zandvoort.
    Transport time (transport time from [track_A to track_B] and [HQ to track_B incl fabrication]): ...
    Total recovery and delivery time: ...

    >>> isinstance(t, float)
    True

    >>> simulate_crash("Hungaroring", "Circuit Zandvoort", "something that should not be given", verbose=True)
    Traceback (most recent call last):
    ...
    ValueError: Unsupported mode: use 'road' or 'air'.
    """
    print(f"Crash at {track_A}. Spare parts flown from HQ to {track_B}.")

    # Fabrication time
    fabrication_time = fabrication()  # Returns random fabrication time each time

    # calculating time for track_A to track_B - moving the non-damaged parts
    base_delivery_time_A = transport_time(track_A, track_B, mode)

    # calculating time for HQ to track_B - getting new parts
    base_delivery_time_B = transport_time("HQ", track_B, "air")
    base_delivery_time_B += fabrication_time
    print(f"Transport time (transport time from [track_A to track_B] and [HQ to track_B incl fabrication]): {base_delivery_time_A:.2f} hrs and {base_delivery_time_B:.2f} hrs")

    # if any delay, the delay would be caused by which ever leg of transportation took the longest
    total_delay_time = max(base_delivery_time_B, base_delivery_time_A)

    print(f"Total recovery and delivery time: {total_delay_time:.2f} hrs")
    return round(total_delay_time, 2)

def simulate_breakdown(track_A, track_B, mode, verbose=False):
    """
    Simulates breakdown of carrier: trucks (road) or cargo planes (air). Adds additional delay if breakdown occurs.
    :param track_A: name of circuit A
    :param track_B: name of circuit B
    :param mode: air or road
    :return: total delayed transportation time because of breakdown

    >>> simulate_breakdown("Circuit de Monaco", "Circuit de Barcelona-Catalunya", "water", verbose=True)
    Traceback (most recent call last):
    ...
    ValueError: Unsupported mode: use 'road' or 'air'.

    >>> simulate_breakdown("this circuit does not exist", "Baku City Circuit", "air", verbose=True)
    Traceback (most recent call last):
    ...
    KeyError: 'this circuit does not exist'

    >>> t = simulate_breakdown("Circuit de Monaco", "Circuit de Barcelona-Catalunya", "road", verbose=True) # doctest: +ELLIPSIS
    Breakdown occurred during transport (ROAD)! Extra delay: ...

    >>> isinstance(t, float)
    True
    """
    # Base transport time
    base_delivery_time = transport_time(track_A, track_B, mode)

    # Set breakdown probability and PERT parameters
    if mode == "road":
        best, most_likely, worst = 1, 3, 12  # best case there is just 1hr of delay, worst case being 12hrs
    elif mode == "air":
        best, most_likely, worst = 2, 3, 12

    else:
        raise ValueError("Unsupported mode: use 'road' or 'air'")

    # Simulate breakdown occurrence
    breakdown_delay = pert_sample(best, most_likely, worst)
    print(f"Breakdown occurred during transport ({mode.upper()})! Extra delay: {breakdown_delay:.2f} hrs")
    total_time = base_delivery_time + breakdown_delay
    return round(total_time, 2)


def simulate_disturbance(track_A, track_B, mode, verbose=True):
    """
    Simulates if a disturbance occurs (customs delay, security delay, weather).
    Adds disturbance delay on top of normal transport time.
    :param track_A: name of circuit A
    :param track_B: name of circuit B
    :param mode: air or road
    :return: total delayed transportation time because of disturbance

    >>> simulate_disturbance("Circuit de Monaco", "Circuit de Barcelona-Catalunya", "water", verbose=True)
    Traceback (most recent call last):
    ...
    ValueError: Unsupported mode: use 'road' or 'air'.

    >>> simulate_disturbance("this circuit does not exist", "Baku City Circuit", "air", verbose=True)
    Traceback (most recent call last):
    ...
    KeyError: 'this circuit does not exist'

    >>> t = simulate_disturbance("Circuit de Monaco", "Circuit de Barcelona-Catalunya", "road", verbose=True) # doctest: +ELLIPSIS
    Disturbance occurred during transport (ROAD)!
    Duration: ..., Severity: ..., Extra delay: ...

    >>> isinstance(t, float)
    True
    """
    race_cancellation_flag = False
    severity = pert_sample(0.1, 0.2, 1.1)  # Severity multiplier
    if severity == 1.1:
        if verbose:
            print("Race cancelled due to extreme disturbance.")
            race_cancellation_flag = True
        track_B, mode = race_cancellation_simulator(track_A)

    # Base transport time
    base_transport_time = transport_time(track_A, track_B, mode)
    # Duration of disturbance in hours
    duration = pert_sample(2, 6, 48)

    severity = pert_sample(0.1, 0.2, 1)  # Severity multiplier
    disturbance_delay = duration * severity

    total_time = base_transport_time + disturbance_delay

    if verbose:
        print(f"Disturbance occurred during transport ({mode.upper()})!")
        print(f"Duration: {duration:.2f} hrs, Severity: {severity:.2f}, Extra delay: {disturbance_delay:.2f} hrs")

    return round(total_time, 2), race_cancellation_flag


def race_cancellation_simulator(track_A):
    """
    If race at track_B is cancelled, this finds track_C (track_A + 2) and determines transport mode.
    """
    circuit_names = list(circuit_dict.keys())
    index = circuit_names.index(track_A)

    # handle edge case if track_A is second-last or last
    if index + 2 >= len(circuit_names):
        raise IndexError("Not enough races left in the calendar to skip to track C.")

    track_C = circuit_names[index + 2]
    cont_A = circuit_dict[track_A]['Continent']
    cont_C = circuit_dict[track_C]['Continent']

    lat_A = circuit_dict[track_A]['Latitude']
    lon_A = circuit_dict[track_A]['Longitude']
    lat_C = circuit_dict[track_C]['Latitude']
    lon_C = circuit_dict[track_C]['Longitude']

    dist = calculate_distance(lat_A, lon_A, lat_C, lon_C)

    if cont_A == cont_C and dist <= 4000:
        mode = "road"
    else:
        mode = "air"
    return track_C, mode # will be received as track_B

#---------------------------------------THE SIMULATOR that calls other simulators---------------------------------------
def simulator(crash, breakdown, disturbance, verbose=False):
    """
    Simulates transport between two consecutive F1 races. Handles crash recovery, breakdowns, and disturbances.
    Dynamically chooses transport mode (road or air) based on distance + continent.
    :param crash: 0 or 1. If 1, simulates a crash at the source track that requires spare parts delivery from HQ.
    :param breakdown: 0 or 1. If 1, simulates a breakdown delay during normal transport.
    :param disturbance: 0 or 1. If 1, simulates an external disturbance such as customs or weather delay.

    :return: float. Total time (in hours) taken for transport including base time and any applicable delays.
    """
    # Get tracks and their information
    (track_A, track_A_date, track_A_continent,
     track_B, track_B_date, track_B_continent) = valid_tracks()

    # Convert race dates to datetime
    track_A_date_dt = datetime.strptime(track_A_date, "%Y-%m-%d")
    track_B_date_dt = datetime.strptime(track_B_date, "%Y-%m-%d")

    # Calculate days between races
    days_between = (track_B_date_dt - track_A_date_dt).days

    # Decide transport max hours
    if days_between == 7:
        max_allowed_hours = 58
    else:
        max_allowed_hours = 65

    # Get coordinates
    lat_A = circuit_dict[track_A]["Latitude"]
    lon_A = circuit_dict[track_A]["Longitude"]
    lat_B = circuit_dict[track_B]["Latitude"]
    lon_B = circuit_dict[track_B]["Longitude"]

    # Calculate distance
    distance_km = calculate_distance(lat_A, lon_A, lat_B, lon_B)

    # Decide mode based on distance and continent
    if track_A_continent == track_B_continent and distance_km <= 4000:
        mode = "road"
    else:
        mode = "air"

    print(f"\n--- Simulation for {track_A} → {track_B} ---")
    print(f"Race A date: {track_A_date} ({track_A_continent})")
    print(f"Race B date: {track_B_date} ({track_B_continent})")
    print(f"Days between races: {days_between}")
    print(f"Distance between tracks: {distance_km:.2f} km")
    print(f"Transport mode decided: {mode.upper()}")
    print(f"Max allowed hours: {max_allowed_hours}")

    # Now simulate based on hypothesis
    if crash == 0 and breakdown == 0 and disturbance == 0:
        # Pure baseline transport
        total_time = transport_time(track_A, track_B, mode)
        #print(f"Transport time (no crash, no breakdown, no disturbance): {total_time} hrs")

    elif crash == 1 and breakdown == 0 and disturbance == 0:
        # Crash case: fabrication + HQ-to-trackB transport + optional delays
        total_time = simulate_crash(track_A, track_B, mode)
        #print(f"Total time after crash scenario: {total_time} hrs")

    elif crash == 0 and breakdown == 1 and disturbance == 0:
        # Breakdown case: trackA to trackB with breakdown delay
        total_time = simulate_breakdown(track_A, track_B, mode)
        #print(f"Total time after breakdown scenario: {total_time} hrs")

    elif crash == 0 and breakdown == 0 and disturbance == 1:
        # Disturbance case: trackA to trackB with disturbance delay
        total_time, race_cancellation_flag = simulate_disturbance(track_A, track_B, mode)
        if race_cancellation_flag:
            max_allowed_hours = 65
        #print(f"Total time after disturbance scenario: {total_time} hrs")
    """
    elif crash == 1 and breakdown == 1 and disturbance == 0:
        total_time = max(simulate_crash(track_A, track_B, mode), simulate_breakdown(track_A, track_B, mode))
    """
    # Final check against allowed max hours
    if total_time <= max_allowed_hours:
        print("Transport fits within allowed time limit.")
    else:
        print("Transport exceeds allowed time limit.")

    return total_time

#--------------------------------------------------VISUALIZERS----------------------------------------------------------
def plot_convergence(results, hypothesis_name):
    """
    Plots a convergence graph showing the running average of delivery times over simulations.
    "Running average" or "running mean" refers to the mean value we get as simulations increase. It denotes, how
    the mean value progresses over time as random values get generated.

    :param results: list[float] - A list of delivery times (in hours) from repeated simulation runs.
    :param hypothesis_name: str. A label indicating which hypothesis/scenario the data corresponds to.

    :return: displays a matplotlib plot with reference lines for 58 and 70 hour thresholds.

    how to do doctest: don't or test for any calculations it does or test the return object of this function
    """
    running_avg = np.cumsum(results) / np.arange(1, len(results) + 1)

    plt.figure(figsize=(8,6))
    plt.plot(running_avg, label='Running Average')
    plt.axhline(58, color='red', linestyle='--', label='58 Hour Target')
    plt.axhline(65, color='green', linestyle='--', label='65 Hour Target')
    plt.title(f"Convergence Plot\n{hypothesis_name}", fontsize=14)
    plt.xlabel("Number of Simulations", fontsize=12)
    plt.ylabel("Average Delivery Time (hours)", fontsize=12)
    plt.legend()
    plt.grid(True, linestyle='--', alpha=0.7)
    plt.show()

def plot_histogram(results, hypothesis_name):
    """
    Plots a histogram of delivery times to visualize the distribution of simulation results.
    :param results: list[float]. A list of delivery times (in hours) from simulation runs
    :param hypothesis_name: str. A label describing the simulation scenario

    :return: displays a histogram with ref lines for 58 (road, incl buffer) and 70 (air, incl buffer) hr thresholds.
    """
    plt.figure(figsize=(8,6))
    plt.hist(results, bins=15, color='skyblue', edgecolor='black')
    plt.axvline(x=58, color='red', linestyle='--', linewidth=2, label='58 Hour Target')
    plt.axvline(x=65, color='green', linestyle='--', linewidth=2, label='65 Hour Target')
    plt.title(f"Delivery Time Distribution\n{hypothesis_name}", fontsize=14)
    plt.xlabel("Delivery Time (hours)", fontsize=12)
    plt.ylabel("Frequency", fontsize=12)
    plt.legend()
    plt.grid(True, linestyle='--', alpha=0.7)
    plt.show()

if __name__ == "__main__":
    exceeding_cases = []

    # Ask user for number of simulations
    n_simulations = int(input("Enter the number of simulations to run per hypothesis: "))

    # Updated hypotheses — only focus on crash, breakdown, disturbance
    hypotheses = {
        "Baseline (no crash, no breakdown, no disturbance)": (0, 0, 0),
        "Crash only": (1, 0, 0),
        "Breakdown only": (0, 1, 0),
        "Disturbance only": (0, 0, 1),
        #"Crash+Breakdown": (1, 1, 0)
    }

    for hypo_name, params in hypotheses.items():
        crash, breakdown, disturbance = params
        results = []

        for _ in range(n_simulations):
            time_taken = simulator(crash=crash, breakdown=breakdown, disturbance=disturbance)
            results.append(time_taken)

        avg_time = round(np.mean(results), 2)
        min_time = round(np.min(results), 2)
        max_time = round(np.max(results), 2)
        std_dev = round(np.std(results), 2)

        print("\n=== Hypothesis:", hypo_name, "===")
        print(f"Simulations run: {n_simulations}")
        print(f"Average Time: {avg_time} hrs")
        print(f"Minimum Time: {min_time} hrs")
        print(f"Maximum Time: {max_time} hrs")
        print(f"Standard Deviation: {std_dev} hrs")
        print("=" * 40)

        plot_histogram(results, hypo_name)
        plot_convergence(results, hypo_name)
