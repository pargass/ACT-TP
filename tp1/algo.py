def merge_roof_line(l1, l2):
    i1 = 0
    i2 = 0
    h1 = 0
    h2 = 0
    d = 0
    hMax = 0
    merged = []

    while i1 < len(l1) and i2 < len(l2):
        if l1[i1][0] < l2[i2][0]:
            d = l1[i1][0]
            h1 = l1[i1][1]
            hMax = max(h1, h2)
            i1 += 1
        else:
            if l1[i1][0] > l2[i2][0]:
                d = l2[i2][0]
                h2 = l2[i2][1]
                hMax = max(h1, h2)
                i2 += 1
            else:
                d = l1[i1][0]
                h1 = l1[i1][1]
                h2 = l2[i2][1]
                hMax = max(h1, h2)
                i1 += 1
                i2 += 1

        if len(merged) == 0 or hMax != merged[-1][1]:
            merged.append([d, hMax])

    merged += l1[i1:]
    merged += l2[i2:]

    return merged

def to_svg(l):
    svg = "<svg xmlns=\"http://www.w3.org/2000/svg\" width=\"300\" height=\"200\" viewBox=\"-10 -150 200 150\"><polyline points=\""
    for i in range(len(l)):
        svg += str(l[i][0]) + "," + str(l[i][1]) + " "
    svg += "\"stroke=\"blue\" stroke-width=\"1\" fill=\"none\" transform=\"scale(5,-5)\"/></svg>"
    return svg

def svg_file(l, filename):
    with open(filename  + ".svg", "w") as f:
        f.write(to_svg(l))

def roof_line(l):
    if len(l) == 1:
        return l
    else:
        return merge_roof_line(roof_line(l[:len(l)//2]), roof_line(l[len(l)//2:]))
    



if __name__ == "__main__":
    l1 = [(1, 10), (5, 6), (8, 0), (10, 8), (12, 0)]
    l2 = [(2, 12), (7, 0), (9, 4), (11, 2), (14, 0)]
    print(merge_roof_line(l1, l2))

    l = [(3, 13, 9), (1, 11, 5), (19, 18, 22), (3, 6, 7), (16, 3, 25), (12, 7, 16)]
