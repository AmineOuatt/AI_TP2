import random
from utils.tsp_utils import total_distance

def hill_climbing(cities, max_iterations=500):
    start_city = cities[0]
    others = cities[1:]

    current = [start_city] + random.sample(others, len(others))
    current_dist = total_distance(current)

    for _ in range(max_iterations):
        improved = False
        for i in range(1, len(cities)):
            for j in range(i + 1, len(cities)):
                neighbor = current[:]
                neighbor[i], neighbor[j] = neighbor[j], neighbor[i]
                d = total_distance(neighbor)
                if d < current_dist:
                    current, current_dist = neighbor, d
                    improved = True
        if not improved:
            break

    return current, current_dist
