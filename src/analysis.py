import json
import numpy as np
import matplotlib.pyplot as plt
from scipy import stats
import os

print("Loading results...")
with open("../results/all_experiments.json", "r") as f:
    data = json.load(f)

random_res = data['random']
zero_shot_res = data['zero_shot']
al_res = data['active_learning']

# Extract formation energies of found materials
random_energies = [r['formation_energy'] for r in random_res if r['found']]
zero_shot_energies = [r['formation_energy'] for r in zero_shot_res if r['found']]

print("\n--- Descriptive Statistics ---")
print(f"Random Search - Hits: {len(random_energies)}/{len(random_res)}, Mean Energy: {np.mean(random_energies):.4f}, Std: {np.std(random_energies):.4f}")
print(f"Zero-Shot Search - Hits: {len(zero_shot_energies)}/{len(zero_shot_res)}, Mean Energy: {np.mean(zero_shot_energies):.4f}, Std: {np.std(zero_shot_energies):.4f}")

print("\n--- Hypothesis Testing ---")
# t-test for independent samples (assuming unequal variance)
t_stat, p_val = stats.ttest_ind(zero_shot_energies, random_energies, equal_var=False)
print(f"T-statistic: {t_stat:.4f}")
print(f"P-value: {p_val:.4e}")

if p_val < 0.05:
    print("Conclusion: The difference in formation energy between LLM Zero-Shot and Random Search is statistically significant (p < 0.05).")
else:
    print("Conclusion: The difference is NOT statistically significant (p >= 0.05).")

# Calculate Effect Size (Cohen's d)
nx = len(zero_shot_energies)
ny = len(random_energies)
dof = nx + ny - 2
pool_sd = np.sqrt(((nx-1)*np.var(zero_shot_energies, ddof=1) + (ny-1)*np.var(random_energies, ddof=1)) / dof)
cohens_d = (np.mean(zero_shot_energies) - np.mean(random_energies)) / pool_sd
print(f"Effect Size (Cohen's d): {cohens_d:.4f}")

print("\n--- Active Learning Analysis ---")
al_energies = [r['formation_energy'] for r in al_res if r['found']]
print(f"Active Learning - Hits: {len(al_energies)}/{len(al_res)}, Mean Energy: {np.mean(al_energies):.4f}")

# Plotting
os.makedirs("../figures", exist_ok=True)

# 1. Boxplot of Formation Energies
plt.figure(figsize=(8, 6))
plt.boxplot([random_energies, zero_shot_energies, al_energies], labels=['Random', 'LLM Zero-Shot', 'LLM Active Learning'])
plt.ylabel('Formation Energy (eV/atom)')
plt.title('Formation Energy of Discovered Stable Materials')
plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.savefig("../figures/energy_comparison.png")
plt.close()

# 2. Hit Rate Bar Chart
hit_rates = [len(random_energies)/len(random_res), 
             len(zero_shot_energies)/len(zero_shot_res), 
             len(al_energies)/len(al_res)]
plt.figure(figsize=(8, 6))
bars = plt.bar(['Random', 'LLM Zero-Shot', 'LLM Active Learning'], hit_rates, color=['gray', 'blue', 'orange'])
plt.ylabel('Hit Rate (Fraction of Valid Systems Proposed)')
plt.title('Success Rate in Proposing Stable Ternary Systems')
plt.ylim(0, 1)
for bar in bars:
    yval = bar.get_height()
    plt.text(bar.get_x() + bar.get_width()/2, yval + 0.02, round(yval, 2), ha='center', va='bottom')
plt.savefig("../figures/hit_rates.png")
plt.close()

# 3. Active Learning Trajectory
steps = [r['step'] for r in al_res if r['found']]
energies = [r['formation_energy'] for r in al_res if r['found']]
plt.figure(figsize=(8, 6))
plt.plot(steps, energies, marker='o', linestyle='-', color='orange')
plt.xlabel('Step')
plt.ylabel('Formation Energy (eV/atom)')
plt.title('Active Learning Trajectory (Found Materials)')
plt.grid(True)
plt.savefig("../figures/al_trajectory.png")
plt.close()

print("\nAnalysis complete. Figures saved to ../figures/")
