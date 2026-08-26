import PySimplicial.utils
import numpy as np

octahedron = [(0,1,2), (0,2,3), (0,3,4), (0,4,1),(5,2,1), (5,3,2), (5,4,3), (5,1,4)]
tetrahedron = [(0, 1, 2, 3),(0, 1, 2, 4)]
one_tetrahedron = [(0, 1, 2, 3)]


# Visualize part
# --------------

print("Visualization 1 : basic octahedron")
tris = octahedron
PySimplicial.utils.visualize_triangulation_2D(tris)

print("Visualization 2 : applied Pachner movement 1-3 on basic octahedron ")
tris_2D_1_3 = PySimplicial.utils.move_1_3(tris)
PySimplicial.utils.visualize_triangulation_2D(tris_2D_1_3)

print("Visualization 3 : applied Pachner movement 3-1 on tris_2D_1_3 (inverse, we should back to basic octahedron)")
tris_2D_3_1 = PySimplicial.utils.move_3_1(tris_2D_1_3)
PySimplicial.utils.visualize_triangulation_2D(tris_2D_3_1)

print("Visualization 4 : applied Pachner movement 2-2 on basic octahedron")
tris_2D_2_2 = PySimplicial.utils.move_2_2(tris)
PySimplicial.utils.visualize_triangulation_2D(tris_2D_2_2)

print("Visualization 5 : basic tetrahedron")
PySimplicial.utils.visualize_triangulation_3D(one_tetrahedron)

print("Visualization 6 : applied Pachner movement 2-3 on basic tetrahedron")
tris_3D_2_3 = PySimplicial.utils.move_2_3(tetrahedron)
PySimplicial.utils.visualize_triangulation_3D(tris_3D_2_3)

print("Visualization 7 : applied Pachner movement 3-2 on tris_3D_2_3 (inverse, we should back to basic tetrahedron)")
tris_3D_3_2 = PySimplicial.utils.move_3_2(tris_3D_2_3)
PySimplicial.utils.visualize_triangulation_3D(tris_3D_3_2)

print("Visualization 8 : applied Pachner movement 1-4 on basic tetrahedron")
tris_3D_1_4 = PySimplicial.utils.move_1_4(one_tetrahedron)
PySimplicial.utils.visualize_triangulation_3D(tris_3D_1_4)

print("Visualization 9 : applied Pachner movement 4-1 on tris_3D_1_4 (inverse, we should back to basic tetrahedron)")
tris_3D_4_1 = PySimplicial.utils.move_4_1(tris_3D_1_4)
PySimplicial.utils.visualize_triangulation_3D(tris_3D_4_1)


# --------------

# Torus generators part
# ---------------------

combinatorial_torus_2D = PySimplicial.utils.combinatorial_torus(10,10)
print("combinatorial torus 2d")
print(combinatorial_torus_2D)

geometry_torus_3D = PySimplicial.utils.geometry_torus(3,3,2,1)
print("geometry torus 3d")
print(geometry_torus_3D)

combinatorial_torus_3D = PySimplicial.utils.combinatorial_torus_3D(3,3,3)
print("combinatorial torus 3d")
print(combinatorial_torus_3D)

u, v = np.meshgrid(np.linspace(0, 2*np.pi, 30),np.linspace(0, 2*np.pi, 30))
bottle_of_klein = PySimplicial.utils.geometry_bottle_of_klein(u, v)
print("bottle of klein")
print(bottle_of_klein)

# ---------------------

# Converters Part
# --------------

octahedron_for_relabel = [(10, 50, 15),(10, 15, 25),(10, 25, 40),(10, 40, 50),(90, 15, 50),(90, 25, 15),(90, 40, 25),(90, 50, 40)]
relabel = PySimplicial.utils.relabel(octahedron_for_relabel)
print("RELABEL")
print(relabel)

converter_GNN_2D = PySimplicial.utils.converter_for_gnn(relabel)
print("CONVERTER GNN")
print(converter_GNN_2D)

converter_TNN_2D = PySimplicial.utils.converter_for_tnn(relabel, 6)
print("CONVERTER TNN")
print(converter_TNN_2D)

converter_MLP_2D = PySimplicial.utils.converter_for_mlp(relabel, return_g=True)
print("CONVERTED MLP")
print(converter_MLP_2D)

tetrahedron_for_relabel = [(100, 8282, 327, 21828),(0,8282, 327, 21828),(0,100, 327, 21828),(0,100, 8282, 21828),(0,100, 8282, 327)]
relabel_3D = PySimplicial.utils.relabel_3D(tetrahedron_for_relabel)
print("RELABEL 3D")
print(relabel_3D)

converter_GNN_3D = PySimplicial.utils.converter_for_gnn_3D(relabel_3D)
print("CONVERTER GNN 3D")
print(converter_GNN_3D)

converter_TNN_3D = PySimplicial.utils.converter_for_tnn_3D(relabel_3D, 6)
print("CONVERTER TNN 3D")
print(converter_TNN_3D)

converter_MLP_3D = PySimplicial.utils.converter_for_mlp_3D(relabel_3D, return_x=True)
print("CONVERTED MLP 3D")
print(converter_MLP_3D)



# --------------

# Computing genus and connected components functions
# -------------------------------------------------

genus = PySimplicial.utils.compute_genus_2D(octahedron)
print(f"compute_genus_2D result is: {genus}")

connected_components_3D = PySimplicial.utils.compute_connected_components_3D(tetrahedron)
print(f"compute_connected_components_3D result is: {connected_components_3D}")

# -------------------------------------------------



