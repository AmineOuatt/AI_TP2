import random
from utils.tsp_utils import total_distance

def local_search(cities, iterations=1000):
    start_city = cities[0]
    others = cities[1:]

    current = [start_city] + random.sample(others, len(others))
    best = current
    best_dist = total_distance(best)

    for _ in range(iterations):
        i, j = random.sample(range(1, len(cities)), 2)  # Ne pas toucher Alger
        neighbor = current[:]
        neighbor[i], neighbor[j] = neighbor[j], neighbor[i]
        d = total_distance(neighbor)
        if d < best_dist:
            best, best_dist = neighbor, d
            current = neighbor

    return best, best_dist
