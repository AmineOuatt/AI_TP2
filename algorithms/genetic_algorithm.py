import random
from utils.tsp_utils import total_distance

def crossover(parent1, parent2):
    """Partie centrale du parent1 + complétée par parent2"""
    start = 1
    end = random.randint(2, len(parent1) - 1)

    middle = parent1[start:end]
    remaining = [city for city in parent2 if city not in middle]

    return [parent1[0]] + middle + remaining


def mutate(route, prob=0.1):
    if random.random() < prob:
        a, b = random.sample(range(1, len(route)), 2)
        route[a], route[b] = route[b], route[a]


def genetic_algorithm(cities, population_size=30, generations=200, mutation_rate=0.1, callback=None):
    start = cities[0]
    others = cities[1:]

    # Population initiale
    population = [
        [start] + random.sample(others, len(others))
        for _ in range(population_size)
    ]

    for _ in range(generations):
        # Trier par distance
        population.sort(key=total_distance)

        best = population[0]
        best_dist = total_distance(best)

        if callback:
            callback(best, best_dist)

        # Sélection : garder top 50%
        survivors = population[:population_size // 2]

        next_gen = survivors[:]

        # Croisement
        while len(next_gen) < population_size:
            p1, p2 = random.sample(survivors, 2)
            child = crossover(p1, p2)
            mutate(child, mutation_rate)
            next_gen.append(child)

        population = next_gen

    # Retourner meilleure solution finale
    population.sort(key=total_distance)
    return population[0], total_distance(population[0])
