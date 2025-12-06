import random
import math

# ------------------------------
# Objective function
# ------------------------------
def objective(x):
    return x**2       # minimize x^2

# ------------------------------
# ABC Algorithm
# ------------------------------
def artificial_bee_colony(
        num_bees=10,
        max_iter=50,
        limit=5,
        lb=-10,
        ub=10
    ):
    
    # Initialize population
    population = [random.uniform(lb, ub) for _ in range(num_bees)]
    fitness = [1 / (1 + objective(x)) for x in population]
    trial = [0] * num_bees

    def mutate(i):
        # pick a different random bee k
        k = random.choice([idx for idx in range(num_bees) if idx != i])
        phi = random.uniform(-1, 1)
        v = population[i] + phi * (population[i] - population[k])
        return max(lb, min(ub, v))  # boundary check

    for iteration in range(max_iter):

        # --------------------------
        # Employed Bee Phase
        # --------------------------
        for i in range(num_bees):
            v = mutate(i)
            if objective(v) < objective(population[i]):
                population[i] = v
                fitness[i] = 1 / (1 + objective(v))
                trial[i] = 0
            else:
                trial[i] += 1

        # --------------------------
        # Onlooker Bee Phase
        # --------------------------
        total_fit = sum(fitness)
        probs = [f / total_fit for f in fitness]

        for _ in range(num_bees):
            # roulette-wheel selection
            i = random.choices(range(num_bees), weights=probs, k=1)[0]
            v = mutate(i)

            if objective(v) < objective(population[i]):
                population[i] = v
                fitness[i] = 1 / (1 + objective(v))
                trial[i] = 0
            else:
                trial[i] += 1
        
        # --------------------------
        # Scout Bee Phase
        # --------------------------
        for i in range(num_bees):
            if trial[i] >= limit:
                population[i] = random.uniform(lb, ub)
                fitness[i] = 1 / (1 + objective(population[i]))
                trial[i] = 0

        # Track progress
        best = min(population, key=lambda x: objective(x))
        print(f"Iteration {iteration+1:3d} | Best x = {best:.5f} | f(x) = {objective(best):.6f}")

    return best

# ------------------------------
# Run ABC
# ------------------------------
best_solution = artificial_bee_colony(
    num_bees=10,
    max_iter=40,
    limit=5,
    lb=-10,
    ub=10
)

print("\nFinal Best Solution:", best_solution)
print("Objective Value:", objective(best_solution))
