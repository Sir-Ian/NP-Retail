# NP Real Estate Model

This project evaluates potential retail locations based on historic customer data using geospatial clustering and visualization. It is structured for easy reuse and extension to other datasets.

## Features
- Calculate coordinates from zip codes
- Cluster locations using weighted K-means
- Visualize clusters and proximity to existing retail locations

## Project Structure

- `np_re_model/` — Main Python package (clustering, geo utilities)
- `scripts/` — Command-line scripts for workflows
- `data/` — Example/sample data (not real customer data)
- `notebooks/` — Jupyter notebooks for demos (add your own for analysis)
- `tests/` — Unit tests

## Setup

1. Clone the repo
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Place your input data in the `data/` folder.

## Usage

### Calculating Coordinates
1. In your input data, rename the zip code column to `zip_code` exactly. Save as a CSV.
2. Update the input file path in the script to your saved CSV.
3. Ensure the `usa_ZipCodes_db` file path is correct. Check column headings if errors occur.
4. Set your desired output file path and name.
5. Run the script.

### Clustering and Graphing
1. Ensure your input data has `latitude` and `longitude` columns.
2. Set `radius_in_miles` to define the approximate cluster size.
3. Update the `retail_locations_df` file path to your store locations CSV (e.g., `NP_Stores_geo.csv`).
   - For new stores, update coordinates in the CSV or add names/zip codes and run through the coordinate script.
4. Set `threshold_distance` (in miles) to ignore points near current locations.
5. Set the output CSV file path in the script.
6. Run the script.

Example command:
```bash
python scripts/cluster_and_graph.py --input data/your_data.csv --output data/output.csv --radius 0.5 --threshold 30
```

See `notebooks/` for example analysis (add your own for custom exploration).

## Extending
- Add new clustering or visualization methods in `np_re_model/`.
- Write new scripts in `scripts/`.
- Add Jupyter notebooks in `notebooks/` for custom analysis.

## Contributing
- Fork the repo and create a feature branch.
- Add tests for new features in `tests/`.
- Submit a pull request with a clear description.

## Next Steps / Ideas
- Add support for more clustering algorithms (e.g., DBSCAN, HDBSCAN)
- Build a web dashboard for interactive exploration
- Add more data validation and cleaning utilities
- Improve documentation and add more usage examples
- Integrate with external geocoding APIs for more flexible coordinate lookup

## License
MIT License
