def to_svg(l):
    svg = "<svg xmlns=\"http://www.w3.org/2000/svg\" width=\"300\" height=\"200\" viewBox=\"-10 -150 200 150\"><polyline points=\""
    for i in range(len(l)):
        svg += str(l[i][0]) + "," + str(l[i][1]) + " "
    svg += "\"\nstroke=\"blue\" stroke-width=\"1\" fill=\"none\" transform=\"scale(5,-5)\"/></svg>"
    return svg

def svg_file(l, filename):
    with open("svg/" + filename  + ".svg", "w") as f:
        f.write(to_svg(l))