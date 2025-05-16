import gudhi as gd
import numpy as np

# Sample points in 2D
points = [(336, 190), (401, 178), (378, 231)]

def group_by_dim(simplices):
    grouped = {}
    for simplex in simplices:
        dim = len(simplex) - 1
        grouped.setdefault(dim, []).append(simplex)
    # Sort the dictionary by dimension keys and return the list of lists
    return [grouped[dim] for dim in sorted(grouped)]

def cech_filtration(points, r):
    complex = gd.DelaunayCechComplex(points=np.array(points))
    simplex_tree = complex.create_simplex_tree(max_alpha_square=r*r)
    return group_by_dim([[points[i] for i in simplex[0]] for simplex in simplex_tree.get_filtration()])


def vr_filtration(points, r):
    complex = gd.RipsComplex(points=np.array(points), max_edge_length=2 * r)
    simplex_tree = complex.create_simplex_tree(max_dimension=2)
    return group_by_dim([[points[i] for i in simplex[0]] for simplex in simplex_tree.get_filtration()])


print(vr_filtration(points, float('inf')))

