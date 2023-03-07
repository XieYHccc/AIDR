import abc
import numpy as np
import collections
import trimesh
from .curvature import edge_based_curvature
import matplotlib.pyplot as plt
from AIDR.odometry.obb_odometry import obb_odometry


class basePart(abc.ABC):

    @property
    @abc.abstractmethod
    def part_mask(self):
        pass


class curvature_based_Part:

    _mesh: trimesh.Trimesh
    _odom: obb_odometry
    _curvature: np.ndarray
    _curvature_per_triangle: np.ndarray
    _peaks_idx: np.ndarray                          # the indices of peaks
    _peak_masks: {}
    _peak_tri2tri_costs: np.ndarray

    @property
    def curvature(self):
        return self._curvature

    @property
    def curvature_per_triangle(self):
        return self._curvature_per_triangle

    @property
    def mask(self):
        return self._part_mask

    def plot_curvature_hist(self):
        plt.hist(self._curvature, bins=30)
        plt.show()

    def __init__(self, mesh, odometry, peaks_idx):
        self._mesh = mesh
        self._odom = odometry
        self._peaks_idx = peaks_idx

        self._run()

    def _run(self):
        self._calculate_curvature()
        self._spread_from_peaks()

    def _calculate_curvature(self):
        self._curvature, self._curvature_per_triangle =\
            edge_based_curvature(self._mesh, get_map=True)

    def _spread_from_peaks(self):                            # core region growing algorithm
        tri2tri_costs = -self._curvature_per_triangle.clip(max=0)
        max_cost = 3.5
        peak_triangles = {i: np.where(self._mesh.faces == i)[0]
                          for i in self._peaks_idx}
        print(peak_triangles)













