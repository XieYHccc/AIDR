import os
import numpy as np
import trimesh as tm
from .find_loacal_maximum import local_height_maximum_finder
from .odometry.obb_odometry import obb_odometry
from .partion import curvature_based_Part
import vtkplotlib as vpl


class AIDR:
    _mesh: tm.Trimesh
    _arch_type: str
    _local_maximum_finder: local_height_maximum_finder
    _odometry: obb_odometry
    _h_threshold: float
    _scene: tm.scene
    _partion: curvature_based_Part
    _figure: vpl.figure                       # the figure to plot in
    _peaks: np.ndarray                        # indices of peak points
    _face_colors: np.ndarray                  # shape=(face_number,3), for the mesh object in _figure

    @property
    def partion(self):
        return self._partion

    def plot_orientation(self):
        for (axis, color) in zip(self._odometry.axes, np.eye(3)):
            vpl.quiver(self._mesh.center_mass+self._odometry.occlusal*15, axis, color=color, length=5)

    def plot_local_maximum(self):
        mask = self._local_maximum_finder.mask
        maximum_points = self._mesh.vertices[mask]
        heights = np.inner(maximum_points, self._odometry.occlusal)
        maximum_points = maximum_points[heights > self._h_threshold]
        vpl.quiver((maximum_points+2*self._odometry.occlusal), -self._odometry.occlusal, color='k', width_scale=2, length=2)

    def plot_edge_curvature(self):
        plot = vpl.mesh_plot_with_edge_scalars(self._mesh.vertices[self._mesh.faces],
                                               edge_scalars=self._partion.curvature_per_triangle,
                                               cmap=["r", 'w', "b"])
        plot_range = np.nanstd(self._partion.curvature) * 2
        plot.scalar_range = (-plot_range, plot_range)
        bar = vpl.scalar_bar(plot, "Curvature")
        bar.set_horizontal()
        bar.size = .8, .1
        bar.position = .1, .05
        vpl.show()

    def plot_peak_spread_region(self, peak_idx):
        self._plot_mesh.tri_scalars[self._partion.mask[peak_idx]] = np.random.randint(1, 256, 3)

    def plot_spread_regions(self):
        for peak in self._peaks:
            self.plot_peak_spread_region(peak)

    def show(self):
        self._figure.show()

    def __init__(self, mesh, arch_type, run=True):
        self._init(mesh, arch_type)

        if run:
            self._run()

    def _init(self, mesh, arch_type):
        self._mesh = mesh
        self._arch_type = arch_type
        self._face_colors = np.tile(np.array([[255, 255, 255]]), (len(self._mesh.faces),1))
        self._figure = vpl.figure("Baby dental model")
        self._plot_mesh = vpl.mesh_plot(self._mesh.vertices[self._mesh.faces], tri_scalars=self._face_colors)

    def _run(self):
        self._find_orientation()
        self._find_height_threshold()
        self._find_local_maximum()
        self._partion_alveolus()

    def _find_orientation(self):
        self._odometry = obb_odometry(self._mesh, self._arch_type)

    def _find_height_threshold(self):
        self._h_threshold = np.inner(self._mesh.vertices,
                                     self._odometry.occlusal).max() - 5

        print(f'height threshold is:{self._h_threshold}')

    def _find_local_maximum(self):
        self._local_maximum_finder = local_height_maximum_finder(
            self._mesh, self._odometry.occlusal)

    def _partion_alveolus(self):
        mask = self._local_maximum_finder.mask
        heights = np.inner(self._mesh.vertices[mask], self._odometry.occlusal)
        self._peaks = mask[heights > self._h_threshold]
        print(f'the indices of peaks:{self._peaks}')
        self._partion = curvature_based_Part(self._mesh, self._odometry, self._peaks)
        # self._partion.plot_peak_spread_region(peaks_idx[2])




