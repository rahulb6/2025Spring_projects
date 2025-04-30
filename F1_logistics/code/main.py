"""
IS597 Spring 2025 - Final Project
F1 Logistics using Monte Carlo Simulation
Author: Rahul Balasubramani(rahulb6) & Anushree Udhayakumar(au11)
"""
import random
import matplotlib.pyplot as plt
from geographiclib.geodesic import Geodesic
import numpy as np
from gen_circuit_details import circuit_dict as circuit_dict
from datetime import datetime

#-------------------------------------------------HELPER FNS-----------------------------------------------------------
# PERT function to generate sample
def pert_sample(best_case, most_likely, worst_case):
    """
    For our F1 logistics project, this function returns a single expected value but random value everytime.
    Citation: https://real-statistics.com/binomial-and-related-distributions/pert-distribution/
    :param best_case: what we consider the best case (like least time or most speed)
    :param most_likely: what is most-likely to happen
    :param worst_case: what we consider the worst case (like most time or least speed)
    :return: floating value realistic value between best_case and worst_case and closer to most_likely
    TODO: doctests
    """
    alpha = 4 * (most_likely - best_case) / (worst_case - best_case) + 1
    beta = 4 * (worst_case - most_likely) / (worst_case - best_case) + 1

    sample = random.betavariate(alpha, beta)
    return best_case + sample * (worst_case-best_case)

def calculate_distance(lat1, lon1, lat2, lon2) -> float:
    """
    This function takes inputs of coordinates(lat-long) and computes the great-circle distance between.
    :param lat1: Race location A latitude
    :param lon1: Race location A longitude
    :param lat2: Race location B latitude
    :param lon2: Race location B longitude
    :return: floating value that denotes the distance between the two points in km.
    TODO: doctests
    """
    distance_meters = Geodesic.WGS84.Inverse(lat1, lon1, lat2, lon2)['s12']
    distance_km = distance_meters / 1000
    return distance_km

def fabrication():
    """
    This function is meant to return the total time it takes to fabricate the spare part(s)
    :return: floating value representing part's fabrication time - random each time.
    TODO: doctests
    """
    fabrication_time = pert_sample(12, 18, 36)
    return fabrication_time

