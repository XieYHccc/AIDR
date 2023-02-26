import numpy as np
import networkx as nx
import collections
import trimesh
import time
from curvature import edge_based_curvature
import vtkplotlib as vpl
import matplotlib.pyplot as plt
m: trimesh.Trimesh = trimesh.load(r'../data/bi_cleft/0101_Birth_Maxillary_export.stl')

e_curvature, curvature_map = edge_based_curvature(m, True)

vpl.mesh_plot_with_edge_scalars(m.vertices[m.faces], edge_scalars=curvature_map, cmap=["r", "w", "b"])

vpl.show()

# plt.hist(e_curvature, bins=30, density=True, alpha=0.5, color='b')
# plt.show()

