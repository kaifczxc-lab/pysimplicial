import PySimplicial.utils

octahedron = [(0,1,2), (0,2,3), (0,3,4), (0,4,1),(5,2,1), (5,3,2), (5,4,3), (5,1,4)]
tetrahedron = [(0, 1, 2, 3),(0, 1, 2, 4)]

print("Octahedron basic without custom pos")
PySimplicial.utils.visualize_triangulation_3D(octahedron, enable_random_face_colors=False)


print("Octahedron with move 1-3")
octahedron_with_move_1_3 = PySimplicial.utils.move_1_3(octahedron)
visualize_octahedron_move_1_3 = PySimplicial.utils.visualize_triangulation_3D(octahedron_with_move_1_3, enable_random_face_colors=False)
print(visualize_octahedron_move_1_3)


pos = {0: (1, 0, 0),1: (-1, 0, 0),2: (0, 1, 0),3: (0, -1, 0),4: (0, 0, 1),5: (0, 0, -1)}

print("Octahedron with custom pos")
octahedron = [(0,1,2), (0,2,3), (0,3,4), (0,4,1), (5,2,1), (5,3,2), (5,4,3), (5,1,4)]
PySimplicial.utils.visualize_triangulation_3D(octahedron, custom_pos=pos, enable_random_face_colors=True)

print("Basic tetrahedron")
PySimplicial.utils.visualize_triangulation_3D(tetrahedron, enable_random_face_colors=False)

print("tetrahedron with 1-4 move")
new_tetrahedron_1_4 = PySimplicial.utils.move_1_4(tetrahedron)
visualize_tetrahedron_1_4 = PySimplicial.utils.visualize_triangulation_3D(new_tetrahedron_1_4, enable_random_face_colors=False)
print(visualize_tetrahedron_1_4)