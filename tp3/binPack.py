import numpy as np

def check_certificate(certificate, n, weight, c, k):
    """
    Check if the certificate is valid

    Parameters
    ----------
    certificate : list
        The assosiation between the items and the bins
    n : int
        The number of items
    weight : list
        The weight of each item
    c : int
        The capacity of each bin
    k : int
        The number of bins
    ----------

    Returns
    -------
    bool
        True if the certificate is valid, False otherwise
    -------
    """
    if len(certificate) != n: # The certificate does not contain all the items
        return False

    bins = np.zeros(k)

    for i in range(n):
        bin_index = int(certificate[i].item())
        if bin_index >= k:
            return False
        bins[bin_index] += weight[i]

    for i in range(k):
        if bins[i] > c:
            return False

    return True


def generate_certificate(n, k):
    """
    Generate a random certificate

    Parameters
    ----------
    n : int
        The number of items
    k : int
        The number of bins
    ----------

    Returns
    -------
    list
        A random certificate
    -------
    """
    return np.random.randint(0, k, n)

def non_deterministic(n, weight, c, k):
    """
    Solve the bin packing problem with a non-deterministic algorithm

    Parameters
    ----------
    n : int
        The number of items
    weight : list
        The weight of each item
    c : int
        The capacity of each bin
    k : int
        The number of bins
    ----------

    Returns
    -------
    bool
        True if a solution is found, False otherwise
    """
    certificate = generate_certificate(n, k)
    print(certificate)
    return check_certificate(certificate, n, weight, c, k)

def exhaustive(n, weight, c, k):
    """
    Solve the bin packing problem with an exhaustive algorithm

    Parameters
    ----------
    n : int
        The number of items
    weight : list
        The weight of each item
    c : int
        The capacity of each bin
    k : int
        The number of bins
    ----------

    Returns
    -------
    bool
        True if a solution is found, False otherwise
    -------
    """
    for i in range(k**n):
        certificate = np.zeros(n)
        for j in range(n):
            certificate[j] = i // k**j % k
        if check_certificate(certificate, n, weight, c, k):
            print(certificate)
            return True
    return False


def read_data(file):
    with open(file, 'r') as f:
        lines = f.readlines()

    n = int(lines[0].strip())
    x = np.array(list(map(int, lines[1].strip().split())))
    c = int(lines[2].strip())
    k = int(lines[3].strip())

    return n, x, c, k

def reduction_partition_binpack(n, l):
    """
    Reduce the pnartition problem to the bin packing problem

    Parameters
    ----------
    n : int
        The number of items
    l : list
        The list of integers
    ----------
    Returns
    -------
    n : int
        The number of items
    weight : list
        The weight of each item
    c : int
        The capacity of each bin
    k : int
        The number of bins
    -------
    """
    weight = np.array(l)
    c = sum(l) // 2
    k = 2
    return n, weight, c, k

def reduction_sum_partition(n, l, c):
    """
    Reduce the sum problem to the partition problem

    Parameters
    ----------
    n : int
        The number of items
    l : list
        The list of integers
    c : int
        The sum to reach
    ----------
    Returns
    -------
    n : int
        The number of items
    l : list
        The list of integers
    -------
    """
    l = np.append(l,l.sum()-2*c)
    return n+1, l


if __name__ == "__main__":
    # file = "./data.txt"
    # n, x, c, k = read_data(file)
    # choix = -1
    # while(choix < 0 or choix > 2):
    #     choix = int(input(f"Choisissez un mode : verification (0), non-déterministe(1), exploration exhaustive (2) : "))

    # if choix == 0:
    #     certificate = np.zeros(n)
    #     for i in range(n):
    #         certificate[i] = int(input(f"A-quel sac appartient l'objet {i} dont le poids fait {x[i]} ? (Choisir entre 0 et {k-1}) "))
    #     print(check_certificate(certificate, n, x, c, k))
    # else :
    #     if choix == 1:
    #         print(non_deterministic(n,x,c,k))
    #     else:
    #         if choix == 2:
    #             print(exhaustive(n,x,c,k))

    # n = 5
    # l = [3, 2, 4, 3, 3]

    # n, weight, c, k = reduction_partition_binpack(n, l)

    # print(n, weight, c, k)
    # print(exhaustive(n,weight,c,k))

    n, l, c = 3, np.array([1, 4, 6]), 9

    print("instance de sum : \nn = ", n, "\nl = ", l, "\nc = ", c, sep="", end="\n\n")

    n, l = reduction_sum_partition(n, l, c)

    print("instance de partition : \nn = ", n, "\nl = ", l, sep="", end="\n\n")

    n, weight, c, k = reduction_partition_binpack(n, l)

    print("instance de binpack : \nn = ", n, "\nweight = ", weight, "\nc = ", c, "\nk = ", k, sep="", end="\n\n")

    print(exhaustive(n,weight,c,k))