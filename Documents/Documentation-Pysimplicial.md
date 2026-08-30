# Official pysimplicial documentation

pysimplicial is a lightweight Python package for working with simplicial complexes in Topological Deep Learning problems, created on foundation of [Open-Closed State-sum Neural Network](https://github.com/kaifczxc-lab/OCSSN)

The current version of the library (0.1.2) has the following set of functions:

* Pachner Moves: move_2_2, move_1_3, move_3_1, move_1_4, move_2_3, move_4_1, move_3_2

* Generators: combinatorial_torus, combinatorial_torus_3D, geometry_bottle_of_klein,geometry_torus

* Data Converters for ML: chain_2D, chain_3D, converter_for_gnn, converter_for_gnn_3D, converter_for_mlp, converter_for_mlp_3D, converter_for_tnn, converter_for_tnn_3D

* Tools for visualization: visualize_triangulation_3D, visualize_triangulation_2D

* Tools for computing euler's characteristics: compute_connected_components_3D, compute_genus_2D

* Experimental tools: state_sum, graph

<div align="center">
  <h1>Pachner Moves</h1>
</div>

More information can be found:

1. [Open-Closed State Sum Neural Network Maths Introduction](https://github.com/kaifczxc-lab/OCSSN/blob/SiritoriProjects/OCSSN-Maths-Introduction.md)

2. [Wikipedia: Pachner Moves](https://en.wikipedia.org/wiki/Pachner_moves) (and from there you can get to the original source, the article by Udo Pachner)

Visualization can be found:



Pachner moves represent a set of local combinatorial operations defined on the simplicial triangulations of piecewise-linear (PL) manifolds, allowing one such triangulation to be transformed into another equivalent one.

These moves consist of **replacing the star of a simplex with the star of the dual simplex** in such a way as to preserve the structure of the manifold, and such that, in dimension n, there are n+1 such moves

Lets talk about type of moves

---

<div align="center">
  <h2>move_2_2(tris)</h2>
</div>


This function implements Pachner Move type 2-2

The 2-2 move is applied to adjacent triangles connected by a common interior edge, forming a quadrilateral. The function replaces the common edge with the opposite diagonal of the quadrilateral, resulting in two new triangles covering the same area
    
Parameters
----------

tris: list of tuples of three ints

* Triangles mesh list

Returns
-------

new_triangles: list of tuple

* tris but with 2-2 Pachner move

tris: list of tuple

* If we couldn't find a candidate for a 2-2 Pachner move (=flip), then we return the original set, that is, we look for an edge that belongs to exactly two triangles (len(tris) == 2), this is the candidate for the flip, otherwise, we return the same figure

    
Examples
--------

>>> Pachner_move_2_2 = move_2_2(octahedron)

>>> print(f"Basic octahedron={octahedron}")

>>> print(f"Pachner_move_2_2 Octahedron={Pachner_move_2_2}")

Basic octahedron=[(0, 1, 2), (0, 2, 3), (0, 3, 4), (0, 4, 1), (5, 2, 1), (5, 3, 2), (5, 4, 3), (5, 1, 4)]

Pachner_move_2_2 Octahedron=[(0, 1, 2), (0, 2, 3), (0, 4, 1), (5, 2, 1), (5, 3, 2), (5, 1, 4), (3, 0, 5), (0, 4, 5)]


---

<div align="center">
  <h2>move_1_3(tris)</h2>
</div>

This function implements Pachner Move type 1-3

Divides the triangle into three smaller ones by connecting them with one common vertex (that is, to determine the correctness of the move 1-3, we must ensure that there is a new vertex and it is connected to the other 3)
    
Parameters
----------

tris: list of tuples of three ints

* Triangles mesh list

Returns
-------

n_triangles: list of tuple

* New triangles mesh list with move 1-3

Examples
--------

>>> Pachner_move_1_3 = PySimplicial.utils.move_1_3(octahedron)

>>> print(f"Basic octahedron={octahedron}")

>>> print(f"Octahedron with move 3-1={Pachner_move_1_3}")

Basic octahedron=[(0, 1, 2), (0, 2, 3), (0, 3, 4), (0, 4, 1), (5, 2, 1), (5, 3, 2), (5, 4, 3), (5, 1, 4)]

Octahedron with move 3-1=[(0, 1, 2), (0, 2, 3), (0, 3, 4), (0, 4, 1), (5, 2, 1), (5, 3, 2), (5, 4, 3), (5, 1, 6), (1, 4, 6), (5, 4, 6)]


---

<div align="center">
  <h2>move_3_1(tris)</h2>
</div>


This function implements Pachner Move type 3-1

The move 3-1 is the inverse of 1-3, removing an interior vertex of degree 3, surrounded by three triangles with no other elements attached to their faces, and combines them into a single triangle

Parameters
----------

tris: list of tuples of three ints

* Triangles mesh list

Returns
-------

new_triangles: list of tuple

* Same triangles mesh list but with move 3-1

Examples
--------

>>> Pachner_move_3_1 = PySimplicial.utils.move_3_1(Pachner_move_1_3)

>>> print(f"Basic octahedron={octahedron}")

>>> print(f"Octahedron with move 3-1={Pachner_move_3_1}")

Basic octahedron=[(0, 1, 2), (0, 2, 3), (0, 3, 4), (0, 4, 1), (5, 2, 1), (5, 3, 2), (5, 4, 3), (5, 1, 4)]

Octahedron with move 3-1=[(0, 1, 2), (0, 2, 3), (0, 3, 4), (0, 4, 1), (5, 2, 1), (5, 3, 2), (5, 4, 3), (5, 1, 4)]
    

---

<div align="center">
  <h2>move_1_4(tetrahedron)</h2>
</div>


This function implements Pachner Move type 1-4

The Pachner move 1-4 divides one tetrahedron into four smaller tetrahedrons by introducing a new internal vertex. The boundary remains unchanged, but three edges and one vertex are added to the original tetrahedron

Parameters
----------

tetrahedron: list of tuples of four ints

* Tetrahedrons mesh list

Returns
-------

n_triangles: list of tuple

* Same tetrahedrons mesh list but with move 1-4

Examples
--------

>>> one_tetrahedron = [(0, 1, 2, 3)]

>>> Pachner_move_1_4 = PySimplicial.utils.move_1_4(one_tetrahedron)

>>> print(f"tetrahedron={one_tetrahedron}")

>>> print(f"same tetrahedron but with move 1-4={Pachner_move_1_4}")

tetrahedron=[(0, 1, 2, 3)]

same tetrahedron but with move 1-4=[(0, 1, 2, 4), (0, 1, 3, 4), (0, 2, 3, 4), (1, 2, 3, 4)]


---

<div align="center">
  <h2>move_4_1(tetrahedron)</h2>
</div>

This function implements Pachner Move type 4-1

Move 4-1 is the inverse of 1-4 and removes an internal vertex that is a common vertex of exactly four tetrahedra with no other internal simplices, collapsing them back into a single tetrahedron, thereby reducing the number of tetrahedra by three, removing one vertex and three edges

Parameters
----------

tetrahedron: list of tuples of four ints

* Tetrahedrons mesh list

Returns
-------

new_triangles: list of tuple

* Same triangles mesh list but with move 4-1 (This move will work for you with 100% probability after using 1-4)

Examples
--------

>>> one_tetrahedron = [(0, 1, 2, 3)]

>>> Pachner_move_1_4 = PySimplicial.utils.move_1_4(one_tetrahedron)

>>> Pachner_move_4_1 = PySimplicial.utils.move_4_1(Pachner_move_1_4)

>>> print(f"Pachner_move_1_4={Pachner_move_1_4}")

>>> print(f"Pachner_move_4_1={Pachner_move_4_1}")

Pachner_move_1_4=[(0, 1, 2, 4), (0, 1, 3, 4), (0, 2, 3, 4), (1, 2, 3, 4)]

Pachner_move_4_1=[(0, 1, 2, 3)]


---

<div align="center">
  <h2>move_2_3(tetrahedron)</h2>
</div>


This function implements Pachner Move type 2-3

Move 2-3 increases the number of tetrahedra by one and adds one new edge, preserving the number of vertices and locally modifying the faces

Parameters
----------

tetrahedron: list of tuples of four ints

* Tetrahedrons mesh list

Returns
-------
new_tetrahedrons: list of tuple

* if there are common faces for two tetrahedrons

tetrahedron: list of tuple

* if there are no common faces for two tetrahedrons

Examples:
--------

>>> tetrahedron = [(0, 1, 2, 3),(0, 1, 2, 4)] # Visualize original figure

>>> Pachner_move_2_3 = PySimplicial.utils.move_2_3(tetrahedron) # visualize the same figure but with Pachner Move 2-3 triangulation

>>> print(f"basic tetrahedron={tetrahedron}")

>>> print(f"same tetrahedron but with move 2-3={Pachner_move_2_3}")

basic tetrahedron=[(0, 1, 2, 3), (0, 1, 2, 4)]

same tetrahedron but with move 2-3=[(0, 1, 3, 4), (1, 2, 3, 4), (0, 2, 3, 4)]

---

<div align="center">
  <h2>move_3_1(tris)</h2>
</div>


This function implements Pachner Move type 3-1

The 3-2 move is the inverse of the 2-3 move, replacing three tetrahedra meeting on an internal edge between two tetrahedra sharing a face, reducing the number of tetrahedra by one, and removing one edge without changing vertices
    
Parameters
----------

tetrahedron: list of tuples of four ints

* Tetrahedrons mesh list

Returns
-------

result: list of tuple of four ints

* If there's a common edge that belongs to exactly three tetrahedra

tetrahedron: list of tuple of four ints

* If there is no common edge that belongs to exactly three tetrahedra

Examples
--------

>>> tetrahedron = [(0, 1, 2, 3),(0, 1, 2, 4)] # Visualize original figure

>>> Pachner_move_2_3 = PySimplicial.utils.move_2_3(tetrahedron) # visualize the same figure but with Pachner Move 2-3 triangulation

>>> Pachner_move_3_2 = PySimplicial.utils.move_3_2(Pachner_move_2_3) # return this modify to basic form

>>> print(f"basic tetrahedron={tetrahedron}")

>>> print(f"same tetrahedron but with move 2-3={Pachner_move_2_3}")

>>> print(f"inverse, move 3-2={Pachner_move_3_2}")

basic tetrahedron=[(0, 1, 2, 3), (0, 1, 2, 4)]

same tetrahedron but with move 2-3=[(0, 1, 3, 4), (1, 2, 3, 4), (0, 2, 3, 4)]

inverse, move 3-2=[(0, 1, 2, 3), (0, 1, 2, 4)]


