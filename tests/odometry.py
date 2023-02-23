import numpy as np
import trimesh
from AIDR import obb_odometry

# attach to logger so trimesh messages will be printed to console
# trimesh.util.attach_to_log()

mesh = trimesh.load(r'../data/bi_cleft/0282_BIRTH_Maxillary_export.stl')
odom = obb_odometry(mesh, arch_type='U')
center = mesh.center_mass
odom_axes = odom.axes
# transform_mat = np.zeros((4, 4))
# transform_mat[0:3, 0] = odom_axes[0]
# transform_mat[0:3, 1] = odom_axes[1]
# transform_mat[0:3, 2] = odom_axes[2]
# transform_mat[0:3, 3] = center
# tri_axis = trimesh.creation.axis(origin_size=2, transform=transform_mat)
# (tri_axis+mesh).show()
#odom.plot_project_to_YZ_plane()

