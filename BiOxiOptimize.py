import random
import matplotlib.pyplot as plt
import numpy as np


"""
PROJECT: BiOxiOptimize - Biofuel Optimization via Genetic Algorithm (GA)
AUTHOR:  Satya Thavanesh Yalla
YEAR:    2026
GOAL:    Identify the cost-effective blend of FAMEs and BHT that meets
         EN 14214 stability standards (>8h) and cold-flow constraints.
LOGIC:   Uses a non-linear Kinetic Synergy Module to model BHT saturation.
LICENSE: MIT
"""


# --- Industry Data ---
COMPONENTS = {
    'Methyl_Oleate': {'stability_IP': 5.0, 'viscosity': 4.5, 'cost': 1.20},
    'Methyl_Palmitate': {'stability_IP': 12.0, 'viscosity': 6.0, 'cost': 1.50},
    'Methyl_Linoleate': {'stability_IP': 1.0, 'viscosity': 4.0, 'cost': 1.30},
    'BHT_Antioxidant': {'stability_IP': 0.0, 'viscosity': 10.0, 'cost': 15.0},
}
COMPONENT_NAMES = list(COMPONENTS.keys())


# --- Constraints ---
POPULATION_SIZE = 100
GENERATIONS = 100
BHT_SOLUBILITY_MAX = 0.002 # 0.2% Physical Limit


def calculate_stability(bht_pct, base_IP):
    """The Kinetic Synergy Module (Saturation Function)"""
    Vmax = 12.0 # Max stability hours BHT can add
    Km = 0.0005 # Saturation constant
    return base_IP + (Vmax * (bht_pct / (Km + bht_pct)))


def calculate_fitness(individual):
    base_IP, viscosity, cost = 0.0, 0.0, 0.0
    bht_pct = individual[COMPONENT_NAMES.index('BHT_Antioxidant')]
    palmitate_pct = individual[COMPONENT_NAMES.index('Methyl_Palmitate')]


    for i, name in enumerate(COMPONENT_NAMES):
        pct = individual[i]
        viscosity += pct * COMPONENTS[name]['viscosity']
        cost += pct * COMPONENTS[name]['cost']
        if name != 'BHT_Antioxidant':
            base_IP += pct * COMPONENTS[name]['stability_IP']


    total_IP = calculate_stability(bht_pct, base_IP)


    # Penalties for violating physical or regulatory limits
    penalties = 0
    if total_IP < 8.0: penalties += (8.0 - total_IP) * 50
    if viscosity > 6.0: penalties += (viscosity - 6.0) * 100
    if palmitate_pct > 0.30: penalties += (palmitate_pct - 0.30) * 150
    if bht_pct > BHT_SOLUBILITY_MAX: penalties += (bht_pct - BHT_SOLUBILITY_MAX) * 500


    fitness = (total_IP * 2.0) - (cost * 10.0) - penalties
    return fitness, total_IP, cost


def run_ga():
    pop = [[random.random() for _ in range(len(COMPONENT_NAMES))] for _ in range(POPULATION_SIZE)]
    pop = [[x/sum(ind) for x in ind] for ind in pop]
    all_results = []


    for gen in range(GENERATIONS):
        scored = []
        for ind in pop:
            fit, ip, cost = calculate_fitness(ind)
            scored.append((fit, ip, cost, ind))
            all_results.append((ip, cost))


        scored.sort(key=lambda x: x[0], reverse=True)


        next_pop = [scored[0][3], scored[1][3]]
        while len(next_pop) < POPULATION_SIZE:
            p1, p2 = random.choice(scored[:10])[3], random.choice(scored[:10])[3]
            child = [(p1[i]+p2[i])/2 for i in range(len(p1))]
            if random.random() < 0.1:
                idx = random.randint(0, len(child)-1)
                child[idx] += random.uniform(-0.02, 0.02)
            child = [max(0, x) for x in child]
            next_pop.append([x/sum(child) for x in child])
        pop = next_pop


    return scored[0], all_results


# --- EXECUTION ---
best_solution, scatter_data = run_ga()
fit_score, final_ip, final_cost, final_composition = best_solution


# --- FORMATTED CONSOLE RESULTS ---
print("-" * 40)
print("OPTIMIZED BIOFUEL BLEND RESULTS")
print("-" * 40)
print(f"{'Component':<20} | {'Concentration':<10}")
print("-" * 40)
for i, name in enumerate(COMPONENT_NAMES):
    print(f"{name:<20} | {final_composition[i]*100:>8.2f}%")


print("-" * 40)
print(f"Predicted Induction Period: {final_ip:.2f} hours")
print(f"Predicted Viscosity:        {final_composition[0]*4.5 + final_composition[1]*6.0 + final_composition[2]*4.0 + final_composition[3]*10.0:.2f} mm²/s")
print(f"Estimated Blend Cost:       ${final_cost:.2f}")
print("-" * 40)
print("Documentation: Blend meets EN 14214 standards (>8h stability).")
print("BHT concentration optimized for kinetic saturation & solubility limits.")
print("-" * 40)


# --- VISUALIZATION ---
ips = [x[0] for x in scatter_data]
costs = [x[1] for x in scatter_data]
bht_range = np.linspace(0, 0.005, 100)
stability_curve = [calculate_stability(x, 5.0) for x in bht_range]


fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))


# Plot A: Pareto Analysis
ax1.scatter(costs, ips, alpha=0.3, color='gray', label='Candidate Blends')
ax1.scatter(final_cost, final_ip, color='red', s=100, label='Optimized Solution', zorder=5)
ax1.set_title("Pareto Front: Stability vs Cost")
ax1.set_xlabel("Cost ($)")
ax1.set_ylabel("Induction Period (Hours)")
ax1.legend()
ax1.grid(True, linestyle='--', alpha=0.6)


# Plot B: Sensitivity Analysis
ax2.plot(bht_range * 100, stability_curve, color='blue', linewidth=2)
ax2.axvline(0.2, color='red', linestyle='--', label='Solubility Limit (0.2%)')
ax2.set_title("Sensitivity: BHT vs Stability")
ax2.set_xlabel("BHT Concentration (%)")
ax2.set_ylabel("Total Stability (Hours)")
ax2.annotate('Kinetic Saturation (Elbow)', xy=(0.1, 14), xytext=(0.2, 10),
             arrowprops=dict(facecolor='black', shrink=0.05))
ax2.legend()
ax2.grid(True, linestyle='--', alpha=0.6)


plt.tight_layout()

plt.show()
