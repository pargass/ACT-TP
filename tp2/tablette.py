def possible_configurations(m, n , i, j):
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

def draw_grid(m, n, i, j):


if __name__ == "__main__":
    print(possible_configurations(1, 2, 0, 1))