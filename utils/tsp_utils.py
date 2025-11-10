import pandas as pd
import math
import matplotlib.pyplot as plt

def load_cities(filepath="data/algeria_20_cities_xy.csv"):
    df = pd.read_csv(filepath)
    cities = df[['city', 'x_km', 'y_km']].values.tolist()
    print("✅ Villes chargées depuis le CSV :")
    for c in cities:
        print(f" - {c[0]} (x={c[1]}, y={c[2]})")
    return cities

def distance(a, b):
    return math.sqrt((a[1] - b[1])**2 + (a[2] - b[2])**2)

def total_distance(path): 
    dist = 0
    for i in range(len(path) - 1):
        dist += distance(path[i], path[i + 1])
    dist += distance(path[-1], path[0])
    return dist
load_cities()