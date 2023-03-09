import numpy as np
import trimesh as tm
from collections import defaultdict


def edge_based_curvature(mesh: tm.Trimesh, get_map=False):
    """
        correspond to trimesh.Trimesh.face_adjacency, ignore edges on the boundary,
        but for watertight mesh, face_adjacency also correspond to edges_unique.
        edge based curvature = |(n0 x n1)|/|△x|.Triangles are referenced by
        argument based on the order they are listed in Trimesh.faces
    """

    face_adj = mesh.face_adjacency
    face_normals = mesh.face_normals

    # get face normals for each pair
    face_normals_adj = face_normals[face_adj]
    cross_product = np.cross(face_normals_adj[:, 0, :], face_normals_adj[:, 1, :])
    curvature = np.linalg.norm(cross_product, axis=1)
    face_center_pair = mesh.triangles_center[face_adj]
    # calculate vector form face0's center to face1's center
    c2c_vector = np.diff(face_center_pair, axis=1).reshape(-1, 3)
    c2c_vector_norm = np.linalg.norm(c2c_vector, axis=1)

    curvature = curvature / c2c_vector_norm
    sign = np.sign(np.sum(face_normals_adj[:, 0, :] * c2c_vector, axis=1))
    curvature = -sign * curvature

    if get_map:
        d = defaultdict(list)
        [(d[a].append(curvature[i]), d[b].append(curvature[i])) for i, (a, b) in enumerate(mesh.face_adjacency)]
        curvature_map = np.array([d[i] for i in range(len(mesh.faces))])
        return curvature, curvature_map

    return curvature
