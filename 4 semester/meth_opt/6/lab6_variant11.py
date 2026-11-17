import random
import math

# ---------- Task 1: genetic algorithm for TSP ----------
DIST_TSP = [
    [0, 1, 11, 10, 5],
    [1, 0, 11, 6, 10],
    [11, 11, 0, 6, 1],
    [10, 6, 6, 0, 1],
    [5, 10, 1, 1, 0],
]


def route_length(genome):
    # City 1 is fixed as the start and finish.
    route = [0] + genome + [0]
    return sum(DIST_TSP[route[i]][route[i + 1]] for i in range(len(route) - 1))


def fitness(genome):
    return 1 / route_length(genome)


def order_crossover(parent1, parent2):
    n = len(parent1)
    left, right = sorted(random.sample(range(n), 2))
    child = [None] * n
    child[left:right + 1] = parent1[left:right + 1]

    pos = (right + 1) % n
    for gene in parent2:
        if gene not in child:
            child[pos] = gene
            pos = (pos + 1) % n
    return child


def mutate(genome, mutation_rate):
    if random.random() < mutation_rate:
        i, j = random.sample(range(len(genome)), 2)
        genome[i], genome[j] = genome[j], genome[i]


def select_parent(population):
    total = sum(fitness(g) for g in population)
    point = random.random() * total
    current = 0
    for genome in population:
        current += fitness(genome)
        if current >= point:
            return genome[:]
    return population[-1][:]


def genetic_algorithm_tsp(seed=11, population_size=4, mutation_rate=0.01, generations=200):
    random.seed(seed)
    genes = list(range(1, len(DIST_TSP)))

    population = []
    while len(population) < population_size:
        genome = genes[:]
        random.shuffle(genome)
        if genome not in population:
            population.append(genome)

    best = min(population, key=route_length)
    improvements = [(0, best[:], route_length(best))]

    for generation in range(1, generations + 1):
        new_population = [min(population, key=route_length)[:]]
        while len(new_population) < population_size:
            parent1 = select_parent(population)
            parent2 = select_parent(population)
            child = order_crossover(parent1, parent2)
            mutate(child, mutation_rate)
            new_population.append(child)

        population = new_population
        current_best = min(population, key=route_length)
        if route_length(current_best) < route_length(best):
            best = current_best[:]
            improvements.append((generation, best[:], route_length(best)))

    return best, route_length(best), improvements


# ---------- Task 2: ant colony algorithm for the shortest path ----------
NAMES = ["A", "B", "C", "D", "E", "F", "G"]
INF = math.inf
GRAPH = [
    [INF, 17, 5, INF, 8, INF, INF],
    [17, INF, INF, INF, INF, INF, INF],
    [5, INF, INF, 17, 17, INF, 45],
    [INF, INF, 17, INF, 9, 11, 22],
    [8, INF, 17, 9, INF, INF, INF],
    [INF, INF, INF, 11, INF, INF, 13],
    [INF, INF, 45, 22, INF, 13, INF],
]


def available_neighbors(vertex, visited):
    return [
        u for u, weight in enumerate(GRAPH[vertex])
        if not math.isinf(weight) and u not in visited
    ]


def build_ant_path(start, finish, pheromone, alpha, beta):
    path = [start]
    visited = {start}
    total_length = 0
    current = start

    while current != finish:
        candidates = available_neighbors(current, visited)
        if not candidates:
            return None, math.inf

        desirabilities = []
        for nxt in candidates:
            tau = pheromone[current][nxt] ** alpha
            eta = (1 / GRAPH[current][nxt]) ** beta
            desirabilities.append(tau * eta)

        border = random.random() * sum(desirabilities)
        cumulative = 0
        chosen = candidates[-1]
        for nxt, value in zip(candidates, desirabilities):
            cumulative += value
            if cumulative >= border:
                chosen = nxt
                break

        path.append(chosen)
        visited.add(chosen)
        total_length += GRAPH[current][chosen]
        current = chosen

    return path, total_length


def ant_colony_shortest_path(seed=11, iterations=80, ants_per_iteration=20,
                             alpha=1.0, beta=2.0, evaporation=0.3, q=100):
    random.seed(seed)
    start, finish = 0, 6
    n = len(GRAPH)
    pheromone = [
        [0.0 if math.isinf(GRAPH[i][j]) else 1.0 for j in range(n)]
        for i in range(n)
    ]

    best_path = None
    best_length = math.inf
    improvements = []

    for iteration in range(1, iterations + 1):
        successful_paths = []
        for _ in range(ants_per_iteration):
            path, length = build_ant_path(start, finish, pheromone, alpha, beta)
            if path is not None:
                successful_paths.append((path, length))
                if length < best_length:
                    best_path = path[:]
                    best_length = length
                    improvements.append((iteration, best_path[:], best_length))

        for i in range(n):
            for j in range(n):
                if not math.isinf(GRAPH[i][j]):
                    pheromone[i][j] *= (1 - evaporation)

        for path, length in successful_paths:
            delta = q / length
            for a, b in zip(path, path[1:]):
                pheromone[a][b] += delta
                pheromone[b][a] += delta

    return best_path, best_length, improvements


if __name__ == "__main__":
    best_genome, best_tsp_length, ga_improvements = genetic_algorithm_tsp()
    best_route = [0] + best_genome + [0]
    best_route_text = " -> ".join(str(city + 1) for city in best_route)

    print("TASK 1. GENETIC ALGORITHM FOR TSP")
    print(f"Best route: {best_route_text}")
    print(f"Route length: {best_tsp_length}")
    print("Improvements:")
    for generation, genome, length in ga_improvements:
        route = [0] + genome + [0]
        route_text = " -> ".join(str(city + 1) for city in route)
        print(f"  generation {generation}: {route_text}, length = {length}")

    best_path, best_path_length, aco_improvements = ant_colony_shortest_path()
    best_path_text = " -> ".join(NAMES[i] for i in best_path)

    print()
    print("TASK 2. ANT COLONY ALGORITHM FOR SHORTEST PATH")
    print(f"Best path: {best_path_text}")
    print(f"Path length: {best_path_length}")
    print("Improvements:")
    for iteration, path, length in aco_improvements:
        path_text = " -> ".join(NAMES[i] for i in path)
        print(f"  iteration {iteration}: {path_text}, length = {length}")
