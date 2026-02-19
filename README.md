# BiOxiOptimize
This is a project revolving aroung using a multi-objective genetic algorithm to optimize anti-oxidant blends to serve as an appropriate surrgoate to improve oxidative stabilitiy in biofuels.

# BiOxiOptimize: Kinetic-Aware Biofuel Blend Optimizer

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Field: Chemical Engineering](https://img.shields.io/badge/Field-Chemical%20Engineering-orange)](https://en.wikipedia.org/wiki/Chemical_engineering)
[![Standard: EN_14214](https://www.en-standard.eu/bs-en-14214-2012-a2-2019-liquid-petroleum-products-fatty-acid-methyl-esters-fame-for-use-in-diesel-engines-and-heating-applications-requirements-and-test-methods/)

## Overview
**BiOxiOptimize** is a computational research framework designed to optimize biofuel blends while bypassing expensive and resource-intensive "wet-lab" experimentation. While traditional linear models fail to account for the physical realities of chemical additives, this engine utilizes **Michaelis-Menten kinetics** to simulate the saturation points of antioxidants.

By modeling the non-linear efficiency of Butylated Hydroxytoluene (BHT), the framework identifies the precise concentration where maximum oxidative stability is achieved before hitting the "Kinetic Ceiling".

---

## Kinetic Logic
The core innovation of BiOxiOptimize is the implementation of a Kinetic Synergy Module. Real-world radical scavenging shows diminishing returns; increasing antioxidant concentration does not lead to infinite stability.

### Saturation Equation
The model calculates the Induction Period (IP) gain using the following approach:

$$IP = IP_{base} + V_{max} \cdot \left( \frac{[BHT]}{K_m + [BHT]} \right)$$

* **$V_{max}$ (12.0h):** The theoretical maximum stability enhancement.
* **$K_m$ (0.0005):** The Michaelis constant, representing the concentration at which 50% of $V_{max}$ is reached.
* **Solubility Constraint:** The algorithm strictly enforces a **0.2% solubility limit** for BHT to ensure physical feasibility in commercial fuels.

---

## Features
* Multi-Objective Genetic Algorithm (GA): Efficiently navigates the FAME (Fatty Acid Methyl Ester) search space.
* Constraint-Aware Optimization: Enforces industry-standard limits on viscosity, cost, and cold-flow saturation (e.g., 30% Palmitate cap).
* Sensitivity Analysis: Automated mapping of the "Kinetic Elbow" to prevent chemical over-dosing.

---

## Results
The framework identified a primary blend that exceeds the 8-hour **EN 14214** standard for oxidative stability:

| Component | Concentration | Predicted Result |
| :--- | :--- | :--- |
| **Methyl Oleate** | 44.42% | **Stability: 16.73 Hours** |
| **Methyl Palmitate** | 30.00% | **Viscosity: 4.85 mm²/s** |
| **Methyl Linoleate** | 25.19% | **Cost: $1.37 / Unit** |
| **BHT Antioxidant** | **0.40%** | **Status: Compliant** |

Observation: Previous linear assumptions suggested BHT concentrations as high as 46%. BiOxiOptimize demonstrated that 0.4% BHT provides ~99% of total possible protection, eliminating 45.6% of redundant chemical volume (Author, 2026).

---

## Installation & Usage
### Prerequisites
* Python 3.8+
* NumPy
* Matplotlib

### Run the Optimizer
```bash
git clone [https://github.com/Laserslade/BiOxiOptimize.git](https://github.com/Laserslade/BiOxiOptimize.git)
cd BiOxiOptimize
python bioxi_optimizer.py
