import numpy as np
import trimesh
from AIDR import obb_odometry
from AIDR import find_loacal_maximum
# attach to logger so trimesh messages will be printed to console
# trimesh.util.attach_to_log()

mesh: trimesh.Trimesh = trimesh.load(r'../data/bi_cleft/0282_BIRTH_Maxillary_export.stl')
odom = obb_odometry(mesh, arch_type='U')
occlusal = odom.occlusal
max_finder = find_loacal_maximum.local_height_maximum_finder(mesh, occlusal)
mask = max_finder.mask
max_vertex = mesh.vertices[mask]
p_cloud = trimesh.PointCloud(max_vertex)
p_cloud.vertices_color = [0, 0, 0, 255]
mesh.visual.face_colors = [255, 255, 255, 255]
sc = trimesh.Scene([mesh, p_cloud])
sc.show()

