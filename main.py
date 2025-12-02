import sys, os
import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from algorithms.simulated_annealing import simulated_annealing

# --- Fix imports ---
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(BASE_DIR, "algorithms"))
sys.path.insert(0, os.path.join(BASE_DIR, "utils"))

from algorithms.random_search import random_search
from algorithms.local_search import local_search
from algorithms.hill_climbing import hill_climbing
from utils.tsp_utils import load_cities, distance

# ------------------------------------------------------
class TSPApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Projet 2 - Métaheuristiques")
        self.root.geometry("1250x780")
        self.root.resizable(True, True)

        # Load cities
        try:
            self.cities = load_cities("data/algeria_20_cities_xy.csv")
        except Exception as e:
            print(f"Erreur : {e}")
            self.cities = []

        # Layout frames
        self.left_frame = tk.Frame(root, width=320, bg="#f0f0f0")
        self.left_frame.pack(side="left", fill="y")

        self.right_frame = tk.Frame(root, bg="white")
        self.right_frame.pack(side="right", expand=True, fill="both")

        # Buttons
        tk.Label(self.left_frame, text="⚙️ Choisissez un algorithme :", font=("Arial", 13, "bold"), bg="#f0f0f0").pack(pady=15)
        ttk.Button(self.left_frame, text="Recherche Aléatoire", command=lambda: self.run_algo("Random"), width=28).pack(pady=6)
        ttk.Button(self.left_frame, text="Recherche Locale", command=lambda: self.run_algo("Local"), width=28).pack(pady=6)
        ttk.Button(self.left_frame, text="Hill Climbing", command=lambda: self.run_algo("Hill"), width=28).pack(pady=6)
        ttk.Button(self.left_frame, text=" Simulated Annealing",command=lambda: self.run_algo("SA"), width=25).pack(pady=6)
        ttk.Button(self.left_frame, text=" Tabu Search",command=lambda: self.run_algo("Tabu"), width=25).pack(pady=6)
        ttk.Button(self.left_frame, text=" Genetic Algorithm",command=lambda: self.run_algo("GA"), width=25).pack(pady=6)

        ttk.Separator(self.left_frame, orient="horizontal").pack(fill="x", pady=15)

        self.step_btn = ttk.Button(self.left_frame, text="▶ Étape par étape", command=self.show_next_step, state="disabled", width=28)
        self.step_btn.pack(pady=6)

        self.final_btn = ttk.Button(self.left_frame, text="🏁 Montrer le résultat final", command=self.show_full_path, state="disabled", width=28)
        self.final_btn.pack(pady=6)

        ttk.Separator(self.left_frame, orient="horizontal").pack(fill="x", pady=15)

        self.info_label = tk.Label(self.left_frame, text="Distance totale : 0.00 km", bg="#f0f0f0", font=("Arial", 12, "bold"), fg="#333")
        self.info_label.pack(pady=10)

        self.step_label = tk.Label(self.left_frame, text="", bg="#f0f0f0", font=("Arial", 10))
        self.step_label.pack(pady=5)

        # Matplotlib figure
        self.fig, self.ax = plt.subplots(figsize=(9.5, 7.5))
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.right_frame)
        self.canvas.get_tk_widget().pack(fill="both", expand=True)

        # Variables
        self.path = []
        self.current_index = 0
        self.partial_distance = 0.0

    # ------------------------------------------------------
    def run_algo(self, algo):
        """Run selected algorithm"""
        if not self.cities:
            return

        if algo == "Random":
            self.path, self.best_dist = random_search(self.cities, iterations=500)
        elif algo == "Local":
            self.path, self.best_dist = local_search(self.cities, iterations=500)
        elif algo == "Hill":
            self.path, self.best_dist = hill_climbing(self.cities, max_iterations=500)
        elif algo == "SA":
            self.path, self.best_dist = simulated_annealing(self.cities, max_iterations=10000,callback= None)
        elif algo == "Tabu":
            from algorithms.tabu_search import tabu_search
            self.path, self.best_dist = tabu_search(cities, tabu_tenure=10)
        elif algo == "GA":
            from algorithms.genetic_algorithm import genetic_algorithm
            self.path, self.best_dist = genetic_algorithm(self.cities, population_size=50, generations=200, mutation_rate=0.1)

        # Ensure the path ends back at Alger (for display)
        self.path.append(self.path[0])

        self.info_label.config(text=f"Distance totale : 0.00 km")
        self.step_btn.config(state="normal")
        self.final_btn.config(state="normal")
        self.current_index = 1
        self.partial_distance = 0.0
        self.clear_plot()
        self.show_next_step()  # instead of self.plot_step(0,1)


    # ------------------------------------------------------
    def clear_plot(self):
        self.ax.clear()
        x = [c[1] for c in self.cities]
        y = [c[2] for c in self.cities]
        self.ax.scatter(x, y, color="blue")

        # 🔴 Mark Alger in red
        for c in self.cities:
            color = "red" if "alger" in c[0].lower() or "algiers" in c[0].lower() else "blue"
            self.ax.text(c[1], c[2], c[0], fontsize=9, color=color)

        self.ax.set_title("Carte des villes d'Algérie", fontsize=13)
        self.ax.set_xlabel("x (km)")
        self.ax.set_ylabel("y (km)")
        self.canvas.draw()

    # ------------------------------------------------------
    def show_next_step(self):
        """Show one city connection per click + increment distance"""
        if self.current_index < len(self.path):
            i = self.current_index - 1
            a, b = self.path[i], self.path[i + 1]
            d = distance(a, b)

            # Draw line segment
            self.ax.plot([a[1], b[1]], [a[2], b[2]], color="red", linewidth=2)
            self.canvas.draw()

            # Update partial distance
            self.partial_distance += d
            self.info_label.config(text=f"Distance totale : {self.partial_distance:.2f} km")

            self.step_label.config(text=f"→ {a[0]} → {b[0]} : {d:.2f} km")
            self.current_index += 1
        else:
            self.step_label.config(text="Trajet complet affiché.")
            self.step_btn.config(state="disabled")

    # ------------------------------------------------------
    def show_full_path(self):
        """Show the complete path and total distance directly"""
        self.clear_plot()
        x = [c[1] for c in self.path]
        y = [c[2] for c in self.path]
        self.ax.plot(x, y, marker='o', linestyle='-', color="red", linewidth=2)
        self.ax.set_title("Résultat final", fontsize=13)
        self.canvas.draw()
        self.step_label.config(text="Trajet complet affiché.")
        self.info_label.config(text=f"Distance totale : {self.best_dist:.2f} km")

# ------------------------------------------------------
if __name__ == "__main__":
    root = tk.Tk()
    app = TSPApp(root)
    root.mainloop()
