import random
import math
from utils.tsp_utils import total_distance

def simulated_annealing(cities, initial_temp=1000, min_temp=0.01, cooling=0.995, callback=None):

    start = cities[0]
    others = cities[1:]

    current = [start] + random.sample(others, len(others))
    current_dist = total_distance(current)

    best = current[:]
    best_dist = current_dist

    T = initial_temp

    while T > min_temp:
        # voisin = swap de 2 villes random (sauf Alger)
        a, b = random.sample(range(1, len(cities)), 2)
        neighbor = current[:]
        neighbor[a], neighbor[b] = neighbor[b], neighbor[a]

        neighbor_dist = total_distance(neighbor)
        delta = neighbor_dist - current_dist

        # meilleur = accepter
        if delta < 0 or random.random() < math.exp(-delta / T):
            current = neighbor
            current_dist = neighbor_dist

            if current_dist < best_dist:
                best = current[:]
                best_dist = current_dist
                if callback:
                    callback(best, best_dist)

        T *= cooling  # refroidissement

    return best, best_dist
