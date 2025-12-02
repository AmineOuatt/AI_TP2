import random
import math
from utils.tsp_utils import total_distance

def simulated_annealing(cities, max_iterations, callback=None):
    """
    Recuit Simulé selon le polycopié Prof. Larabi
    """
    # Départ obligatoire depuis Alger
    start_city = cities[0]
    other_cities = cities[1:]
    
    # Schéma de température : [2^0, 2^-1, 2^-2, ..., 2^-99]
    temperature_schedule = [2 ** (-t) for t in range(max_iterations)]
    
    # n = chemin initial (solution aléatoire)
    current_path = [start_city] + random.sample(other_cities, len(other_cities))
    current_cost = total_distance(current_path)
    
    # Meilleure solution connue
    best_path = current_path[:]
    best_cost = current_cost
    
    epsilon = 0.001  # Seuil de convergence
    
    # --- Boucle principale : Pour t = 1..taille(schema) ---
    for t in range(len(temperature_schedule)):
        T = temperature_schedule[t]  # T = schema[t]
        
        # n' = successeur de n choisi au hasard (swap de 2 villes)
        i, j = random.sample(range(1, len(cities)), 2)
        neighbor_path = current_path[:]
        neighbor_path[i], neighbor_path[j] = neighbor_path[j], neighbor_path[i]
        
        neighbor_cost = total_distance(neighbor_path)
        
        # dE = F(n') - F(n) si on maximise
        # Mais ici on MINIMISE, donc dE = F(n) - F(n')
        dE = current_cost - neighbor_cost
        
        # --- Décision d'acceptation  ---
        if dE > 0:
            # Si dE > 0, alors amélioration → assigner n = n'
            current_path = neighbor_path
            current_cost = neighbor_cost
        else:
            # Sinon assigner n = n' seulement avec probabilité e^(-|dE|/T) ≥ r
            r = random.random()  # r = random(0, 1)
            acceptance_prob = math.exp(-abs(dE) / T) if T > 0 else 0
            
            if acceptance_prob >= r:
                current_path = neighbor_path
                current_cost = neighbor_cost
        
        # Mise à jour du meilleur trouvé
        if current_cost < best_cost:
            best_path = current_path[:]
            best_cost = current_cost
            
            if callback:
                callback(best_path, best_cost)
        
        # --- Condition d'arrêt
        # "Si |n - n'| < ε et T petit alors stop"
        # On interprète |n - n'| comme la différence de coût
        if abs(dE) < epsilon and T < 0.01:
            print(f"⏹️ Convergence atteinte à l'itération {t}")
            break
    
    return best_path, best_cost