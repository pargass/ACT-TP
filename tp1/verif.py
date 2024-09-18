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

folder_path = os.path.dirname(os.path.abspath(__file__)) + "/files"  

filenames = []
for d, _, fs in os.walk(folder_path):
    for f in fs:
        filenames.append(os.path.join(d, f))
input_files = [f for f in filenames if f.endswith("input.txt")]
output_files = [f for f in filenames if f.endswith("output.txt")]
input_files.sort()
output_files.sort()
ids = [f.split("-")[6] for f in input_files]

for i in range(len(input_files)):
    buildings = []
    with open(input_files[i], "r") as f:
        n = int(f.readline())
        for j in range(n):
            buildings.append(tuple(map(int, f.readline().split())))
    roof_line = algo.building_to_roof_line(buildings)
    with open(output_files[i], "r") as f:
        expected = f.read().strip().split("\n")
        expected = [eval(item) for item in expected]
        expected = compact_write(expected)
        # roof_line = uncompact_write(roof_line)
        if len(roof_line) < 20:
            print("ID: ", ids[i])
            print("Expected: ", expected)
            print("Output: ", roof_line)
            print("\n")
            





                

                    