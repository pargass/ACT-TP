# m : nombre de colonnes
# n : nombre de lignes

import time
import sys


def timeit(f):
    def timed(*args, **kw):
        t1 = time.time()
        result = f(*args, **kw)
        t2 = time.time()
        print(f"Temps d'execution de {f.__name__} : {t2 - t1}")
        return result
    return timed

def possible_configurations(m, n , i, j):
    # il y a n - 1 + m - 1 = n + m - 2 configurations possibles
    configurations = []
    for k in range(1, i+1):
        configurations.append((m - k, n, i - k, j))
    for k in range(i+1, m):
        configurations.append((k, n, i, j))
    for k in range(1, j+1):
        configurations.append((m, n - k, i, j - k))
    for k in range(j+1, n):
        configurations.append((m, k, i, j))
    return configurations

# def draw_grid(m, n, i, j):

def position_value(m, n , i, j):
    if m == 1 and n == 1:
        return 0
    else :
        tab_values = []
        for position in possible_configurations(m, n, i, j):
            tab_values.append(position_value(*position))
        if min(tab_values) <= 0:
            negative_values = [v for v in tab_values if v <= 0]
            return abs(max(negative_values)) + 1
        else :
            return -max(tab_values) -1

d_memo = {}

def d_position_value(m, n, i, j):
    state = (m, n, i, j)

    if state in d_memo:
        return d_memo[state]

    if m == 1 and n == 1:
        return 0

    tab_values = []
    for position in possible_configurations(m, n, i, j):
        tab_values.append(d_position_value(*position))

    if min(tab_values) <= 0:
        negative_values = [v for v in tab_values if v <= 0]
        result = abs(max(negative_values)) + 1
    else:
        result = -max(tab_values) - 1

    d_memo[state] = result
    return result


acc_memo = {}

def normalize_state(m, n, i, j):
    if m < n:
        m, n = n, m
        i, j = j, i
    if i > m / 2:
        i = m - i -1
    if j > n / 2:
        j = n - j -1
    return (m, n, i, j)

def acc_position_value(m, n, i, j):
    state = normalize_state(m, n, i, j)

    if state in acc_memo:
        return acc_memo[state]

    if m == 1 and n == 1:
        return 0

    tab_values = []
    for position in possible_configurations(m, n, i, j):
        normalized_position = normalize_state(*position)
        tab_values.append(acc_position_value(*normalized_position))

    if min(tab_values) <= 0:
        negative_values = [v for v in tab_values if v <= 0]
        result = abs(max(negative_values)) + 1
    else:
        result = -max(tab_values) - 1

    acc_memo[state] = result
    return result

def grid_representation(m, n, i, j):
    for k in range(n):
        for l in range(m):
            if l == i and k == j:
                print("☠️ ", end="")
            else:
                print("■ ", end="")
        print()
    print()


def play(m, n, i, j, joueur):
    if m == 1 and n == 1: #condition d'arret
        grid_representation(m, n, i, j)
        if joueur == 1:
            print("Fin du jeu, vous avez gagné ! 🎉")
        else:
            print("Fin du jeu, vous avez perdu. 😥")
        return 

    
    if joueur == 1:
        print("C'est à l'ordinateur de jouer")
        grid_representation(m, n, i, j)
        configurations = possible_configurations(m, n, i, j)
        choices = []
        for config in configurations:
            choices.append(acc_position_value(*config))
            
        if min(choices) <= 0:
            index = choices.index(min(choices))
            for i in range(len(choices)):
                if choices[i] <= 0 and choices[i] > choices[index]:
                    index = i
        else:
            index = choices.index(max(choices))
        play(*configurations[index], 2)
    else:
        print("C'est à vous de jouer")
        grid_representation(m, n, i, j)
        test = True
        while test:
            if not (m == 1 or n == 1):
                direction = input("Choisissez une coupe horizontal ou vertical (h / v): ")
            elif m == 1:
                direction = "h"
            else:
                direction = "v"

            if direction == "h":
                n2 = 0
                while (n2 <= 0 or n2 >= n):
                    n2 = int(input(f"A quelles endroit souhaitez-vous coupez (entre 1 et {n-1}): "))
                    if n2 <= j and n2 > 0: 
                        print("L'évaluation de votre coup est ",acc_position_value(m, n-n2, i, j-n2))
                        play(m, n-n2, i, j-n2, 1)
                    else:
                        if not (n2 <= 0 or n2 >= n):
                            print("L'évaluation de votre coup est ",acc_position_value(m, n2, i, j))
                            play(m, n2, i, j, 1)
                test = False
            if direction == "v":
                m2 = 0
                while (m2 <= 0 or m2 >= m):
                    m2 = int(input(f"A quelles endroit souhaitez-vous coupez (entre 1 et {m-1}): "))
                    print(m2)
                    if m2 <= i and m2 > 0: 
                        print("L'évaluation de votre coup est ",acc_position_value(m-m2, n, i-m2, j))
                        play(m-m2, n, i-m2, j, 1)
                    else:
                        if not (m2 <= 0 or m2 >= n):
                            print("L'évaluation de votre coup est ",acc_position_value(m2, n, i, j))
                            play(m2, n, i, j, 1)
                test = False


def find_127():
    positions = []
    for i in range(127):
        t1 = time.time()
        for j in range(127):
            if acc_position_value(127, 127, i, j) == 127:
                positions.append((i, j))
        t2 = time.time()
        print(t2 - t1)
    return positions


if __name__ == "__main__":
    # print(possible_configurations(5, 5, 2,4))
    # print(position_value(3, 2, 2, 0))

    # @timeit
    # def test_position_value():
    #     return position_value(3, 2, 2, 0)

    # @timeit
    # def test_d_position_value():
    #     return d_position_value(6, 6, 3, 3)

    # @timeit
    # def test_acc_position_value():
    #     return acc_position_value(100, 100, 50, 50)

    # print(test_position_value())
    # print(test_d_position_value())
    # print(test_acc_position_value())

    if len(sys.argv) != 5:
       print("Commande non valide, format accepté: python3 tablette.py <m:nb_colonne> <n:nb_lignes> <i:emplacement x de la case (entre 0 et m-1)> <j:emplacement y de la case (entre 0 et n-1>")
       sys.exit(1)

    m = int(sys.argv[1])
    n = int(sys.argv[2])
    i = int(sys.argv[3])
    j = int(sys.argv[4])

    # play(m, n, i, j, 2)

    # print(normalize_state(6,4,1,0))
    # print(normalize_state(6,4,1,3))
    # print(normalize_state(6,4,4,0))
    # print(normalize_state(6,4,4,3))

    # print(normalize_state(4,6,0,1))
    # print(normalize_state(4,6,3,1))
    # print(normalize_state(4,6,0,4))
    # print(normalize_state(4,6,3,4))

    tuple = (1,2,3)

