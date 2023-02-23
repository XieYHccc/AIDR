import trimesh
import numpy as np


class local_height_maximum_finder:
    """
    """

    _mask: np.ndarray
    _mesh: trimesh.Trimesh
    _height_direction: np.ndarray

    @property
    def mask(self):
        return self._mask

    def __init__(self, mesh: trimesh.Trimesh, height_direction):
        self._mesh = mesh
        self._height_direction = height_direction

        self._find_local_maximum()

    def _find_local_maximum(self):
        # create the vertex mask to be returned
        # init zero to all vertex
        self._mask = np.ones(len(self._mesh.vertices), dtype=bool)

        # calculate height for all vertex
        direction_mat = self._height_direction.reshape(-1, 1)
        heights = np.dot(self._mesh.vertices, self._height_direction)
        # get idx (= 0,1,2) with the maximum value in each face
        heights_per_face = heights[self._mesh.faces]
        max_idx = np.argmax(heights_per_face, axis=1)
        # get idx to be set to 1 in mask
        mask_to_get_idx = np.ones_like(self._mesh.faces, dtype=bool)
        mask_to_get_idx[np.arange(self._mesh.faces.shape[0]), max_idx] = 0
        non_max_idx = self._mesh.faces[mask_to_get_idx]

        self._mask[non_max_idx] = 0
