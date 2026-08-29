import PySimplicial.utils as ps
import random

torus = ps.combinatorial_torus(10,10)

genus_before = ps.compute_genus_2D(torus)
print(genus_before)

"""
1
"""

K = 100

for p in range(K):
    chance = random.random()
    if chance < 0.33:
        ps.move_1_3(torus)
    elif chance < 0.66:
        ps.move_2_2(torus)
    else:
        ps.move_3_1(torus)

genus_after = ps.compute_genus_2D(torus)
print(genus_after)

"""
1
"""


octahedron = [(0,1,2), (0,2,3), (0,3,4), (0,4,1),(5,2,1), (5,3,2), (5,4,3), (5,1,4)]

genus_before_octahedron = ps.compute_genus_2D(octahedron)
print(genus_before_octahedron)

"""
0
"""

for p in range(K):
    chance = random.random()
    if chance < 0.33:
        ps.move_1_3(octahedron)
    elif chance < 0.66:
        ps.move_2_2(octahedron)
    else:
        ps.move_3_1(octahedron)

genus_after_octahedron = ps.compute_genus_2D(octahedron)
print(genus_after_octahedron)

"""
0
"""