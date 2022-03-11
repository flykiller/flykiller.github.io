---
layout: page
title: Patterns Geometry
permalink: /patterns/geometry
---

Here is a collection of different geometry algorithms.


#### Convex Hull

To find convex hull of points, it is better to use Monotone chains approach. If you need to find convex hull, use the following code.

```python
def remove_middle(a, b, c):
    cross = (a[0] - b[0]) * (c[1] - b[1]) - (a[1] - b[1]) * (c[0] - b[0])
    dot = (a[0] - b[0]) * (c[0] - b[0]) + (a[1] - b[1]) * (c[1] - b[1])
    return cross < 0 or cross == 0 and dot <= 0


def convex_hull(points):
    spoints = sorted(points)
    hull = []
    for p in spoints + spoints[::-1]:
        while len(hull) >= 2 and remove_middle(hull[-2], hull[-1], p):
            hull.pop()
        hull.append(p)
    hull.pop()
    return hull
```

If you need to find convex hull with all points on borders, you can use this code (**TO CHECK**)
```python
def cross (a, b, c):
    return (a[0] - b[0]) * (c[1] - b[1]) - (a[1] - b[1]) * (c[0] - b[0])

def convex_hull(self, points):
    spoints = sorted((x, y) for x, y in points)
    hull = []
    for p in spoints + spoints[::-1]:
        while len(hull) >= 2 and cross(hull[-2], hull[-1], p) < 0:
            hull.pop()
        hull.append(p)

    return set(hull)
```

#### Line functions
Here are some function to work with lines and points with integer coordinates.

1. `get_2dline`: given two points, return equation of line in form `a*x + b*y + c = 0`, where `gcd(a, b, c) > 0`.
2. `dist` is distance between two points.
3. `is_parallel` to check if two lines are paralles or equal.
4. `is_same` to check if two lines the same.
5. `collinear` is to check if `3` points are on the same line.
6. `intersect` is to check if two lines have intersection and if they have, return point.
7. `rotate` is to rotate given point `p` around point `origin` by `theta` radians.

```pyhon
def get_2dline(p1, p2):
    if p1 == p2:
        return (0, 0, 0)
    _p1, _p2 = min(p1, p2), max(p1, p2)
    a, b, c = _p2[1] - _p1[1], _p1[0] - _p2[0], _p1[1] * _p2[0] - _p1[0] * _p2[1]
    g = gcd(gcd(a, b), c)
    return (a // g, b // g, c // g)

dist = lambda p1, p2: sum((a - b) * (a - b) for a, b in zip(p1, p2))**0.5

is_parallel = lambda l1, l2: l1[0] * l2[1] == l2[0] * l1[1]

is_same = lambda l1, l2: is_parallel(l1, l2) and (l1[1] * l2[2] == l2[1] * l1[2])

collinear = lambda p1, p2, p3: is_same(get_2dline(p1, p2), get_2dline(p2, p3))

intersect = (lambda l1, l2: None if is_parallel(l1, l2) else (
    (l2[1] * l1[2] - l1[1] * l2[2]) / (l2[0] * l1[1] - l1[0] * l2[1]),
    (l1[0] * l2[2] - l1[2] * l2[0]) / (l2[0] * l1[1] - l1[0] * l2[1]),
))

rotate = lambda p, theta, origin=(0, 0): (
    origin[0] + (p[0] - origin[0]) * math.cos(theta) - (p[1] - origin[1]) * math.sin(theta),
    origin[1] + (p[0] - origin[0]) * math.sin(theta) + (p[1] - origin[1]) * math.cos(theta),
)
```

#### Polygon functions
Here are some function of polygons.
1. `perimeter` is perimeter of polygon.
2. `area` is area of polygon.
3. `is_in_circle` is to ckeck if given point lies inside given circe.
4. `incircle_radius` is radius of incircle for given triangle.
5. `circumcircle_radius` is radius of circumcircle for given triangle.

```python
perimeter = lambda *p: sum(dist(i, j) for i, j in zip(p, p[1:] + p[:1]))

area = lambda *p: abs(sum(i[0] * j[1] - j[0] * i[1] for i, j in zip(p, p[1:] + p[:1]))) / 2

is_in_circle = lambda p, c, r: sum(i * i - j * j for i, j in zip(p, c)) < r * r

incircle_radius = lambda a, b, c: area(a, b, c) / (perimeter(a, b, c) / 2)

circumcircle_radius = lambda a, b, c: (dist(a, b) * dist(b, c) * dist(c, a)) / (4 * area(a, b, c))
```

#### Vector functions
Here are some functions to work with vertors.

1. `to_vec` is to create vector from two points.
2. `scale` is multiply vector by number.
3. `translate` is to translate vector by another vector.
4. `dot` is dot product of two vectors.
5. `norm_sq` is length of vector.
6. `angle` is angle between two vectors.
7. `cross2d` is length of vector product of two vectors.
8. `cross3d` is 3d vector: vector product of two 3d vectors.
9. `closest_point` is closest point on segment `a, b` (or line `a, b`) to given point `p`.

```python
to_vec = lambda p1, p2: (j - i for i, j in zip(p1, p2))

scale = lambda v, s: (i * s for i in v)

translate = lambda p, v: (pi + vi for pi, vi in zip(p, v))

dot = lambda v1, v2: sum(i * j for i, j in zip(v1, v2))

norm_sq = lambda v: sum(i * i for i in v)

angle = lambda oa, ob: math.acos(dot(oa, ob) / (norm_sq(oa) * norm_sq(ob))**0.5)

cross2d = lambda v1, v2: v1[0] * v2[1] - v1[1] * v2[0]

cross3d = lambda v1, v2: (v1[1] * v2[2] - v1[2] * v2[1], v1[2] * v2[0] - v1[0] * v2[2], v1[0] * v2[1] - v1[1] * v2[0])

def closest_point(p, a, b, segment=False):
    ap, ab = to_vec(a, p), to_vec(a, b)

    u = dot(ap, ab) / norm_sq(ab)

    if segment:
        if u < 0:
            return a
        if u > 1:
            return b

    return translate(a, scale(ab, u))
```