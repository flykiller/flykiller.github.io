def convex_hull_trick(K, M, integer=True):
    intersect = lambda i, j: (M[j] - M[i]) / (K[i] - K[j])

    hull_i, hull_x = [], []
    order = sorted(range(len(K)), key=K.__getitem__)
    for i in order:
        while True:
            if not hull_i:
                hull_i.append(i)
                break
            elif K[hull_i[-1]] == K[i]:
                if M[hull_i[-1]] >= M[i]: break
                hull_i.pop()
                if hull_x: hull_x.pop()
            else:
                x = intersect(i, hull_i[-1])
                if hull_x and x <= hull_x[-1]:
                    hull_i.pop()
                    hull_x.pop()
                else:
                    hull_i += [i]
                    hull_x += [x]
                    break
    return hull_i, hull_x
