""" some topology properties for trimesh.Trimesh structure"""

import numpy
from trimesh import Trimesh
from trimesh.grouping import group_rows


def face_neighbors(mesh:Trimesh):




def edge_faces(mesh: Trimesh):
    """
        get two adjacent faces for each edge(in order of edges_unique below),
        but ignore edges on boundary

        Returns: face_index - indices of each edge's two adjacent faces

        Return type:(n,2)int
    """
    groups = group_rows(mesh.edges_sorted, require_count=2)
    face_index = mesh.edges_face[groups]

    return face_index


def edges_unique(mesh: Trimesh):
    """ignore edges on boundary"""

    groups = group_rows(mesh.edges_sorted, require_count=2)
    edges = mesh.edges_sorted[groups[:, 0]]

    return edges
