"""
IS597 Spring 2025 - Final Project
F1 Logistics using Monte Carlo Simulation: Core Functions
Author: Rahul Balasubramani(rahulb6) & Anushree Udhayakumar(au11)
"""

import random
import matplotlib.pyplot as plt
from geographiclib.geodesic import Geodesic
import numpy as np
from gen_circuit_details import circuit_dict as circuit_dict
from datetime import datetime


# PERT function to generate sample
def pert_sample(best_case, most_likely, worst_case):
    """
    For our F1 logistics project, this function returns a single expected value
    using the classic PERT formula used to estimate values like travel time,
    fabrication time, or disturbance duration where we know the best, most likely,
    and worst-case scenarios.

    Citation:
    https://real-statistics.com/binomial-and-related-distributions/pert-distribution/
    This version avoids randomness and gives a stable, realistic estimate.
    """
    expected_value = (best_case + 4 * most_likely + worst_case) / 6
    return expected_value

"""
#Calculate distance between 2 points
def calculate_distance(coord1, coord2):
    return geodesic(coord1, coord2).km
"""
def calculate_distance(lat1, lon1, lat2, lon2) -> float:
    """
    This function takes inputs of coordinates(lat-long) and computes the great-circle distance between.
    :param lat1: Race location A latitude
    :param lon1: Race location A longitude
    :param lat2: Race location B latitude
    :param lon2: Race location B longitude
    :return: floating value that denotes the distance between the two points in km.
    TODO: make sure the return value makes sense in km
    """
    distance_meters = Geodesic.WGS84.Inverse(lat1, lon1, lat2, lon2)['s12']
    distance_km = distance_meters / 1000
    return distance_km

def fabrication():
    """
    This function is meant to return the total time it takes to fabricate the spare part(s)
    :return:
    TODO: what distribution does fabrication follow?
    """
    fabrication_time = pert_sample(12, 18, 36)
    return fabrication_time

