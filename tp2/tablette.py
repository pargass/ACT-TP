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
            return -max(tab_values)

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
        result = -max(tab_values)

    d_memo[state] = result
    return result


acc_memo = {}

def normalize_state(m, n, i, j):
    if m < n:
        m, n = n, m
        i, j = j, i
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
        result = -max(tab_values)

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
    if joueur == 1: #changer joueur
        joueur = 2
    else:    
        joueur = 1

    if m == 1 and n == 1: #condition d'arret
        grid_representation(m, n, i, j)
        if joueur == 1:
            print("Fin du jeu, vous avez gagné ! 🎉")
        else:
            print("Fin du jeu, vous avez perdu. 😥")
        return
    

    grid_representation(m, n, i, j)
    if joueur == 1:
        print("C'est à l'ordinateur de jouer")
    else:
        print("C'est à vous de jouer")

    
    if joueur == 1:
        configurations = possible_configurations(m, n, i, j)
        choices = []
        for config in configurations:
            choices.append(acc_position_value(*config))

        print("Les choix possibles sont : ", choices)
        if min(choices) <= 0:
            index = choices.index(min(choices))
            for i in range(len(choices)):
                if choices[i] <= 0 and choices[i] > choices[index]:
                    index = i
        else:
            index = choices.index(max(choices))
        play(*configurations[index], joueur)
    else:
        test = True
        while test:
            if not (m == 1 or n == 1):
                direction = input("Choisissez une coupe horizontal ou vertical (h / v): ")
            elif m == 1:
                direction = "h"
            else:
                direction = "v"

            if direction == "h":
                n2 = int(input(f"A quelles endroit souhaitez-vous coupez (entre 1 et {n-1}): "))
                if n2 <= j: 
                    print("L'évaluation de votre coup est ",acc_position_value(m, n-n2, i, j-n2))
                    play(m, n-n2, i, j-n2, joueur)
                else:
                    print("L'évaluation de votre coup est ",acc_position_value(m, n2, i, j))
                    play(m, n2, i, j, joueur)
                test = False
            if direction == "v":
                m2 = int(input(f"A quelles endroit souhaitez-vous coupez (entre 1 et {m-1}): "))
                if m2 <= i: 
                    print("L'évaluation de votre coup est ",acc_position_value(m-m2, n, i-m2, j))
                    play(m-m2, n, i-m2, j, joueur)
                else:
                    print("L'évaluation de votre coup est ",acc_position_value(m2, n, i, j))
                    play(m2, n, i, j, joueur)
                test = False


if __name__ == "__main__":
    # print(possible_configurations(5, 5, 2,4))
    # print(position_value(3, 2, 2, 0))

    @timeit
    def test_position_value():
        return position_value(3, 3, 1, 1)

    @timeit
    def test_d_position_value():
        return d_position_value(6, 6, 3, 3)

    @timeit
    def test_acc_position_value():
        return acc_position_value(100, 100, 50, 50)

    print(test_position_value())
    print(test_d_position_value())
    print(test_acc_position_value())

    if len(sys.argv) != 5:
       print("Commande non valide, format accepté: python3 tablette.py <m:nb_colonne> <n:nb_lignes> <i:emplacement x de la case (entre 0 et m-1)> <j:emplacement y de la case (entre 0 et n-1>")
       sys.exit(1)

    m = int(sys.argv[1])
    n = int(sys.argv[2])
    i = int(sys.argv[3])
    j = int(sys.argv[4])

    play(m, n, i, j, 2)

    if len(sys.argv) != 5:
       print("Commande non valide, format accepté: python3 tablette.py <m:nb_colonne> <n:nb_lignes> <i:emplacement x de la case (entre 0 et m-1)> <j:emplacement y de la case (entre 0 et n-1>")
       sys.exit(1)

    m = int(sys.argv[1])
    n = int(sys.argv[2])
    i = int(sys.argv[3])
    j = int(sys.argv[4])

    play(m, n, i, j, 2)
