import numpy as np

import AIDR.topology
import trimesh

m: trimesh.Trimesh = trimesh.load(r'../data/bi_cleft/0282_BIRTH_Maxillary_export.stl')

e = AIDR.topology.edge_faces(m)

e1 = m.face_adjacency_edges
e2 = m.edges_unique

print(np.array_equal(e1, e2))

