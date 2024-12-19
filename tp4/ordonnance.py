import numpy as np
import time
import random
import matplotlib.pyplot as plt

def read_file(fichier):
    with open(fichier, 'r') as f:
        lignes = f.readlines()

    n = int(lignes[0].strip())
    task = []
    for i in range(1, n + 1):
        pi, wi, di = map(int, lignes[i].strip().split())
        task.append((pi, wi, di))

    return task

def read_opt():
    opt = []
    with open("./opt.txt", 'r') as f:
        lignes = f.readlines()
        for ligne in lignes:
            parts = ligne.strip().split(':')
            if len(parts) == 2:
                opt.append(int(parts[1].strip()))
        return opt


def late2(task, ordonnance):
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
    return ordo

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
    best_late = late2(task, ordo)
    amelio = True
    while amelio: # tant que l'ordonnancement s'améliore
        amelio = False
        neighbors = voisinage(ordo) # on crée les voisins
        for neighbor in neighbors: # on parcourt les voisins
            late_neighbor = late2(task, neighbor) # on calcule le retard de l'ordo
            if late_neighbor < best_late: # si le retard est meilleur
                best_late = late_neighbor
                best_ordo = neighbor
                amelio = True
        ordo = best_ordo
    return best_ordo, best_late

def vnd(task, ordo, voisinages=[generate_neighbor_inv, generate_neighbor_swap, generate_neighbor_insert]):
    best_ordo = ordo
    best_late = late2(task, ordo)
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
    best_late = late2(task, best_solution)

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
    ordo = sorted(range(len(task)), key=lambda i: task[i][1], reverse=True)
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

def heuristic_weightdelay(task):
    ordo = sorted(range(len(task)), key=lambda i: task[i][1]/task[i][2], reverse=True)
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

def analyse():
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

    heuristics = {
        'heuristic_time': heuristic_time,
        'heuristic_weight': heuristic_weight,
        'heuristic_limit': heuristic_limit,
        'heuristic_timeweight': heuristic_timeweight,
        'heuristic_weightdelay': heuristic_weightdelay,
        'random_solution': random_solution,
    }

    test = {
        'hill_climb_neigh_inv': lambda task: hill_climb(task, generate_neighbor_inv, heuristic_weightdelay(task)),
        'hill_climb_neigh_swap': lambda task: hill_climb(task, generate_neighbor_swap, heuristic_weightdelay(task)),
        'hill_climb_neigh_insert': lambda task: hill_climb(task, generate_neighbor_insert, heuristic_weightdelay(task)),
        'vnd_inv_swap_insert': lambda task: vnd(task, heuristic_weightdelay(task)),
        'ils_4': lambda task: ils(task, heuristic_weightdelay(task), perturbation_size=4),
        'ils_8': lambda task: ils(task, heuristic_weightdelay(task), perturbation_size=8),
        'ils_16': lambda task: ils(task, heuristic_weightdelay(task), perturbation_size=16)
    }

    opt = read_opt()

    for heuristic_name, heuristic in heuristics.items():
        print(heuristic_name)
        file = open(f"./results/{heuristic_name}.txt", "w")
        mean = 0
        for i in range(20):
            print(i)
            ordo = heuristic(task[i])
            l = late2(task[i], ordo)
            diff = l - opt[i]
            ratio = l / opt[i]
            file.write(f"{i+1} {opt[i]} {l} {diff} {ratio}\n")
            if i != 15:
                mean += ratio
        print(mean/19)
        file.close()

    for test_name, test_func in test.items():
        print(test_name)
        file = open(f"./results/{test_name}.txt", "w")
        for i in range(20):
            print(i)
            ordo, late = test_func(task[i])
            diff = late - opt[i]
            ratio = late / opt[i]
            file.write(f"{i+1} {opt[i]} {late} {diff} {ratio}\n")
        file.close()

def read_analyse():
    results = {}
    files = ["heuristic_time", "heuristic_weight", "heuristic_limit", "heuristic_timeweight", "heuristic_weightdelay", "random_solution", "hill_climb_neigh_inv", "hill_climb_neigh_swap", "hill_climb_neigh_insert", "vnd_inv_swap_insert", "ils_4", "ils_8", "ils_16"]

    for file in files:
        with open(f"./results/{file}.txt", 'r') as f:
            lignes = f.readlines()
            results[file] = []
            for ligne in lignes:
                parts = ligne.strip().split()
                results[file].append([int(parts[0]), int(parts[1]), int(parts[2]), int(parts[3]), float(parts[4])])

    return results


def plot_analyse(results):
    """
    Plot the results of the analyse in bar charts
    """
    keys = list(results.keys())
    n = len(results[keys[0]])
    x = np.arange(n)
    width = 0.1

    fig, ax = plt.subplots()
    for i, key in enumerate(keys):
        means = [results[key][j][4] for j in range(n)]
        ax.bar(x + i * width, means, width, label=key)

    ax.set_ylabel('Ratio')
    ax.set_title('Ratio of the different algorithms')
    ax.set_xticks(x + width * (len(keys) - 1) / 2)
    ax.set_xticklabels([str(i) for i in range(1, n+1)])
    ax.legend()

    plt.savefig("results.png")
    plt.show()



if __name__ == "__main__":
    # task = np.zeros(20, dtype=object)
    # task[0] = read_file("./SMTWP/n100_15_b.txt")

    # task[1] = read_file("./SMTWP/n100_16_b.txt")
    # task[2]  = read_file("./SMTWP/n100_17_b.txt")
    # task[3]  = read_file("./SMTWP/n100_18_b.txt")
    # task[4]  = read_file("./SMTWP/n100_19_b.txt")
    # task[5]  = read_file("./SMTWP/n100_35_b.txt")
    # task[6]  = read_file("./SMTWP/n100_36_b.txt")
    # task[7]  = read_file("./SMTWP/n100_37_b.txt")
    # task[8]  = read_file("./SMTWP/n100_38_b.txt")
    # task[9]  = read_file("./SMTWP/n100_39_b.txt")
    # task[10]  = read_file("./SMTWP/n100_40_b.txt")
    # task[11]  = read_file("./SMTWP/n100_41_b.txt")
    # task[12]  = read_file("./SMTWP/n100_42_b.txt")
    # task[13]  = read_file("./SMTWP/n100_43_b.txt")
    # task[14]  = read_file("./SMTWP/n100_44_b.txt")
    # task[15]  = read_file("./SMTWP/n100_85_b.txt")
    # task[16]  = read_file("./SMTWP/n100_86_b.txt")
    # task[17]  = read_file("./SMTWP/n100_87_b.txt")
    # task[18]  = read_file("./SMTWP/n100_88_b.txt")
    # task[19]  = read_file("./SMTWP/n100_89_b.txt")

    # ordo_neighbour = [[generate_neighbor_inv, generate_neighbor_swap, generate_neighbor_insert]]
    # perturbation_size = [4, 8, 16]
    # print(read_opt()[0])

    analyse()