import numpy as np
import matplotlib.pyplot as plt

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


def plot_analyse_ratio_mean(results):
    """
    Plot the results of the analyse in bar charts
    """
    keys = list(results.keys())
    ratios = {}
    for key in keys:
        mean = 0
        for i in range(20):
            if i != 15:
                mean += results[key][i][4]
        mean /= 19
        ratios[key] = mean

    ratios = dict(sorted(ratios.items(), key=lambda item: item[1], reverse=True))

    fig, ax = plt.subplots(figsize=(12, 8))
    bars = ax.bar(ratios.keys(), ratios.values())

    ax.set_ylabel('Mean ratio')
    ax.set_title('Mean ratio for each heuristic')
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()

    # Add mean values on top of the bars
    for bar in bars:
        height = bar.get_height()
        ax.annotate(f'{height:.2f}',
                    xy=(bar.get_x() + bar.get_width() / 2, height),
                    xytext=(0, 3),  # 3 points vertical offset
                    textcoords="offset points",
                    ha='center', va='bottom')

    plt.savefig("results_ratio.png")

def plot_analyse_sum_diff(results):
    """
    Plot the results of the analyse in bar charts
    """
    keys = list(results.keys())
    ratios = {}
    for key in keys:
        sum = 0
        for i in range(20):
            if i != 15:
                sum += results[key][i][3]
        ratios[key] = sum

    ratios = dict(sorted(ratios.items(), key=lambda item: item[1], reverse=True))

    fig, ax = plt.subplots(figsize=(12, 8))
    bars = ax.bar(ratios.keys(), ratios.values())

    ax.set_ylabel('Mean sum of late tasks')
    ax.set_title('Mean sum of late tasks for each heuristic')
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()

    # Add mean values on top of the bars
    for bar in bars:
        height = bar.get_height()
        ax.annotate(f'{height:.2f}',
                    xy=(bar.get_x() + bar.get_width() / 2, height),
                    xytext=(0, 3),  # 3 points vertical offset
                    textcoords="offset points",
                    ha='center', va='bottom')

    plt.savefig("results_diff.png")


if __name__ == "__main__":
    results = read_analyse()
    plot_analyse_ratio_mean(results)
    plot_analyse_sum_diff(results)