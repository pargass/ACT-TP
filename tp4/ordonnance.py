import numpy as np

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
        sum += task[el][2] * Tj
    return sum

def random_solution(task):
    ordo = np.arange(100)
    ordo = np.random.permutation(ordo)
    return late(task, ordo)

#Voisinage
def generate_neighbor1(ordonnance):
    neighbors = []
    n = len(ordonnance)
    for i in range(n-1):
        neighbor = ordonnance.copy()
        neighbor[i], neighbor[i+1] = neighbor[i+1], neighbor[i]
        neighbors.append(neighbor)
    return neighbors

def generate_neighbor2(ordonnance):
    neighbors = []
    n = len(ordonnance)
    for i in range(n):
        for j in range(i + 1, n):
            neighbor = ordonnance.copy()
            neighbor[i], neighbor[j] = neighbor[j], neighbor[i]
            neighbors.append(neighbor)
    return neighbors

def hill_climb(task,voisinage,ordo):
    best_ordo = ordo
    best_late = late(task, ordo)
    amelio = True
    while amelio:
        amelio = False
        neighbors = voisinage(ordo)
        for neighbor in neighbors:
            late_neighbor = late(task, neighbor)
            if late_neighbor < best_late:
                best_late = late_neighbor
                best_ordo = neighbor
                amelio = True
        ordo = best_ordo
    return best_ordo, best_late

def vnd(task , ordo):
    best_ordo = ordo
    best_late = late(task, ordo)
    voisinages = [generate_neighbor2, generate_neighbor1]
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
    

if __name__ == "__main__":
    task1 = read_file("./SMTWP/n100_15_b.txt")
    print(random_solution(task1))
    ordo = heuristic_weight(task1)
    print(vnd(task1, ordo))
