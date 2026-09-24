import PySimplicial.utils

import numpy as np
import matplotlib.pyplot as plt

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
PySimplicial.utils.visualize_triangulation_2D(one_tetrahedron)

print("Visualization 6 : applied Pachner movement 2-3 on basic tetrahedron")
tris_3D_2_3 = PySimplicial.utils.move_2_3(tetrahedron)
PySimplicial.utils.visualize_triangulation_2D(tris_3D_2_3)

print("Visualization 7 : applied Pachner movement 3-2 on tris_3D_2_3 (inverse, we should back to basic tetrahedron)")
tris_3D_3_2 = PySimplicial.utils.move_3_2(tris_3D_2_3)
PySimplicial.utils.visualize_triangulation_2D(tris_3D_3_2)

print("Visualization 8 : applied Pachner movement 1-4 on basic tetrahedron")
tris_3D_1_4 = PySimplicial.utils.move_1_4(one_tetrahedron)
PySimplicial.utils.visualize_triangulation_2D(tris_3D_1_4)

print("Visualization 9 : applied Pachner movement 4-1 on tris_3D_1_4 (inverse, we should back to basic tetrahedron)")
tris_3D_4_1 = PySimplicial.utils.move_4_1(tris_3D_1_4)
PySimplicial.utils.visualize_triangulation_2D(tris_3D_4_1)

# --------------

# Torus generators part
# ---------------------

combinatorial_torus_2D = PySimplicial.utils.combinatorial_torus(3,3)
print("combinatorial torus 2d")
print(combinatorial_torus_2D)

geometry_torus_3D = PySimplicial.utils.geometry_torus(3,3,2,1)
print("geometry torus 3d")
print(geometry_torus_3D)

combinatorial_torus_3D = PySimplicial.utils.combinatorial_torus_3D(2,2,2)
print("combinatorial torus 3d")
print(combinatorial_torus_3D)

u, v = np.meshgrid(np.linspace(0, 2*np.pi, 5),np.linspace(0, 2*np.pi, 5))
bottle_of_klein = PySimplicial.utils.geometry_bottle_of_klein(u, v)
print("bottle of klein")
print(bottle_of_klein)

print("Bottle of klein visualization")
u, v = np.meshgrid(np.linspace(0, 2*np.pi, 100),np.linspace(0, 2*np.pi, 100))
x, y, z = PySimplicial.utils.geometry_bottle_of_klein(u, v)
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.plot_surface(x, y, z)
plt.show()

# ---------------------

# Converters Part
# --------------

octahedron_for_relabel = [(10, 50, 15),(10, 15, 25),(10, 25, 40),(10, 40, 50),(90, 15, 50),(90, 25, 15),(90, 40, 25),(90, 50, 40)]
tetrahedron_for_relabel = [(100, 8282, 327, 21828),(0,8282, 327, 21828),(0,100, 327, 21828),(0,100, 8282, 21828),(0,100, 8282, 327)]

converter = PySimplicial.utils.Converters()

relabeled = converter.relabel(octahedron_for_relabel)

A, L = converter.to_gnn(relabeled)
print(f"(a,b,c): A={A}, L={L}")

A_norm = converter.to_tnn(relabeled, N=6)
print(f"(a,b,c): A_norm={A_norm}")

features = converter.to_mlp(relabeled, return_chi=True)
print(f"(a,b,c): features={features}")

relabeled_ = converter.relabel(tetrahedron_for_relabel)

A_, L_ = converter.to_gnn(relabeled_)
print(f"(a,b,c,d): A_={A_}, L_={L}")

A_norm_ = converter.to_tnn(relabeled_, N=5)
print(f"(a,b,c,d): A_norm_={A_norm_}")

features_ = converter.to_mlp(relabeled_)
print(f"(a,b,c,d): features_={features_}")
# --------------

# -------------------------------------------------

octahedron = [(0,1,2), (0,2,3), (0,3,4), (0,4,1),(5,2,1), (5,3,2), (5,4,3), (5,1,4)]
print(f"Euler characteristics for mesh in form of (a,b,c) = {PySimplicial.utils.euler_characteristics(octahedron)}")

tetrahedron = [(0, 1, 2, 3),(0, 1, 2, 4)]
print(f"Euler characteristics for mesh in form of (a,b,c) = {PySimplicial.utils.euler_characteristics(tetrahedron)}")

# State sum
# -------------------------------------------------

print("state sum")
C = np.array([[[1.,0.],[0.,1.]],[[0.,1.],[1.,0.]]])
b_inv = np.array([[1.,0.],[0.,1.]])
before = PySimplicial.utils.state_sum(C, b_inv, [(0,1,2),(3,4,5)], [(0,3),(1,4),(2,5)], ())
after = PySimplicial.utils.state_sum(C, b_inv, [(0,1,2),(3,4,5)], [(0,4),(1,3),(2,5)], ())
print(before, after, np.isclose(before, after))
