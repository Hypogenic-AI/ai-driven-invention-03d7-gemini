# Downloaded Datasets

This directory contains datasets for the materials discovery research project.

## Dataset 1: GNoME Stable Materials Summary
- **Source**: Google DeepMind GNoME Project (https://storage.googleapis.com/gdm_materials_discovery/gnome_data/stable_materials_summary.csv)
- **Size**: 144 MB (381,000+ entries)
- **Format**: CSV
- **Content**: Compositions, energies, space groups, and stability metrics for discovered inorganic crystals.

## Dataset 2: GNoME r2SCAN Validation
- **Source**: Google DeepMind GNoME Project (https://storage.googleapis.com/gdm_materials_discovery/gnome_data/stable_materials_r2scan.csv)
- **Size**: 21 MB
- **Format**: CSV
- **Content**: Validation calculations using the r2SCAN functional.

## Note on Large Data
Detailed crystal structures (CIF files) are available in compressed ZIPs from the GNoME bucket but are NOT downloaded here due to size (>10GB). They can be fetched on-demand using the provided scripts in `code/GNoME/scripts/`.
