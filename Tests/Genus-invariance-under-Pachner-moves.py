import PySimplicial.utils as ps
import random

rng = random.Random(1)

torus = ps.combinatorial_torus(10,10)

genus_before = ps.euler_characteristics(torus)


K = 1000

for p in range(K):
    chance = rng.random()
    if chance < 0.33:
        new = ps.move_1_3(torus)
    elif chance < 0.66:
        new = ps.move_2_2(torus)
    else:
        new = ps.move_3_1(torus)
    if new is not None:
        torus = new

genus_after = ps.euler_characteristics(torus)

assert genus_after == genus_before

# -------------------------

octahedron = [(0,1,2), (0,2,3), (0,3,4), (0,4,1),(5,2,1), (5,3,2), (5,4,3), (5,1,4)]

genus_before_octahedron = ps.euler_characteristics(octahedron)

for p in range(K):
    chance = rng.random()
    if chance < 0.33:
        new = ps.move_1_3(octahedron)
    elif chance < 0.66:
        new = ps.move_2_2(octahedron)
    else:
        new = ps.move_3_1(octahedron)
    if new is not None:
        octahedron = new
genus_after_octahedron = ps.euler_characteristics(octahedron)

assert genus_after_octahedron == genus_before_octahedron
