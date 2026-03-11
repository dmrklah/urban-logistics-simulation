"""
Hybrid Simulation of Urban Last-Mile Logistics under Peak Demand
================================================================
BSc Computer Science and Digitization
Module: Advanced Simulation Techniques

This script implements a hybrid simulation combining:
- Discrete Event Simulation (DES) using SimPy
- Monte Carlo sampling for stochastic inputs

Two scenarios are evaluated:
- Scenario A: Normal Day (baseline demand)
- Scenario B: Peak Day (high demand, fixed fleet)
"""

import simpy
import random
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

# ── Configuration ──────────────────────────────────────────────
SIM_DURATION = 480          # Simulated minutes (8-hour operating day)
FLEET_SIZE = 5              # Number of delivery vehicles
NUM_REPLICATIONS = 10       # Monte Carlo replications per scenario

# Travel time ranges (minutes)
WAREHOUSE_TO_HUB = (5, 15)
HUB_TO_CUSTOMER = (10, 30)
PEAK_DELAY_RANGE = (2, 8)   # Additional delay during peak demand

# Order arrival rates (orders per hour)
NORMAL_ARRIVAL_RATE = 8
PEAK_ARRIVAL_RATE = 16


# ── Monte Carlo: Order Arrival Generation ─────────────────────
def generate_order_times(arrival_rate_per_hour):
    """
    Generates stochastic order arrival times using exponential distribution.
    Inter-arrival times are sampled to represent random customer demand.
    """
    times = []
    current = 0

    while current < SIM_DURATION:
        gap = random.expovariate(arrival_rate_per_hour / 60)
        current += gap
        if current < SIM_DURATION:
            times.append(current)

    return times


# ── Vehicle Fleet Resource ─────────────────────────────────────
class VehicleFleet:
    def __init__(self, env, fleet_size):
        self.vehicles = simpy.Resource(env, capacity=fleet_size)


# ── DES: Delivery Process ──────────────────────────────────────
def deliver_order(env, order_id, fleet, metrics, is_peak=False):
    """
    Discrete Event Simulation of a single order delivery.
    Models: warehouse → micro-hub → customer delivery.
    """
    order_start = env.now

    with fleet.vehicles.request() as req:
        yield req

        # Warehouse → Micro-hub
        travel_1 = random.uniform(*WAREHOUSE_TO_HUB)
        yield env.timeout(travel_1)

        # Micro-hub → Customer
        travel_2 = random.uniform(*HUB_TO_CUSTOMER)
        yield env.timeout(travel_2)

        # Additional peak demand delay
        if is_peak:
            delay = random.uniform(*PEAK_DELAY_RANGE)
            yield env.timeout(delay)

    delivery_time = env.now - order_start
    metrics["delivery_times"].append(delivery_time)
    metrics["orders_completed"] += 1


# ── Hybrid Simulation Execution ────────────────────────────────
def run_model(order_rate, is_peak=False):
    """
    Integrates Monte Carlo order arrivals with DES execution.
    Controls model initialisation, event scheduling, and metrics collection.
    """
    env = simpy.Environment()
    fleet = VehicleFleet(env, FLEET_SIZE)

    metrics = {
        "delivery_times": [],
        "orders_completed": 0
    }

    order_times = generate_order_times(order_rate)

    for i, t in enumerate(order_times):
        env.process(deliver_order(env, i, fleet, metrics, is_peak))

    env.run(until=SIM_DURATION)
    return metrics


# ── Scenario Runner ────────────────────────────────────────────
def run_scenario(label, order_rate, is_peak=False):
    """
    Runs multiple replications of a scenario and aggregates results.
    """
    all_avg = []
    all_max = []
    all_completed = []

    for _ in range(NUM_REPLICATIONS):
        result = run_model(order_rate, is_peak)
        if result["delivery_times"]:
            all_avg.append(np.mean(result["delivery_times"]))
            all_max.append(np.max(result["delivery_times"]))
            all_completed.append(result["orders_completed"])

    return {
        "Scenario": label,
        "Average Delivery Time (min)": round(np.mean(all_avg), 2),
        "Max Delivery Time (min)": round(np.mean(all_max), 2),
        "Orders Delivered": round(np.mean(all_completed), 1)
    }


# ── Main Execution ─────────────────────────────────────────────
if __name__ == "__main__":
    print("Running Hybrid Simulation: Urban Last-Mile Logistics")
    print("=" * 55)

    normal = run_scenario("Normal Day", NORMAL_ARRIVAL_RATE, is_peak=False)
    peak   = run_scenario("Peak Day",   PEAK_ARRIVAL_RATE,   is_peak=True)

    # Results table
    df = pd.DataFrame([normal, peak]).set_index("Scenario")
    print("\nResults:")
    print(df.to_string())

    # ── Figure 1: Bar chart – Average Delivery Time ────────────
    fig, ax = plt.subplots(figsize=(7, 5))
    scenarios = [normal["Scenario"], peak["Scenario"]]
    avg_times = [normal["Average Delivery Time (min)"], peak["Average Delivery Time (min)"]]
    colors = ["#A8C4D4", "#4A90B8"]

    bars = ax.bar(scenarios, avg_times, color=colors, width=0.45, edgecolor="black", linewidth=0.6)
    for bar, val in zip(bars, avg_times):
        ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.8,
                str(val), ha="center", va="bottom", fontsize=11, fontweight="bold")

    ax.set_title("Average Delivery Time: Normal vs Peak Day", fontsize=13, fontweight="bold")
    ax.set_xlabel("Scenario", fontsize=11)
    ax.set_ylabel("Average Delivery Time (minutes)", fontsize=11)
    ax.set_ylim(0, max(avg_times) * 1.2)
    ax.grid(axis="y", linestyle="--", alpha=0.6)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    plt.tight_layout()
    plt.savefig("average_delivery_time.png", dpi=150)
    plt.show()
    print("\nChart saved: average_delivery_time.png")
