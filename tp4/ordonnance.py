import numpy as np
import time

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

def vnd(task , ordo):
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
    task1 = read_file("./SMTWP/n100_15_b.txt")
    # print(task1)
    # heuristic_time_by_weight_coef_limit(task1)
    # random = ("Random", random_solution(task1))
    # time = ("Time", late(task1, heuristic_time(task1)))
    # weight = ("Weight", late(task1, heuristic_weight(task1)))
    # limit = ("Limit", late(task1, heuristic_limit(task1)))
    # timeweight = ("TimeWeight", late(task1, heuristic_timeweight(task1)))
    # time_weight_limit = ("TimeWeightLimit", late(task1, heuristic_time_by_weight_coef_limit(task1)))

    # liste = [random, time, weight, limit, timeweight, time_weight_limit]
    # for i in sorted(liste, key=lambda i: i[1]):
    #     print(i[0],":", i[1])

    # print(generate_neighbor_inv([1,2,3,4,5]))
    # print(generate_neighbor_swap([1,2,3,4,5]))
    # print(generate_neighbor_insert([1,2,3,4,5]))

    # time1 = time.time()
    # print(hill_climb(task1, generate_neighbor_inv, heuristic_time(task1))[1]- 172995)
    # time2 = time.time()
    # print(time2-time1)
    # time1 = time.time()
    # print(hill_climb(task1, generate_neighbor_swap, heuristic_time(task1))[1]- 172995)
    # time2 = time.time()
    # print(time2-time1)
    # time1 = time.time()
    # print(hill_climb(task1, generate_neighbor_insert, heuristic_time(task1))[1]- 172995)
    # time2 = time.time()
    # print(time2-time1)
    # time1 = time.time()
    print(vnd(task1, heuristic_time(task1)))
    # time2 = time.time()
    # print(time2-time1)
