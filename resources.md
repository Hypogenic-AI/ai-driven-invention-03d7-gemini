# Resources Catalog: AI-Driven Invention (Atomic Modelling)

## Summary
This catalog summarizes the papers, datasets, and code gathered to investigate AI-driven materials discovery and atomic modelling.

## Papers
Total papers downloaded: 3

| Title | Authors | Year | File | Key Info |
|-------|---------|------|------|----------|
| Scaling deep learning for materials discovery | Merchant et al. | 2023 | papers/2023_Merchant_GNoME.pdf | Discovered 381,000 stable crystals |
| Automating alloy design... | Buehler et al. | 2025 | papers/2025_Buehler_AtomAgents.pdf | Multi-agent AI for HEAs |
| Active Learning for Conditional Inverse Design | Li et al. | 2025 | papers/2025_Li_Active_Learning_FAM.pdf | Inverse design with FAMs |

## Datasets
Total datasets downloaded: 2 main summaries

| Name | Source | Size | Task | Location | Notes |
|------|--------|------|------|----------|-------|
| GNoME Summary | Google DeepMind | 144 MB | Stability Prediction | datasets/gnome/stable_materials_summary.csv | 381K stable materials |
| GNoME r2SCAN | Google DeepMind | 21 MB | Validation | datasets/gnome/stable_materials_r2scan.csv | High-fidelity benchmarks |

## Code Repositories
Total repositories cloned: 2

| Name | URL | Purpose | Location | Notes |
|------|-----|---------|----------|-------|
| GNoME | github.com/google-deepmind/materials_discovery | Stability Prediction | code/GNoME/ | Official DeepMind repo |
| AtomAgents | github.com/lamm-mit/AtomAgents | Multi-agent discovery | code/AtomAgents/ | LLM + LAMMPS framework |

## Resource Gathering Notes

### Search Strategy
- Used `paper-finder` for initial screening.
- Targeted search on arXiv for specific landmark papers mentioned in reviews (GNoME, AtomAgents).
- Searched for official GitHub repositories associated with the papers.
- Downloaded public datasets from Google Cloud Storage (GNoME bucket).

### Challenges Encountered
- GNoME paper is in Nature; utilized the arXiv preprint for deep reading.
- Crystal structure ZIP files are too large for direct inclusion (>10GB); documented the fetching scripts instead.

## Recommendations for Experiment Design

1. **Primary Dataset**: Use `datasets/gnome/stable_materials_summary.csv` to identify chemical systems of interest (e.g., Ternary or Quaternary systems).
2. **Baseline Methods**: Use the pre-trained GNoME models (if scripts available) or simple GNNs on the provided summary data.
3. **Simulation Tool**: Use `code/AtomAgents/` as a template for integrating LLM agents with physical simulation (LAMMPS).
4. **Task**: Conduct an "autonomous invention" experiment where an agent designs a new alloy with specific target properties (e.g., low density and high stability) by exploring combinations in the GNoME space and verifying them with AtomAgents' simulation pipeline.
