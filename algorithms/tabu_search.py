import random
from utils.tsp_utils import total_distance

def tabu_search(cities, iterations=300, tabu_size=30, callback=None):
    start = cities[0]
    others = cities[1:]

    current = [start] + random.sample(others, len(others))
    current_dist = total_distance(current)

    best = current[:]
    best_dist = current_dist

    tabu_list = []

    for _ in range(iterations):
        best_neighbor = None
        best_neighbor_dist = float("inf")
        best_move = None

        for i in range(1, len(cities)):
            for j in range(i + 1, len(cities)):
                if (i, j) in tabu_list:
                    continue

                neighbor = current[:]
                neighbor[i], neighbor[j] = neighbor[j], neighbor[i]
                dist = total_distance(neighbor)

                if dist < best_neighbor_dist:
                    best_neighbor = neighbor
                    best_neighbor_dist = dist
                    best_move = (i, j)

        # Move to best neighbor
        current = best_neighbor
        current_dist = best_neighbor_dist

        # Update best global
        if current_dist < best_dist:
            best = current[:]
            best_dist = current_dist
            if callback:
                callback(best, best_dist)

        # Update tabu list
        tabu_list.append(best_move)
        if len(tabu_list) > tabu_size:
            tabu_list.pop(0)

    return best, best_dist