def valid_tracks():
    """
    This function is mean to pick random consecutive tracks from the dictionary - random each time
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
        local_distance_km_per_leg = 20

        # d/s = hrs # Total local road time (both departure + arrival sides)
        local_road_time = (2 * local_distance_km_per_leg) / local_road_speed_kmph

        # Main air transport time
        air_travel_time = distance_km / speed_kmph

        # Total transport time
        travel_time_hrs = air_travel_time + local_road_time
        travel_time_hrs += 5 # +5 for loading, unloading into and out of the cargo plane
        return round(travel_time_hrs, 2)

    else:
        raise ValueError("Unsupported mode: use 'road' or 'air'.")

    travel_time_hrs = distance_km / speed_kmph
    return round(travel_time_hrs, 2)

#--------------------------------------------SIMULATORS----------------------------------------------------------------
#def simulate_crash(track_A, track_B, breakdown, disturbance):
def simulate_crash(track_A, track_B):
    """
    Simulates a crash scenario where spare parts need to be fabricated and flown from HQ to the next track.
    Always assumes air transport due to urgency.
    :param: track_A: name of circuit A
    :param: track_B: name of circuit B
    :return: total delayed transportation time
    """
    print(f"Crash at {track_A}. Spare parts flown from HQ to {track_B}.")

    # Fabrication time
    fabrication_time = fabrication()  # Returns random fabrication time each time

    # Transport time from HQ to Track B (always by air because if the teams
    # need the part to be flown in from HQ, then 100% of time, it is an emergency and the delivery needs to happen asap.
    # So airways is the better choice)
    base_delivery_time = transport_time("HQ", track_B, "air")
    print(f"Transport time (air): {base_delivery_time:.2f} hrs")

    """
    ------this section was included when we wanted to simulate a crash + breakdown (+ disturbance)------
    # 3. If disturbance happens
    disturbance_delay = 0
    if disturbance:
        disturbance_delay = simulate_disturbance("HQ", track_B, "air")
        print(f"Disturbance delay: {disturbance_delay:.2f} hrs")

    # 4. If breakdown happens (very rare in air)
    breakdown_delay = 0
    if breakdown:
        breakdown_delay = simulate_breakdown("HQ", track_B, "air")
        print(f"Breakdown delay: {breakdown_delay:.2f} hrs")
    
    # 5. Total time
    total_crash_time = fabrication_time + delivery_time + disturbance_delay + breakdown_delay
    """
    total_delay_time = fabrication_time + base_delivery_time

    print(f"Total recovery and delivery time: {total_delay_time:.2f} hrs")
    return round(total_delay_time, 2)


def simulate_breakdown(track_A, track_B, mode):
    """
    Simulates breakdown of carrier: trucks (road) or cargo planes (air). Adds additional delay if breakdown occurs.
    :param track_A: name of circuit A
    :param track_B: name of circuit B
    :param mode: air or road
    :return: total delayed transportation time because of breakdown
    """
    # Base transport time
    base_delivery_time = transport_time(track_A, track_B, mode)

    # Set breakdown probability and PERT parameters
    if mode == "road":
        best, most_likely, worst = 1, 3, 12  # best case there is just 1hr of delay, worst case being 12hrs
    elif mode == "air":
        best, most_likely, worst = 2, 3, 12

    else:
        raise ValueError("Mode must be 'road' or 'air'.")

    # Simulate breakdown occurrence
    breakdown_delay = pert_sample(best, most_likely, worst)
    print(f"Breakdown occurred during transport ({mode.upper()})! Extra delay: {breakdown_delay:.2f} hrs")
    total_time = base_delivery_time + breakdown_delay
    return round(total_time, 2)


def simulate_disturbance(track_A, track_B, mode):
    """
    Simulates if a disturbance occurs (customs delay, security delay, weather).
    Adds disturbance delay on top of normal transport time.
    :param track_A: name of circuit A
    :param track_B: name of circuit B
    :param mode: air or road
    :return: total delayed transportation time because of disturbance
    """
    # Base transport time
    base_transport_time = transport_time(track_A, track_B, mode)

    duration = pert_sample(2, 6, 48)  # Duration of disturbance in hours
    severity = pert_sample(0.1, 0.2, 1)  # Severity multiplier
    disturbance_delay = duration * severity

    total_time = base_transport_time + disturbance_delay

    print(f"Disturbance occurred during transport ({mode.upper()})!")
    print(f"Duration: {duration:.2f} hrs, Severity: {severity:.2f}, Extra delay: {disturbance_delay:.2f} hrs")

    return round(total_time, 2)
#---------------------------------------THE SIMULATOR that calls other simulators---------------------------------------
def simulator(crash, breakdown, disturbance):
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

    # adding buffer times
    """
    for back-to-back races and roadways transport -> loading of paddock material/ priority stuff happens during the 
    race, and thus no considerable downtime during "loading phase". The "unloading phase" is after the trucks
    reach the destination which is not part of the "transportation time" we are calculating. So, no buffer time
    is added for any roadways transportation.
    
    for those races that get deliveries through airways -> the paddock material will have to be packed and loaded into 
    trucks, driven to the airport, unloaded from trucks, loaded onto cargo planes and then is flown to the destination, 
    unloaded into trucks which is then driven to the tracks. So the time for loading and unloading is roughly 5 hours.
    """
    # Decide transport max hours
    if days_between == 7:
        max_allowed_hours = 58
    else:
        max_allowed_hours = (60+5) # where the 5hrs is the loading unloading time

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
        print(f"Transport time (no crash, no breakdown, no disturbance): {total_time} hrs")

    elif crash == 1 and breakdown == 0 and disturbance == 0:
        # Crash case: fabrication + HQ-to-trackB transport + optional delays
        total_time = simulate_crash(track_A, track_B)
        print(f"Total time after crash scenario: {total_time} hrs")

    elif crash == 0 and breakdown == 1 and disturbance == 0:
        # Breakdown case: trackA to trackB with breakdown delay
        total_time = simulate_breakdown(track_A, track_B, mode)
        print(f"Total time after breakdown scenario: {total_time} hrs")

    elif crash == 0 and breakdown == 0 and disturbance == 1:
        # Disturbance case: trackA to trackB with disturbance delay
        total_time = simulate_disturbance(track_A, track_B, mode)
        print(f"Total time after disturbance scenario: {total_time} hrs")

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
        #"Crash + Breakdown": (1, 1, 0), # too unrealistic
        #"Crash + Breakdown + Disturbance": (1, 1, 1), # too unrealistic
        "Breakdown only": (0, 1, 0),
        "Disturbance only": (0, 0, 1)
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
