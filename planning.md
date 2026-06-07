## Research Title
Beyond Trial and Error: AI-Driven Invention (Atomic Modelling)

## Motivation & Novelty Assessment

### Why This Research Matters
Human progress relies on inventing new combinations of existing elements, from medicines to advanced materials. Typically, this process relies on human intuition and trial-and-error, which is slow and limited by human cognitive bandwidth. An autonomous, intelligent system capable of systematically structuring experiments across the space of possible material combinations could vastly accelerate breakthrough discoveries in domains like materials science and engineering.

### Gap in Existing Work
Existing work (like DeepMind's GNoME) utilizes Graph Neural Networks for large-scale stability prediction of generated crystal structures, and work like AtomAgents uses multi-agent frameworks for complex physics simulations. However, what is lacking is an overarching "inventor" framework that uses the reasoning capabilities of LLMs to intelligently traverse the design space, formulate hypotheses about combinations, and validate them against known stable domains automatically, closing the loop of autonomous invention.

### Our Novel Contribution
We propose a generalized "AI-Driven Inventor" system that integrates real-time LLM reasoning to propose novel elemental combinations (alloys/materials) optimized for specific properties, leveraging the GNoME stable materials database as a validation ground for stability (Formation Energy / Energy Above Hull).

### Experiment Justification
- **Experiment 1 (LLM Combination Proposal vs. Random Search):** We will test whether an LLM (using domain knowledge) can propose elemental combinations that are statistically more stable (lower formation energy in the GNoME dataset) than random sampling.
- **Experiment 2 (Iterative Refinement - Active Learning):** We will test if the LLM can iteratively refine its proposals when given feedback on the stability of its previous guesses, mimicking the scientific method.

---

## Research Question
Can an LLM-based autonomous agent systematically propose and refine elemental combinations that are more likely to result in stable materials compared to random exploration, using the GNoME stability dataset as the ground truth?

## Background and Motivation
The search space for stable materials is vast. Traditional computational methods (like DFT) are expensive. While models like GNoME have mapped out hundreds of thousands of stable structures, navigating this space strategically requires intelligent hypothesis generation. By using LLMs as the "hypothesis generator" and GNoME data as "experimental validation", we simulate a fully autonomous invention loop.

## Hypothesis Decomposition
1. **Hypothesis 1:** LLMs possess intrinsic chemical knowledge that allows them to propose elemental combinations with significantly lower formation energies than random element combinations.
2. **Hypothesis 2:** Providing LLMs with performance feedback (active learning loop) will result in proposed combinations converging towards the convex hull of stability (lower Energy Above Hull).

## Proposed Methodology

### Approach
We will build a simple autonomous loop where an LLM agent is tasked with inventing stable ternary or quaternary materials. The system will parse the agent's proposed chemical formula, check if it exists in the GNoME `stable_materials_summary.csv` dataset, and retrieve its stability metrics.

### Experimental Steps
1. **Data Ingestion:** Load and preprocess the `stable_materials_summary.csv` dataset. Create an index of formulas to their `formation_energy_per_atom` and `energy_above_hull`.
2. **Random Baseline Search:** Generate $N$ random combinations of 3-4 elements that exist in the dataset and compute their average stability metrics.
3. **LLM Zero-Shot Search:** Prompt an LLM to propose $N$ novel stable 3-4 element combinations. Check their stability in the dataset.
4. **LLM Iterative Search (Active Learning):** Prompt the LLM to propose 1 combination. Provide its stability as feedback. Ask the LLM to adjust and propose the next. Repeat for $M$ steps.
5. **Evaluation:** Compare the success rate (finding stable materials) and average formation energy across methods.

### Baselines
- **Random Search:** Randomly picking 3-4 elements from the periodic table and checking the GNoME database. This represents the "dumb trial and error" approach.

### Evaluation Metrics
- **Hit Rate:** Percentage of proposed combinations that exist in the GNoME stable dataset.
- **Average Formation Energy:** Mean formation energy of the proposed combinations (lower is better).
- **Energy Above Hull:** Mean energy above hull for proposed structures (where 0 indicates a stable structure).

### Statistical Analysis Plan
- We will conduct a t-test to compare the mean formation energies of LLM proposals vs. random search.
- We will plot learning curves for the iterative search to see if stability improves over iterations.

## Expected Outcomes
We expect the LLM to significantly outperform random search due to its pre-trained knowledge of chemistry and material science. We also expect the active learning loop to show a downward trend in Energy Above Hull over iterations.

## Timeline and Milestones
1. Environment and dataset setup (20 mins).
2. Implementing the search baselines and LLM interface (45 mins).
3. Running experiments and parsing results (45 mins).
4. Analysis and documentation (30 mins).

## Potential Challenges
- The LLM might propose formulas that don't match the exact stoichiometry in the GNoME dataset.
  - *Mitigation:* We will simplify the check to matching the *elemental system* (e.g., if LLM proposes Li2O, we check for the Li-O system in GNoME and pick the most stable variant).
- Cost/Rate limits on LLM calls.
  - *Mitigation:* Use OpenRouter with provided environment variables and limit $N$ to 30-50 for proof-of-concept.

## Success Criteria
- Successful execution of the automated loop.
- Statistically significant difference between LLM-guided search and random search.
- A comprehensive REPORT.md documenting the findings.