def transport_time(loc_A, loc_B, mode):
    """
    Calculates transport time (in hours) from loc_A to loc_B.
    Uses PERT-sampled speed and geodesic distance.

    :param loc_A: 'HQ' or name of circuit A
    :param loc_B: name of circuit B
    :param mode: 'road' (default), or 'air' if needed later
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
        speed_kmph = pert_sample(100, 80, 48) #we have citation for this
    elif mode == "air":
        speed_kmph = pert_sample(800, 700, 600)  #no citation for this
    else:
        raise ValueError("Unsupported mode: use 'road' or 'air'.")

    # Time = distance / speed
    travel_time_hrs = distance_km / speed_kmph
    return round(travel_time_hrs, 2)


def simulate_crash(track_A, track_B, breakdown, disturbance):
    """
    Simulates a crash scenario where spare parts need to be fabricated and flown from HQ to the next track.
    Always assumes air transport due to urgency.
    """

    print(f"Crash at {track_A}. Spare parts flown from HQ to {track_B}.")

    # 1. Fabrication time
    fabrication_time = fabrication()  # Assume you already have a fabrication() function returning sampled hours
    print(f"Fabrication time: {fabrication_time:.2f} hrs")

    # 2. Transport time from HQ to Track B (always by air)
    delivery_time = transport_time("HQ", track_B, "air")
    print(f"Transport time (air): {delivery_time:.2f} hrs")

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
    print(f"Total recovery and delivery time: {total_crash_time:.2f} hrs")

    return round(total_crash_time, 2)


def simulate_breakdown(track_A, track_B, mode):
    """
    Simulates breakdown of carrier: trucks (road) or cargo planes (air).
    Adds additional delay if breakdown occurs.
    """

    # Base transport time
    delivery_time = transport_time(track_A, track_B, mode)

    # Set breakdown probability and PERT parameters
    if mode == "road":
        breakdown_prob = 0.02  # 2% chance truck breakdown
        best, most_likely, worst = 2, 3, 12  # Delay times in hours
    elif mode == "air":
        breakdown_prob = 0.001  # 0.1% chance cargo plane issue
        best, most_likely, worst = 2, 3, 12  # Slightly shifted delay times
    else:
        raise ValueError("Mode must be 'road' or 'air'.")

    # Simulate breakdown occurrence
    if np.random.binomial(1, breakdown_prob):
        breakdown_delay = pert_sample(best, most_likely, worst)
        print(f"Breakdown occurred during transport ({mode.upper()})! Extra delay: {breakdown_delay:.2f} hrs")
        total_time = delivery_time + breakdown_delay
        return round(total_time, 2)
    else:
        print(f"No breakdown during transport ({mode.upper()}).")
        return round(delivery_time, 2)

def simulate_disturbance(track_A, track_B, mode):
    """
    Simulates if a disturbance occurs (customs delay, security delay, weather).
    Adds disturbance delay on top of normal transport time.
    """

    # Base transport time
    base_transport_time = transport_time(track_A, track_B, mode)

    disturbance_prob = 0.001  # 10% chance of disturbance

    if np.random.binomial(1, disturbance_prob):
        # If disturbance occurs
        duration = pert_sample(2, 6, 48)  # Duration of disturbance in hours
        severity = pert_sample(0.1, 0.2, 1)  # Severity multiplier
        disturbance_delay = duration * severity

        total_time = base_transport_time + disturbance_delay

        print(f"Disturbance occurred during transport ({mode.upper()})! Extra delay: {disturbance_delay:.2f} hrs")
        return round(total_time, 2)
    else:
        print(f"No disturbance during transport ({mode.upper()}).")
        return round(base_transport_time, 2)

def valid_tracks():
    circuit_names = list(circuit_dict.keys())

    # Pick a random index except the last one
    index = random.randint(0, len(circuit_names) - 2)

    track_A = circuit_names[index]
    track_B = circuit_names[index + 1]

    track_A_info = circuit_dict[track_A]
    track_B_info = circuit_dict[track_B]

    return (track_A, track_A_info["RaceDate"], track_A_info["Continent"],
            track_B, track_B_info["RaceDate"], track_B_info["Continent"])

def simulator(crash, breakdown, disturbance):
    """
    This function simulates transport based on crash, breakdown, disturbance.
    Now transport mode is dynamically decided based on continents.
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
        max_allowed_hours = 68
    else:
        max_allowed_hours = 85

    # Get coordinates
    lat_A = circuit_dict[track_A]["Latitude"]
    lon_A = circuit_dict[track_A]["Longitude"]
    lat_B = circuit_dict[track_B]["Latitude"]
    lon_B = circuit_dict[track_B]["Longitude"]

    # Calculate distance
    distance_km = calculate_distance(lat_A, lon_A, lat_B, lon_B)

    # Decide mode
    if track_A_continent == track_B_continent and distance_km <= 7000:
        mode = "road"
    else:
        mode = "air"

    print(f"\n--- Simulation for {track_A} → {track_B} ---")
    print(f"Race A date: {track_A_date} ({track_A_continent})")
    print(f"Race B date: {track_B_date} ({track_B_continent})")
    print(f"Days between races: {days_between}")
    print(f"Transport mode decided: {mode.upper()}")
    print(f"Max allowed hours: {max_allowed_hours}")

    total_time = 0

    if crash == 0 and breakdown == 0 and disturbance == 0:
        base_time = transport_time(track_A, track_B, mode)
        print(f"Transport time (no crash, no breakdown, no disturbance): {base_time} hrs")

        # Check if base_time <= max_allowed_hours
        if base_time <= max_allowed_hours:
            print("Transport fits within allowed time limit.")
        else:
            print("Transport exceeds allowed time limit.")

        return base_time

    elif crash == 1 and breakdown ==0 and disturbance == 0:
        total_delay = simulate_crash(track_A, track_B, breakdown, disturbance)
        delivery_time = transport_time("HQ", track_B, mode)
        total_time = total_delay + delivery_time
        print(f"Total time after crash scenario: {total_time} hrs")

    elif crash == 0 and breakdown == 1 and disturbance == 0:
        total_delay = simulate_breakdown(track_A, track_B, mode)
        delivery_time = transport_time(track_A, track_B, mode)
        total_time = total_delay + delivery_time
        print(f"Total time after breakdown scenario: {total_time} hrs")

    else:
        total_delay = simulate_disturbance(track_A, track_B, mode)
        delivery_time = transport_time(track_A, track_B, mode)
        total_time = total_delay + delivery_time
        print(f"Total time after disturbance scenario: {total_time} hrs")

    # Final transport check
    if total_time <= max_allowed_hours:
        print("Transport fits within allowed time limit.")
    else:
        print("Transport exceeds allowed time limit.")

    return total_time


