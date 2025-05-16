import itertools

import gudhi as gd
import numpy as np
from scipy.spatial import Voronoi

from scipy.spatial import voronoi_plot_2d
import matplotlib.pyplot as plt


def group_by_dim(simplices):
    grouped = {}
    for simplex in simplices:
        dim = len(simplex) - 1
        grouped.setdefault(dim, []).append(simplex)
    # Sort the dictionary by dimension keys and return the list of lists
    return [grouped[dim] for dim in sorted(grouped)]


def cech_filtration(points, r):
    complex = gd.DelaunayCechComplex(points=np.array(points))
    simplex_tree = complex.create_simplex_tree(max_alpha_square=r * r)
    return group_by_dim(
        [[points[i] for i in simplex[0]] for simplex in simplex_tree.get_filtration()]
    )


def vr_filtration(points, r):
    complex = gd.RipsComplex(points=np.array(points), max_edge_length=2 * r)
    simplex_tree = complex.create_simplex_tree(max_dimension=2)
    return group_by_dim(
        [[points[i] for i in simplex[0]] for simplex in simplex_tree.get_filtration()]
    )



# def voronoi_lines(points, width, height):
#
#     def are_colinear(p1, p2, p3):
#
#
#     points = np.array([list(map(float, point)) for point in points])
#     if len(points) <= 2:
#         return []
#     boundaries = []
#     vor = Voronoi(points)
#     fig = voronoi_plot_2d(vor)
#     plt.show()
#
#
#
#     return vor.regions
#
#
#
# # Test with a bounding box of WIDTH x HEIGHT
# WIDTH, HEIGHT = 1000, 800
# points = [[119.0, 524.0], [220.0, 335.0], [300.0, 400.0]]
# lines = voronoi_lines(points, width=WIDTH, height=HEIGHT)
#
# print("\nVoronoi boundary lines (clipped to box):")
# for line in lines:
#     print(line)
