from itertools import combinations

def read_points(path: str):
    points = []
    with open(path) as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            x, y = map(int, line.split(","))
            points.append((x, y))
    return points


def rect_area(p1, p2) -> int:
    x1, y1 = p1
    x2, y2 = p2
    # +1 parce qu’on compte les tuiles, pas juste la distance
    return (abs(x1 - x2) + 1) * (abs(y1 - y2) + 1)


def build_edges(points):
    """Chaque edge = segment entre point i et point i+1 (boucle qui wrap)."""
    edges = []
    n = len(points)
    for i in range(n):
        edges.append((points[i], points[(i + 1) % n]))
    return edges


def edge_crosses_rectangle(edge, rect) -> bool:
    """
    True si l’edge traverse l’INTÉRIEUR du rectangle.
    Les bords qui sont juste sur le bord du rectangle sont OK (autorisés).
    """
    (ex1, ey1), (ex2, ey2) = edge
    (rx1, ry1), (rx2, ry2) = rect

    rx_min, rx_max = sorted((rx1, rx2))
    ry_min, ry_max = sorted((ry1, ry2))

    if ex1 == ex2:
        x = ex1
        ey_min, ey_max = sorted((ey1, ey2))

        if not (rx_min < x < rx_max):
            return False

        if ey_min <= ry_min:
            overlap = ey_max > ry_min
        else:
            overlap = ry_max > ey_min

        return overlap
    else:
        y = ey1
        ex_min, ex_max = sorted((ex1, ex2))

        if not (ry_min < y < ry_max):
            return False

        if ex_min <= rx_min:
            overlap = ex_max > rx_min
        else:
            overlap = rx_max > ex_min

        return overlap


def largest_rectangle_red_green(points):
    edges = build_edges(points)

    rects = []
    n = len(points)
    for i in range(n):
        p1 = points[i]
        for j in range(i + 1, n):
            p2 = points[j]
            if p1[0] == p2[0] or p1[1] == p2[1]:
                continue
            a = rect_area(p1, p2)
            rects.append((a, p1, p2))

    rects.sort(key=lambda t: t[0], reverse=True)

    for area, p1, p2 in rects:
        rect = (p1, p2)
        valid = True
        for e in edges:
            if edge_crosses_rectangle(e, rect):
                valid = False
                break
        if valid:
            return area, p1, p2

    return 0, None, None


def main():
    points = read_points("./data/day09.txt")
    area, p1, p2 = largest_rectangle_red_green(points)
    print("Max area (red+green only):", area)
    print("Corners:", p1, p2)


if __name__ == "__main__":
    main()
