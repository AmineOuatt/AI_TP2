import random
from utils.tsp_utils import total_distance

def random_search(cities, iterations=1000):
    # La première ville du fichier = Alger
    start_city = cities[0]
    others = cities[1:]

    # Premier chemin aléatoire
    best = [start_city] + random.sample(others, len(others))
    best_dist = total_distance(best)

    # Recherche aléatoire
    for _ in range(iterations):
        candidate = [start_city] + random.sample(others, len(others))
        dist = total_distance(candidate)
        if dist < best_dist:
            best, best_dist = candidate, dist

    return best, best_dist
