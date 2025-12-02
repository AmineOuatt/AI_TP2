import random
from collections import deque
from utils.tsp_utils import total_distance

def tabu_search(cities, tabu_tenure=10):
    max_iterations=1000
    # Fixer la ville de départ (TSP avec retour à la même ville)
    start_city = cities[0]
    others = cities[1:]
    
    # Solution initiale aléatoire
    current = [start_city] + random.sample(others, len(others))
    current_dist = total_distance(current)
    
    # Meilleure solution globale
    best_solution = current[:]
    best_dist = current_dist

    # Liste Taboue : stocke les paires (i, j) récemment utilisées
    tabu_list = deque()

    for _ in range(max_iterations):
        best_neighbor = None
        best_neighbor_dist = float('inf')
        best_move = None

        # Explorer tous les voisins (swaps possibles)
        for i in range(1, len(cities)):
            for j in range(i + 1, len(cities)):
                neighbor = current[:]
                neighbor[i], neighbor[j] = neighbor[j], neighbor[i]
                d = total_distance(neighbor)

                move = (i, j)  # ou (min(i,j), max(i,j)) pour symétrie

                # Accepter si non tabou OU si meilleure que la meilleure globale (aspiration)
                if move not in tabu_list or d < best_dist:
                    if d < best_neighbor_dist:
                        best_neighbor = neighbor
                        best_neighbor_dist = d
                        best_move = move

        # Si aucun voisin n’est trouvable (improbable ici), sortir
        if best_neighbor is None:
            break

        # Mettre à jour la solution courante
        current = best_neighbor
        current_dist = best_neighbor_dist

        # Mettre à jour la meilleure solution globale si nécessaire
        if current_dist < best_dist:
            best_solution = current[:]
            best_dist = current_dist

        # Ajouter le mouvement à la liste taboue
        if best_move:
            tabu_list.append(best_move)
            if len(tabu_list) > tabu_tenure:
                tabu_list.popleft()

    return best_solution, best_dist