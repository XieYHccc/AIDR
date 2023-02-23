# -*- coding: utf-8 -*-
"""
"""

from typing import Tuple

import numpy as np
import trimesh
from trimesh.bounds import oriented_bounds
from trimesh import Trimesh
from trimesh.util import unitize
from AIDR.transform import base_transform
import matplotlib.pyplot as plt


class obb_odometry:

    """Find the position and orientation of any dental model (:arxiv:`3.1`).

    Orientation is described with unit-vectors. The following directions are
    available as attributes.

    +-------------------+------------------------------------------------------+
    | Attribute         | Description                                          |
    +===================+======================================================+
    | :attr:`right`     | Both from the patient's perspective.                 |
    +-------------------+                                                      |
    | :attr:`forwards`  |                                                      |
    +-------------------+------------------------------------------------------+
    | :attr:`up`        | To the roof irregardless of                          |
    |                   | whether the model is maxillary of mandibular.        |
    +-------------------+------------------------------------------------------+
    | :attr:`occlusal`  | Alias for the direction of the teeth. Up if it is    |
    |                   | a lower jaw or down if it is an upper jaw.           |
    +-------------------+------------------------------------------------------+

    Position is described with the model's center of mass which is the mean
    of all the mesh's vertices (which isn't much use in practice).

    Odometry is a fancy collective term, borrowed from robotics meaning
    position and orientation.
    """

    names: Tuple[str, str, str] = ("right", "forwards", "up")
    """The names of the axes given by :attr:`axes`."""

    _eX: np.ndarray
    _eY: np.ndarray
    _eZ: np.ndarray
    _arch_type: str
    _mesh: trimesh.Trimesh

    @property
    def right(self):
        return self._eX

    @property
    def forwards(self):
        return self._eY

    @property
    def up(self):
        return self._eZ

    @right.setter
    def right(self, x):
        self._eX = x

    @forwards.setter
    def forwards(self, x):
        self._eY = x

    @up.setter
    def up(self, x):
        self._eZ = x

    @property
    def occlusal(self):
        return self._eZ if self._arch_type == 'L' else -self._eZ

    @occlusal.setter
    def occlusal(self, x):
        self._eZ = x * (1 if self._arch_type == "L" else -1)

    @property
    def axes(self) -> np.ndarray:
        """The core unit-vectors listed in :attr:`names` as rows of a
        3x3 matrix.

        This rotation matrix may be used to normalise and unnormalise a set of
        points.
        """
        return np.array([getattr(self, x)for x in self.names])

    def plot_project_to_YZ_plane(self):
        new_coordinates = base_transform(self._mesh.triangles_center-self._mesh.center_mass
                                         , self.axes.T)
        y = new_coordinates[:, 1]
        z = new_coordinates[:, 2]
        if self._arch_type == 'U':
            z = -z

        plt.scatter(y, z, c='midnightblue', marker='.', s=0.3)
        plt.show()

    def __init__(self, mesh: Trimesh, arch_type=None):
        self._mesh = mesh
        self._arch_type = arch_type
        self._run()

    def _run(self):
        """Run all steps.
        I have written each function in the order they get used, so reading
        this process should just be a case of scrolling down through this
        class
        """
        self._apply_obb()
        self._check_eZ_sign()
        self._check_eY_sign()
        self._check_eX_sign()

    def _apply_obb(self):
        self._eZ, self._eY, self._eX = oriented_bounds(self._mesh)[0][:3, :3]

    def _check_eZ_sign(self):
        """ check/corrct the sign of the vertical axis

        The triangle density is much higher on the occlusal surface so a mean
        of mesh.face_normals could give a decent approximation of occlusal
        """
        # Get an approximate occlusal from the mesh's face normals.
        self._mesh_occlusal = unitize([i.sum() for i in self._mesh.face_normals.T])

        # compare it with OBB's occlusal
        agreement = np.dot(self._mesh_occlusal, self.occlusal)

        self._eZ *= np.sign(agreement)  # swap sign if necessary

    def _check_eY_sign(self):
        """Check/correct the sign of the forwards/backwards axis.

        Fit a weighted quadratic curve to the horizontal components of every
        mesh polygons' center. This curve will approximate the jaw line. If
        the sign is correct, curve should be ⋂ shaped (negative x² coefficient).
        If it is ⋃ shaped then the y-axis needs flipping.

        Note that the fit is quite poor and shouldn't be used for anything
        precise.
        """
        # Extract the horizontal components, removing the center of mass
        x, y = (np.dot((self._mesh.triangles_center - self._mesh.center_mass), e)
                for e in (self._eX, self._eY))

        # Prioritise the more occlusal points
        weights = np.dot(self._mesh.triangles_center, self.occlusal)
        # Prioritise non-occlusal facing triangles.
        # This is supposed to capture the labial and lingual vertical surfaces.
        crosses = np.cross(self._mesh.face_normals, self.occlusal)
        weights *= np.dot(crosses ** 2, [1]*crosses.shape[1])

        weights -= np.min(weights)
        weights = weights**5

        # Fit a quadratic curve to the points with a weighted fitting.
        poly = np.polynomial.Polynomial.fit(x, y, 2, w=weights)

        # If x² coefficient is positive:
        if poly.convert().coef[2] > 0:
            # Flip eY
            self._eY = -self._eY

    def _check_eX_sign(self):
        """Finally eX is just determined so as not to mirror the mesh. This must
        be done after checking eZ and eY because it uses them."""

        # If rotation matrix mirrors then reverse eX
        print(np.linalg.det(self.axes))
        self._eX *= np.sign(np.linalg.det(self.axes))





