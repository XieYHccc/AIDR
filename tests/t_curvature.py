import numpy as np
import networkx as nx
import collections
import trimesh
import time
from AIDR.curvature import edge_based_curvature
import vtkplotlib as vpl
import matplotlib.pyplot as plt
m: trimesh.Trimesh = trimesh.load(r'../data/bi_cleft/0101_Birth_Maxillary_export.stl')
e_curvature, curvature_map = edge_based_curvature(m, True)
plot = vpl.mesh_plot_with_edge_scalars(m.vertices[m.faces], edge_scalars=curvature_map,
                                       cmap=["r", 'w', "b"])
range = np.nanstd(e_curvature) * 2
plot.scalar_range = (-range, range)
bar = vpl.scalar_bar(plot, "Curvature")
bar.set_horizontal()
bar.size = .8, .1
bar.position = .1, .05
vpl.show()