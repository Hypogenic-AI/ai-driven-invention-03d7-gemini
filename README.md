# AI-Driven Invention (Atomic Modelling)

This repository contains the code, data, and experimental reports for testing whether an LLM-based autonomous agent can systemically invent new stable materials by proposing elemental combinations and validating them against the GNoME dataset.

## Key Findings
- **Intelligent Search Beats Random:** The `gpt-4o` LLM achieved a 50% hit rate in predicting stable ternary materials compared to 40% for random search, and the discovered materials had significantly lower formation energies (-1.30 eV/atom vs -0.82 eV/atom).
- **Active Learning Drives Deep Stability:** When given iterative feedback on the stability of its proposals, the LLM adapted its strategy to find exceptionally stable perovskite-like oxide systems (e.g., Ba-Ti-O), achieving an average formation energy of -2.33 eV/atom.
- **Medium Effect Size:** The difference between LLM-guided proposals and random guessing demonstrated a Cohen's d of 0.58.

## File Structure
- `planning.md` - Initial research plan and experimental design.
- `REPORT.md` - Comprehensive final research report including methodology, statistics, and analysis.
- `src/` - Python source code.
  - `experiment.py` - Connects to the LLM (OpenRouter) and tests proposals against GNoME data.
  - `analysis.py` - Computes descriptive/inferential statistics and generates plots.
- `results/` - Output JSON files containing experimental data.
- `figures/` - Generated plots (e.g., hit rates, learning trajectories).

## How to Reproduce
1. Set up the virtual environment:
   ```bash
   uv venv
   source .venv/bin/activate
   uv pip install -r requirements.txt
   ```
2. Set your OpenRouter API key:
   ```bash
   export OPENROUTER_KEY="your_key_here"
   ```
3. Run the experiments:
   ```bash
   cd src
   python experiment.py
   ```
4. Run the analysis:
   ```bash
   python analysis.py
   ```

For full details, please refer to [REPORT.md](./REPORT.md).