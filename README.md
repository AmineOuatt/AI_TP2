# Metaheuristic TSP Visualizer

Interactive Tkinter application that demonstrates three metaheuristics (random search, local search, and hill climbing) on an Algerian Traveling Salesman Problem instance. Cities are loaded from a CSV file, and the best tour is plotted step by step or in full using Matplotlib.

## Project Structure
- `main.py`: GUI entry point; wires up the algorithms and plotting.
- `algorithms/`: contains `random_search.py`, `local_search.py`, and `hill_climbing.py`.
- `utils/tsp_utils.py`: helpers to load the CSV, compute distances, and tour length.
- `data/algeria_20_cities_xy.csv`: expected dataset (city name, `x_km`, `y_km`). Add this file if it is missing.

## Requirements
- Python 3.10+
- `pandas`, `matplotlib`

Tkinter ships with standard Python on Windows/macOS; on Linux you may need the `python3-tk` package.

Install dependencies:
```bash
pip install -r requirements.txt
# or, if there is no requirements file yet:
pip install pandas matplotlib
```

## Running the App
```bash
python main.py
```

What you get:
- Choose one of the three algorithms from the left panel.
- Use `▶ Étape par étape` to reveal each leg of the path and accumulate distance.
- Use `🏁 Montrer le résultat final` to draw the entire best tour immediately.

## Customizing Cities
Update or replace `data/algeria_20_cities_xy.csv` with your own coordinates (columns: `city,x_km,y_km`). Ensure the first row corresponds to the starting city (Alger in the default dataset).

## Troubleshooting
- **Missing CSV**: create the `data` directory and add the expected file.
- **Tkinter import errors on Linux**: install `sudo apt install python3-tk`.
- **Plot not showing**: make sure a GUI backend is available (e.g., run locally, not on a headless server).

