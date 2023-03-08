import abc
import time
import numpy as np
import collections
import queue
import heapq
import trimesh
from .curvature import edge_based_curvature
import matplotlib.pyplot as plt
from .odometry.obb_odometry import obb_odometry
from .topology import face_neighbors


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
    _peaks_idx: np.ndarray  # the indices of peaks
    _peak_masks: {}
    _peak_costs: {}
    _peak_tri2tri_costs: np.ndarray

    _MAX_COST = 1
    _MAX_SPREAD_WIDTH = 8
    _MAX_SPREAD_HEIGHT = 5

    @property
    def curvature(self):
        return self._curvature

    @property
    def curvature_per_triangle(self):
        return self._curvature_per_triangle

    @property
    def mask(self):
        return self._peak_masks

    def plot_curvature_hist(self):
        plt.hist(self._curvature, bins=30)
        plt.show()

    def plot_peak_spread_region(self, peak_idx):
        self._mesh.visual.face_colors[self._peak_masks[peak_idx]] = [255, 0, 0, 255]

    def plot_spread_regions(self):
        mask = np.array([value for value in self._peak_masks.values()])
        mask = np.bitwise_or.reduce(mask, axis=0)
        self._mesh.visual.face_colors[mask] = [255, 0, 0, 255]

    def __init__(self, mesh, odometry, peaks_idx):
        self._mesh = mesh
        self._odom = odometry
        self._peaks_idx = peaks_idx
        self._faces_adj = face_neighbors(self._mesh)
        self._peak_masks = {}
        self._peak_costs = {}

        t0 = time.time()
        self._run()
        run_time = time.time() - t0
        print(run_time)

    def _run(self):
        self._calculate_curvature()
        self._spread_from_peaks()

    def _calculate_curvature(self):
        self._curvature, self._curvature_per_triangle = \
            edge_based_curvature(self._mesh, get_map=True)

    def _spread_from_peaks(self):

        tri2tri_costs = -self._curvature_per_triangle.clip(max=0)

        # self._spread_from_peak(self._peaks_idx[2], tri2tri_costs)
        for peak in self._peaks_idx:
            self._spread_from_peak(peak, tri2tri_costs)

    def _spread_from_peak(self, peak_idx, costs):  # core region growing algorithm
        peak_triangles = np.where(self._mesh.faces == peak_idx)[0]

        # init accumulative costs
        accumulative_cost = np.ones(self._mesh.faces.shape[0]) * self._MAX_COST
        accumulative_cost[peak_triangles] = 0.0

        # to make sure the region won't spread too widely,
        # restrict region within specific width and height
        center2peak = self._mesh.triangles_center - self._mesh.vertices[peak_idx]
        width_array = abs(np.inner(center2peak, self._odom.right))
        height_array = abs(np.inner(center2peak, self._odom.occlusal))

        # init queue
        tmp_queue = queue.Queue()
        faces_init = self._faces_adj[peak_triangles].reshape(-1)
        [tmp_queue.put(face) for face in faces_init]

        # spread from triangles containing peak
        while not tmp_queue.empty():
            face = tmp_queue.get()

            # make sure the region won't spread too widely
            if width_array[face] > self._MAX_SPREAD_WIDTH or height_array[face] > self._MAX_SPREAD_HEIGHT:
                continue

            face_adj = self._faces_adj[face]
            cost_adj = accumulative_cost[face_adj]
            edges_cost_adj = costs[face]
            tmp = (cost_adj + edges_cost_adj).min()

            if tmp < accumulative_cost[face]:
                accumulative_cost[face] = tmp
                [tmp_queue.put(adj) for adj in face_adj]

        self._peak_costs[peak_idx] = accumulative_cost
        self._peak_masks[peak_idx] = accumulative_cost < self._MAX_COST

    # def _spread_from_peak(self, peak_idx, costs):  # core region growing algorithm
    #     peak_triangles = np.where(self._mesh.faces == peak_idx)[0]
    #
    #     # init accumulative costs
    #     accumulative_cost = np.ones(self._mesh.faces.shape[0]) * self._MAX_COST
    #     accumulative_cost[peak_triangles] = 0.0
    #
    #     # init queue
    #     faces_init = self._faces_adj[peak_triangles].reshape(-1)
    #     tmp_queue = queue.PriorityQueue()
    #     [tmp_queue.put((accumulative_cost[face], face)) for face in faces_init]
    #
    #     # spread from triangles containing peak
    #     while not tmp_queue.empty():
    #         face = tmp_queue.get()[1]
    #
    #         # make sure the region won't spread too widely
    #         face_center = self._mesh.triangles_center[face]
    #         width = abs(np.inner(self._odom.right, face_center - self._mesh.vertices[peak_idx]))
    #         height = abs(np.inner(self._odom.occlusal, face_center - self._mesh.vertices[peak_idx]))
    #         if width > self._MAX_SPREAD_WIDTH or height > self._MAX_SPREAD_HEIGHT:
    #             continue
    #
    #         face_adj = self._faces_adj[face]
    #         cost_adj = accumulative_cost[face_adj]
    #         edges_cost_adj = costs[face]
    #         tmp = (cost_adj + edges_cost_adj).min()
    #
    #         if tmp < accumulative_cost[face]:
    #             [tmp_queue.put((accumulative_cost[adj], adj)) for adj in face_adj]
    #             accumulative_cost[face] = tmp
    #
    #     self._peak_costs[peak_idx] = accumulative_cost
    #     self._peak_masks[peak_idx] = accumulative_cost < self._MAX_COST