def plot_convergence(results, hypothesis_name):
    running_avg = np.cumsum(results) / np.arange(1, len(results) + 1)

    plt.figure(figsize=(8,6))
    plt.plot(running_avg, label='Running Average')
    plt.axhline(68, color='red', linestyle='--', label='68 Hour Target')
    plt.axhline(85, color='green', linestyle='--', label='85 Hour Target')
    plt.title(f"Convergence Plot\n{hypothesis_name}", fontsize=14)
    plt.xlabel("Number of Simulations", fontsize=12)
    plt.ylabel("Average Delivery Time (hours)", fontsize=12)
    plt.legend()
    plt.grid(True, linestyle='--', alpha=0.7)
    plt.show()

def plot_histogram(results, hypothesis_name):
    plt.figure(figsize=(8,6))
    plt.hist(results, bins=15, color='skyblue', edgecolor='black')
    plt.axvline(x=68, color='red', linestyle='--', linewidth=2, label='68 Hour Target')
    plt.axvline(x=85, color='green', linestyle='--', linewidth=2, label='85 Hour Target')
    plt.title(f"Delivery Time Distribution\n{hypothesis_name}", fontsize=14)
    plt.xlabel("Delivery Time (hours)", fontsize=12)
    plt.ylabel("Frequency", fontsize=12)
    plt.legend()
    plt.grid(True, linestyle='--', alpha=0.7)
    plt.show()



"""
if __name__ == "__main__":

    # HYPOTHESIS 0: Baseline scenario - ideal case
    simulator(crash=0, breakdown=0, disturbance=0, mode="road")
    simulator(crash=0, breakdown=0, disturbance=0, mode="air")

    #HYPOTHESIS 1: simulating crash at circuit A, and spare parts being fabricated and dent from HQ to circuit B
    simulator(crash=1, breakdown=0, disturbance=0,mode="road")
    simulator(crash=1, breakdown=0, disturbance=0, mode="air")
    simulator(crash=1, breakdown=1, disturbance=0, mode="road")
    simulator(crash=1, breakdown=1, disturbance=0, mode="air")

    #HYPOTHESIS 2: simulating the occurrence of breakdown
    simulator(crash=0, breakdown=1, disturbance=0, mode="air")
    simulator(crash=0, breakdown=1, disturbance=0, mode="road")

    #HYPOTHESIS 3: simulating the occurrence of disturbance during normal transport
    simulator(crash=0, breakdown=0, disturbance=1, mode="road")
    simulator(crash=0, breakdown=0, disturbance=1, mode="air")
"""
if __name__ == "__main__":
    # Ask user for number of simulations
    n_simulations = int(input("Enter the number of simulations to run per hypothesis: "))

    # Updated hypotheses — only focus on crash, breakdown, disturbance
    hypotheses = {
        "Baseline (no crash, no breakdown, no disturbance)": (0, 0, 0),
        "Crash only": (1, 0, 0),
        #"Crash + Breakdown": (1, 1, 0),
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
