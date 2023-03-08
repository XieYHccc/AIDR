from AIDR.AIDR import AIDR
import trimesh

mesh: trimesh.Trimesh = trimesh.load(r'../data/bi_cleft/0101_Birth_Maxillary_export.stl')

aidr = AIDR(mesh, arch_type='U')

aidr.plot_local_maximum()
aidr.plot_spread_regions()
aidr.show()
