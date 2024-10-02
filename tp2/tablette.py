# m : nombre de colonnes
# n : nombre de lignes

import time


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
            if k == i and l == j:
                print("X ", end="")
            else:
                print("■ ", end="")
        print()


if __name__ == "__main__":
    # print(possible_configurations(5, 5, 2,4))
    # print(position_value(3, 2, 2, 0))

    # t1 = time.time()
    # print(position_value(10, 7, 7, 3))
    # t2 = time.time()
    # print("temps d'execution : ", t2 - t1)

    # t1 = time.time()
    # print(position_value(10, 7, 5, 3))
    # t2 = time.time()
    # print("temps d'execution : ", t2 - t1)
    # t1 = time.time()

    # t1 = time.time()
    # print(position_value(6, 6, 3, 3))
    # t2 = time.time()
    # print("temps d'execution : ", t2 - t1)

    # t1 = time.time()
    # print(d_position_value(6, 6, 3, 3))
    # t2 = time.time()
    # print("temps d'execution : ", t2 - t1)

    # t1 = time.time()
    # print(acc_position_value(6, 6, 3, 3))
    # t2 = time.time()
    # print("temps d'execution : ", t2 - t1)

    # t1 = time.time()
    # print(acc_position_value(100, 100, 50, 50))
    # t2 = time.time()
    # print("temps d'execution : ", t2 - t1)

    # t1 = time.time()
    # print(acc_position_value(100, 100, 48, 52))
    # t2 = time.time()
    # print("temps d'execution : ", t2 - t1)

    grid_representation(20, 20, 10, 10)

