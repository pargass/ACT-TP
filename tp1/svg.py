import os

def to_svg(points):
    svg = "<svg xmlns=\"http://www.w3.org/2000/svg\" width=\"300\" height=\"150\" viewBox=\"-10 -150 200 150\"><polyline points=\""
    for point in points:
        svg += f"{point[0]},{point[1]} "
    svg += "\"\nstroke=\"blue\" stroke-width=\"0.5\" fill=\"none\" transform=\"scale(10,-10)\"/></svg>"
    return svg

def svg_file(points, filename):
    path = os.path.dirname(os.path.abspath(__file__))
    if not os.path.exists(f"{path}/svg"):
        os.makedirs(f"{path}/svg")
    with open(f"{path}/svg/{filename}.svg", "w") as f:
        f.write(to_svg(points))

data = [
    [(2, 0), (2, 5), (4, 4), (4, 7), (5, 7), (5, 0)],
    [(2, 0), (1, 4), (4, 4), (4, 7), (5, 7), (5, 0)],
    [(2, 0), (2, 5), (4, 5), (4, 7), (5, 7), (5, 0)],
    [(2, 0), (2, 5), (4, 5), (4, 7), (5, 7), (6, 7), (5, 0)],
    [(2, 0), (2, 5), (4, 5), (4, 8), (4, 7), (5, 7), (5, 0)]
]

for i in range(len(data)):
    svg_file(data[i], f"test{i}")