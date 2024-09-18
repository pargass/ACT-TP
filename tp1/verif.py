import os
import algo
import svg

def compact_write(tuples):
    compact = []
    for i in range(len(tuples)):
        if i % 2 == 1:
            compact.append((tuples[i-1][0], tuples[i][1]))
    return compact

def uncompact_write(tuples):
    uncompact = []
    height = 0
    for i in range(len(tuples)):
        uncompact.append((tuples[i][0], height))
        uncompact.append(tuples[i])
        height = tuples[i][1]
    return uncompact

def get_files(folder_path):
    filenames = []
    for d, _, fs in os.walk(folder_path):
        for f in fs:
            filenames.append(os.path.join(d, f))
    input_files = [f for f in filenames if f.endswith("input.txt")]
    output_files = [f for f in filenames if f.endswith("output.txt")]
    input_files.sort()
    output_files.sort()
    ids = [f.split("-")[6] for f in input_files]
    return input_files, output_files, ids

def process_files(input_files, output_files, ids):
    for i in range(len(input_files)):
        buildings = []
        with open(input_files[i], "r") as f:
            n = int(f.readline())
            for j in range(n):
                buildings.append(tuple(map(int, f.readline().split())))
        roof_line = algo.building_to_roof_line(buildings)
        with open(output_files[i], "r") as f:
            expected = [eval(item) for item in f.read().strip().split("\n")]
            roof_line = uncompact_write(roof_line)
            print("ID: ", ids[i], "\n")
            print("Expected: ", expected, "\n")
            print("Output: ", roof_line, "\n")
            if roof_line == expected:
                print("Test passed " + "\033[92m✅\033[0m" + "\n")
            else:
                print("Test failed " + "\033[91m❌\033[0m" + "\n")
            print("=====================================")

def main():
    folder_path = os.path.dirname(os.path.abspath(__file__)) + "/files"
    input_files, output_files, ids = get_files(folder_path)
    process_files(input_files, output_files, ids)

if __name__ == "__main__":
    main()
            





                

                    