from AIDR.AIDR import AIDR
import trimesh

mesh: trimesh.Trimesh = trimesh.load(r'../data/r_cleft/0106_Birth_Maxillary_export.stl')

aidr = AIDR(mesh, arch_type='U')

aidr.plot_local_maximum()
# aidr.partion.plot_spread_regions()
aidr.partion.plot_group_regions()
aidr.show()
