import random
import numpy as np

# Parameter
NUM_CATEGORIES = 4  # Misalnya, kebutuhan pokok, tabungan, hiburan, dan investasi
POP_SIZE = 20       # Ukuran populasi
GENERATIONS = 50    # Jumlah generasi
MUTATION_RATE = 0.01  # Tingkat mutasi

# Meminta input rata-rata pemasukan dari user
average_income = int(input("Masukkan rata-rata pemasukan bulanan Anda: "))

# Meminta input bobot prioritas dari user untuk setiap kategori
categories = ["Kebutuhan Pokok", "Tabungan", "Hiburan", "Investasi"]
priorities = []
print("\nMasukkan tingkat kepentingan untuk setiap kategori (1-10, di mana 10 paling penting):")
for category in categories:
    priority = int(input(f"{category}: "))
    priorities.append(priority)

# Menormalisasi bobot prioritas
priority_weights = np.array(priorities) / np.sum(priorities)

# Fungsi Fitness: Optimasi untuk mendekati batas pengeluaran yang efisien
def fitness(expenses):
    total_expenses = np.sum(expenses)
    if total_expenses > average_income:
        return 0  # Penalti jika melebihi pemasukan
    return total_expenses / average_income

# Inisialisasi populasi
def initialize_population():
    return [priority_weights * average_income * np.random.rand(NUM_CATEGORIES) for _ in range(POP_SIZE)]

# Seleksi individu terbaik
def select(population):
    fitness_scores = np.array([fitness(ind) for ind in population])
    return population[np.argmax(fitness_scores)]

# Crossover
def crossover(parent1, parent2):
    point = random.randint(1, NUM_CATEGORIES - 1)
    child = np.concatenate((parent1[:point], parent2[point:]))
    return (child / np.sum(child)) * average_income  # Normalisasi ke rata-rata pemasukan

# Mutasi
def mutate(individual):
    if random.random() < MUTATION_RATE:
        idx = random.randint(0, NUM_CATEGORIES - 1)
        individual[idx] += np.random.uniform(-0.05, 0.05) * average_income
        individual = np.abs(individual)  # Pastikan nilai positif
        individual = (individual / np.sum(individual)) * average_income  # Normalisasi
    return individual

# Algoritma Genetik
population = initialize_population()
for gen in range(GENERATIONS):
    new_population = []
    for _ in range(POP_SIZE // 2):
        parent1, parent2 = random.choices(population, k=2)
        child1, child2 = crossover(parent1, parent2), crossover(parent2, parent1)
        new_population.extend([mutate(child1), mutate(child2)])
    population = new_population
    best_solution = select(population)
    print(f"Generation {gen + 1}, Best Fitness: {fitness(best_solution)}")

# Hasil akhir
optimal_expenses = best_solution

print("\nOptimal Expense Allocation:")
for i, category in enumerate(categories):
    print(f"{category}: Rp {optimal_expenses[i]:,.0f}")

print(f"\nTotal Expenses: Rp {np.sum(optimal_expenses):,.0f} (Target Income: Rp {average_income:,.0f})")
