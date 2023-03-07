import AIDR.partion as part
import trimesh

mesh: trimesh.Trimesh = trimesh.load(r'../data/bi_cleft'
                                     r'/0101_Birth_Maxillary_export.stl')
peaks_idx = [3, 71, 197, 5900, 12391, 12606, 12821, 20763, 26534, 34374,
             34936, 39655, 39962, 40327, 42202, 44236, 46089]
partion = part.curvature_based_Part(mesh, peaks_idx=peaks_idx)


