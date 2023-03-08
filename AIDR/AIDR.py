import os
import numpy as np
import trimesh as tm
from .find_loacal_maximum import local_height_maximum_finder
from .odometry.obb_odometry import obb_odometry
from .partion import curvature_based_Part


class AIDR:
    _mesh: tm.Trimesh
    _arch_type: str
    _local_maximum_finder: local_height_maximum_finder
    _odometry: obb_odometry
    _h_threshold: float

    def plot_local_maximum(self):
        mask = self._local_maximum_finder.mask
        maximum_points = self._mesh.vertices[mask]
        heights = np.inner(maximum_points, self._odometry.occlusal)
        maximum_points = maximum_points[heights > self._h_threshold]
        p_cloud = tm.PointCloud(maximum_points)
        p_cloud.vertices_color = [0, 0, 0, 255]
        self._mesh.visual.face_colors = [255, 255, 255, 255]
        sc = tm.Scene([self._mesh, p_cloud])
        sc.show()

    def plot_peak_spread_region(self, peak_idx):
        self._partion.plot_peak_spread_region(peak_idx)

    def plot_spread_regions(self):
        self._partion.plot_spread_regions()

    def __init__(self, mesh, arch_type, run=True):
        self._init(mesh, arch_type)

        if run:
            self._run()

    def _init(self, mesh, arch_type):
        self._mesh = mesh
        self._arch_type = arch_type

    def _run(self):
        self._find_orientation()
        self._find_height_threshold()
        self._find_local_maximum()
        self._partion_alveolus()

    def _find_orientation(self):
        self._odometry = obb_odometry(self._mesh, self._arch_type)

    def _find_height_threshold(self):
        self._h_threshold = np.inner(self._mesh.vertices,
                                     self._odometry.occlusal).max() - 4

        print(f'height threshold is:{self._h_threshold}')

    def _find_local_maximum(self):
        self._local_maximum_finder = local_height_maximum_finder(
            self._mesh, self._odometry.occlusal)

    def _partion_alveolus(self):
        mask = self._local_maximum_finder.mask
        maximum_points = self._mesh.vertices[mask]
        heights = np.inner(maximum_points, self._odometry.occlusal)
        peaks_idx = mask[heights > self._h_threshold]
        print(f'the indices of peaks:{peaks_idx}')
        self._partion = curvature_based_Part(self._mesh, self._odometry, peaks_idx)
        # self._partion.plot_peak_spread_region(peaks_idx[2])




