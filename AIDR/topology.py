""" some topology structures and properties for trimesh.Trimesh class"""

import numpy
from trimesh import Trimesh
from trimesh.grouping import group_rows
import numpy as np
import collections


def face_neighbors(mesh: Trimesh):
    """
    get each face's three adjacent faces

    Parameters
    mesh: Trimesh object

    Returns
    f_neighbors: (len(mesh.faces),3)int

    """
    face_adj = mesh.face_adjacency

    # create a default dict object to store the neighbors of each face the default value of dictionary is empty list.
    d = collections.defaultdict(list)
    [(d[a].append(b), d[b].append(a)) for a, b in mesh.face_adjacency]

    f_neighbors = np.array([d[i] for i in range(len(mesh.faces))])

    return f_neighbors


# def edge_faces(mesh: Trimesh):
#     """
#         get each edge's adjacent faces(1 on boundary), corresponding to trimesh.Trimesh.edges_unique
#
#         Returns: face_index - indices of each edge's two adjacent faces
#
#         Return type:(n,2)int
#     """
#
#     groups = group_rows(mesh.edges_sorted, require_count=2)
#     face_index = mesh.edges_face[groups]
#
#     return face_index






