# Literature Review: AI-Driven Invention (Atomic Modelling)

## Research Area Overview
The field of materials science is undergoing a paradigm shift from traditional trial-and-error experimentation to AI-driven autonomous discovery. This transition is enabled by large-scale datasets, powerful Graph Neural Networks (GNNs) for atomic modelling, and multi-agent LLM systems that can plan and execute complex experimental workflows.

## Key Papers

### Paper 1: Scaling deep learning for materials discovery (GNoME)
- **Authors**: Amil Merchant, Simon Batzner, et al.
- **Year**: 2023
- **Source**: Nature / arXiv:2310.14029
- **Key Contribution**: Introduced Graph Networks for Materials Exploration (GNoME), discovering 2.2 million new crystal structures.
- **Methodology**: Large-scale training of GNNs on Materials Project data, followed by active learning loops where candidate structures are validated via Density Functional Theory (DFT).
- **Datasets Used**: Materials Project (2018 snapshot), OQMD, WBM.
- **Results**: Increased the number of known stable materials by an order of magnitude, identifying 381,000 stable crystals.
- **Relevance**: Provides the foundation for large-scale structural discovery and stable crystal identification.

### Paper 2: Automating alloy design and discovery with physics-aware multimodal multiagent AI (AtomAgents)
- **Authors**: Alireza Ghafarollahi, Markus J. Buehler
- **Year**: 2025
- **Source**: PNAS / arXiv:2410.13768
- **Key Contribution**: Developed "AtomAgents," a multi-agent LLM-based framework for autonomous alloy design.
- **Methodology**: Integration of LLMs with atomistic simulation tools (LAMMPS). Specialized agents (Physicist, Chemist, Engineer) collaborate to design HEAs (High Entropy Alloys) and analyze their properties.
- **Datasets Used**: Uses interatomic potential repositories (EAM, MEAM, MTP).
- **Results**: Successfully designed novel HEAs and predicted their mechanical properties, demonstrating the power of multi-agent collaboration in scientific discovery.
- **Relevance**: Shows how to bridge high-level reasoning (LLMs) with low-level physical simulations.

### Paper 3: Active Learning for Conditional Inverse Design with Crystal Generation and Foundation Atomic Models
- **Authors**: Zhuoyuan Li, et al.
- **Year**: 2025
- **Source**: arXiv:2502.16984
- **Key Contribution**: Combined generative models with Foundation Atomic Models (FAMs) for inverse design of crystals.
- **Methodology**: Active learning framework using crystal generation models (like CDVAE) and FAMs (like MACE) to iteratively improve discovery of materials with target properties.
- **Relevance**: Highlights the current state-of-the-art in "targeted" discovery rather than broad structural search.

## Common Methodologies
- **Graph Neural Networks (GNNs)**: Used for representing crystal structures and predicting properties (energies, stability).
- **Active Learning**: Iterative loops of structure generation -> property prediction -> high-fidelity validation (DFT/LAMMPS) -> retraining.
- **Multi-Agent Systems**: Using LLMs to orchestrate complex simulation pipelines and expert-level reasoning.
- **Inverse Design**: Starting with target properties and generating structures that might satisfy them.

## Standard Baselines
- **Materials Project (MP)**: The gold standard for crystal structures and properties.
- **OQMD (Open Quantum Materials Database)**: Another large database for inorganic materials.
- **NequIP / MACE**: State-of-the-art equivariant GNNs for interatomic potentials.

## Evaluation Metrics
- **Energy Above Hull (Ehull)**: Distance to the convex hull of stability (lower is more stable).
- **Formation Energy**: Energy required to form the material from elements.
- **Accuracy of Property Prediction**: MAE/RMSE of predicted energies compared to DFT.

## Recommendations for Our Experiment
1. **Focus on Multi-Agent Orchestration**: Build upon the AtomAgents concept to automate the exploration of the GNoME dataset.
2. **Target Specific Properties**: Instead of broad search, use active learning to find materials with specific mechanical or electronic properties (e.g., high-toughness alloys or Li-ion conductors).
3. **Hybrid Validation**: Use fast GNNs (GNoME-like) for initial screening and LAMMPS (AtomAgents-like) for deeper property verification.
