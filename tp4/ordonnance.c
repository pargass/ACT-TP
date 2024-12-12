#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>

#define MAX_TASKS 100
#define MAX_ITER 10

typedef struct {
    int pi; // Processing time
    int wi; // Weight
    int di; // Due date
} Task;

Task* read_file(const char* filename, int* task_count) {
    FILE* file = fopen(filename, "r");
    if (!file) {
        perror("Error opening file");
        exit(EXIT_FAILURE);
    }

    fscanf(file, "%d", task_count);
    Task* tasks = (Task*)malloc(*task_count * sizeof(Task));
    for (int i = 0; i < *task_count; i++) {
        fscanf(file, "%d %d %d", &tasks[i].pi, &tasks[i].wi, &tasks[i].di);
    }

    fclose(file);
    return tasks;
}

int late(Task* tasks, int* order, int task_count) {
    int time = 0, Cj = 0, total = 0;
    for (int i = 0; i < task_count; i++) {
        int idx = order[i];
        Cj += tasks[idx].pi;
        int Tj = Cj > tasks[idx].di ? Cj - tasks[idx].di : 0;
        total += tasks[idx].wi * Tj;
    }
    return total;
}

void random_solution(int* order, int task_count) {
    for (int i = 0; i < task_count; i++) {
        order[i] = i;
    }
    for (int i = 0; i < task_count; i++) {
        int j = rand() % task_count;
        int temp = order[i];
        order[i] = order[j];
        order[j] = temp;
    }
}

void generate_neighbor_swap(int* order, int task_count, int** neighbors, int* neighbor_count) {
    *neighbor_count = (task_count * (task_count - 1)) / 2;
    *neighbors = (int*)malloc((*neighbor_count) * task_count * sizeof(int));
    int k = 0;
    for (int i = 0; i < task_count; i++) {
        for (int j = i + 1; j < task_count; j++) {
            memcpy(*neighbors + k * task_count, order, task_count * sizeof(int));
            int temp = (*neighbors + k * task_count)[i];
            (*neighbors + k * task_count)[i] = (*neighbors + k * task_count)[j];
            (*neighbors + k * task_count)[j] = temp;
            k++;
        }
    }
}

void hill_climb(Task* tasks, int* order, int task_count, int* best_order, int* best_late) {
    memcpy(best_order, order, task_count * sizeof(int));
    *best_late = late(tasks, order, task_count);
    int amelio = 1;

    while (amelio) {
        amelio = 0;
        int* neighbors;
        int neighbor_count;
        generate_neighbor_swap(order, task_count, &neighbors, &neighbor_count);

        for (int i = 0; i < neighbor_count; i++) {
            int* neighbor = neighbors + i * task_count;
            int current_late = late(tasks, neighbor, task_count);
            if (current_late < *best_late) {
                *best_late = current_late;
                memcpy(best_order, neighbor, task_count * sizeof(int));
                amelio = 1;
            }
        }

        free(neighbors);
        memcpy(order, best_order, task_count * sizeof(int));
    }
}

void perturbation(int* order, int task_count) {
    int quarter_size = task_count / 4;
    int start1 = rand() % 3;
    int start2 = start1 + 1;
    for (int i = 0; i < quarter_size; i++) {
        int temp = order[start1 * quarter_size + i];
        order[start1 * quarter_size + i] = order[start2 * quarter_size + i];
        order[start2 * quarter_size + i] = temp;
    }
}

void ils(Task* tasks, int task_count, int* initial_order, int* best_order, int* best_late) {
    memcpy(best_order, initial_order, task_count * sizeof(int));
    *best_late = late(tasks, initial_order, task_count);

    for (int iter = 0; iter < MAX_ITER; iter++) {
        int current_order[MAX_TASKS];
        memcpy(current_order, best_order, task_count * sizeof(int));
        int current_late;

        hill_climb(tasks, current_order, task_count, current_order, &current_late);

        if (current_late < *best_late) {
            memcpy(best_order, current_order, task_count * sizeof(int));
            *best_late = current_late;
        }

        perturbation(current_order, task_count);
        current_late = late(tasks, current_order, task_count);
    }
}

int main() {
    srand(time(NULL));

    int task_count;
    Task* tasks = read_file("./SMTWP/n100_15_b.txt", &task_count);

    int initial_order[MAX_TASKS];
    random_solution(initial_order, task_count);

    int best_order[MAX_TASKS];
    int best_late;

    ils(tasks, task_count, initial_order, best_order, &best_late);

    printf("Best lateness: %d\n", best_late);
    free(tasks);

    return 0;
}
