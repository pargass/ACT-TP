import numpy as np
import time
import random

def read_file(fichier):
    with open(fichier, 'r') as f:
        lignes = f.readlines()

    n = int(lignes[0].strip())
    task = []
    for i in range(1, n + 1):
        pi, wi, di = map(int, lignes[i].strip().split())
        task.append((pi, wi, di))

    return task


def late(task, ordonnance):
    time = 0
    Cj = 0
    sum = 0
    for el in ordonnance:
        Cj += task[el][0]
        Tj = max(Cj - task[el][2], 0)
        sum += task[el][1] * Tj
    return sum

def random_solution(task):
    ordo = np.arange(100)
    ordo = np.random.permutation(ordo)
    return late(task, ordo)

#Voisinage
def generate_neighbor_inv(ordonnance):
    neighbors = []
    n = len(ordonnance)
    for i in range(n-1):
        neighbor = ordonnance.copy()
        neighbor[i], neighbor[i+1] = neighbor[i+1], neighbor[i]
        neighbors.append(neighbor)
    return neighbors

def generate_neighbor_swap(ordonnance):
    neighbors = []
    n = len(ordonnance)
    for i in range(n):
        for j in range(i + 1, n):
            neighbor = ordonnance.copy()
            neighbor[i], neighbor[j] = neighbor[j], neighbor[i]
            neighbors.append(neighbor)
    return neighbors

def generate_neighbor_insert(ordonnance):
    neighbors = []
    n = len(ordonnance)
    for i in range(n):
        for j in range(n):
            if i != j:
                neighbor = ordonnance.copy()
                neighbor.insert(j, neighbor.pop(i))
                neighbors.append(neighbor)
    return neighbors


def hill_climb(task,voisinage,ordo):
    best_ordo = ordo
    best_late = late(task, ordo)
    amelio = True
    while amelio: # tant que l'ordonnancement s'améliore
        amelio = False
        neighbors = voisinage(ordo) # on crée les voisins
        for neighbor in neighbors: # on parcourt les voisins
            late_neighbor = late(task, neighbor) # on calcule le retard de l'ordo
            if late_neighbor < best_late: # si le retard est meilleur
                best_late = late_neighbor
                best_ordo = neighbor
                amelio = True
        ordo = best_ordo
    return best_ordo, best_late

def vnd(task, ordo, voisinages=[generate_neighbor_inv, generate_neighbor_swap, generate_neighbor_insert]):
    best_ordo = ordo
    best_late = late(task, ordo)
    voisinages = [generate_neighbor_inv, generate_neighbor_swap, generate_neighbor_insert]
    k = 0
    while k <= len(voisinages)-1:
        ordo_n, late_n = hill_climb(task, voisinages[k] ,best_ordo)
        if  late_n < best_late:
            best_ordo = ordo_n
            best_late = late_n
            k = 0
        else:
            k += 1
    return best_ordo, best_late

# Perturbation
def perturbation(solution, size):
    n = len(solution)

    if size <= 0 or size > n:
        raise ValueError("Size must be between 1 and the length of the solution")

    slice_size = n // size
    slices = [solution[i * slice_size:(i + 1) * slice_size] for i in range(size)]

    leftover = n % size
    if leftover:
        slices[-1].extend(solution[-leftover:])

    i = random.randint(0, size - 2)
    slices[i], slices[i + 1] = slices[i + 1], slices[i]

    perturbed_solution = []
    for slice in slices:
        perturbed_solution.extend(slice)

    return perturbed_solution



def ils(task, ordo, max_iter=10, perturbation_size=4, reset=False):
    best_solution = ordo
    best_late = late(task, best_solution)

    current_solution, current_late = vnd(task, best_solution)

    for iteration in range(max_iter):
        p_solution = perturbation(current_solution, perturbation_size)
 
        tmp_solution, tmp_late = vnd(task, p_solution)

        if tmp_late < best_late:
            best_solution = tmp_solution
            best_late = tmp_late
            current_solution = tmp_solution
            if reset:
                iteration = 0

    return best_solution, best_late


#Glouton
#Heuristic les tache les plus courtes d'abord
def heuristic_time(task):
    ordo = sorted(range(len(task)), key=lambda i: task[i][0])
    return ordo

#Heuristic les poids les plus lourd d'abord
def heuristic_weight(task):
    ordo = sorted(range(len(task)), key=lambda i: task[i][1])
    return ordo

#Heuristic les limit les plus courtes d'abord
def heuristic_limit(task):
    ordo = sorted(range(len(task)), key=lambda i: task[i][2])
    return ordo

#Heuristic les poids les plus lourd d'abord
def heuristic_timeweight(task):
    ordo = sorted(range(len(task)), key=lambda i: task[i][0]*task[i][1])
    return ordo

def heuristic_timeweightdelay(task):
    ordo = sorted(range(len(task)), key=lambda i: task[i][1]/(task[i][2]*task[i][0]), reverse=True)
    return ordo

def heuristic_time_by_weight_coef_limit(task):
    ordo_1 = sorted(range(len(task)), key=lambda i: task[i][0]*task[i][1]) # car taches les plus couteuses d'abord
    ordo_2 = sorted(range(len(task)), key=lambda i: task[i][2]) # car taches avec limites les plus courtes d'abord
    order = []
    for i in range(len(task)):
        idx1 = ordo_1.index(i)
        idx2 = ordo_2.index(i)
        order.append((i, idx1 + idx2))
    ordo = [i[0] for i in sorted(order, key=lambda i: i[1])]
    return ordo

if __name__ == "__main__":
    task = np.zeros(20, dtype=object)
    task[0] = read_file("./SMTWP/n100_15_b.txt")

    task[1] = read_file("./SMTWP/n100_16_b.txt")
    task[2]  = read_file("./SMTWP/n100_17_b.txt")
    task[3]  = read_file("./SMTWP/n100_18_b.txt")
    task[4]  = read_file("./SMTWP/n100_19_b.txt")
    task[5]  = read_file("./SMTWP/n100_35_b.txt")
    task[6]  = read_file("./SMTWP/n100_36_b.txt")
    task[7]  = read_file("./SMTWP/n100_37_b.txt")
    task[8]  = read_file("./SMTWP/n100_38_b.txt")
    task[9]  = read_file("./SMTWP/n100_39_b.txt")
    task[10]  = read_file("./SMTWP/n100_40_b.txt")
    task[11]  = read_file("./SMTWP/n100_41_b.txt")
    task[12]  = read_file("./SMTWP/n100_42_b.txt")
    task[13]  = read_file("./SMTWP/n100_43_b.txt")
    task[14]  = read_file("./SMTWP/n100_44_b.txt")
    task[15]  = read_file("./SMTWP/n100_85_b.txt")
    task[16]  = read_file("./SMTWP/n100_86_b.txt")
    task[17]  = read_file("./SMTWP/n100_87_b.txt")
    task[18]  = read_file("./SMTWP/n100_88_b.txt")
    task[19]  = read_file("./SMTWP/n100_89_b.txt")

    for i in range(len(task)):
        print("Ils ",i," : ", ils(task[i] , heuristic_timeweightdelay(task[i]), 10, 8))

