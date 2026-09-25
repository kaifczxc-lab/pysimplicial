# Official pysimplicial documentation

pysimplicial is a lightweight Python package for working with simplicial complexes in Topological Deep Learning problems, created on foundation of [Open-Closed State-sum Neural Network](https://github.com/kaifczxc-lab/OCSSN)

The current version of the library (0.1.3) has the following set of functions:

* [Tools for visualization](https://github.com/kaifczxc-lab/pysimplicial/blob/SiritoriProjects/Documents/Documentation-Pysimplicial.md#tools-for-visualization): [visualize_triangulation_3D](https://github.com/kaifczxc-lab/pysimplicial/blob/SiritoriProjects/Documents/Documentation-Pysimplicial.md#visualize_triangulation_3dfigure-fs18-fs26-xlim-1-ylim-1-zlim---1-xlimright1-ylimright1-zlimright1-enable_random_face_colorsfalse-xlabx-axis-ylaby-axis-zlabz-axis-facecolorpurple-edgecolorwhite-custom_posnone-showtrue), [visualize_triangulation_2D](https://github.com/kaifczxc-lab/pysimplicial/blob/SiritoriProjects/Documents/Documentation-Pysimplicial.md#visualize_triangulation_2dfigure-typetriangles)

* [Pachner Moves](https://github.com/kaifczxc-lab/pysimplicial/blob/SiritoriProjects/Documents/Documentation-Pysimplicial.md#pachner-moves): [move_2_2](https://github.com/kaifczxc-lab/pysimplicial/blob/SiritoriProjects/Documents/Documentation-Pysimplicial.md#move_2_2tris), [move_1_3](https://github.com/kaifczxc-lab/pysimplicial/blob/SiritoriProjects/Documents/Documentation-Pysimplicial.md#move_1_3tris), [move_3_1](https://github.com/kaifczxc-lab/pysimplicial/blob/SiritoriProjects/Documents/Documentation-Pysimplicial.md#move_3_1tris), [move_1_4](https://github.com/kaifczxc-lab/pysimplicial/blob/SiritoriProjects/Documents/Documentation-Pysimplicial.md#move_1_4tetrahedron), [move_2_3](https://github.com/kaifczxc-lab/pysimplicial/blob/SiritoriProjects/Documents/Documentation-Pysimplicial.md#move_2_3tetrahedron), [move_4_1](https://github.com/kaifczxc-lab/pysimplicial/blob/SiritoriProjects/Documents/Documentation-Pysimplicial.md#move_4_1tetrahedron), [move_3_2](https://github.com/kaifczxc-lab/pysimplicial/blob/SiritoriProjects/Documents/Documentation-Pysimplicial.md#move_3_2tetrahedrons)

* [Data Converters for ML](https://github.com/kaifczxc-lab/pysimplicial/blob/SiritoriProjects/Documents/Documentation-Pysimplicial.md#converters): [Converters](https://github.com/kaifczxc-lab/pysimplicial/blob/SiritoriProjects/Documents/Documentation-Pysimplicial.md#converters)

* [Generators](https://github.com/kaifczxc-lab/pysimplicial/blob/SiritoriProjects/Documents/Documentation-Pysimplicial.md#generators): [combinatorial_torus](https://github.com/kaifczxc-lab/pysimplicial/blob/SiritoriProjects/Documents/Documentation-Pysimplicial.md#combinatorial_torusm-n), [combinatorial_torus_3D](https://github.com/kaifczxc-lab/pysimplicial/blob/SiritoriProjects/Documents/Documentation-Pysimplicial.md#combinatorial_torus_3dm-n-p), [geometry_bottle_of_klein](https://github.com/kaifczxc-lab/pysimplicial/blob/SiritoriProjects/Documents/Documentation-Pysimplicial.md#geometry_bottle_of_kleinu-v),[geometry_torus](https://github.com/kaifczxc-lab/pysimplicial/blob/SiritoriProjects/Documents/Documentation-Pysimplicial.md#geometry_torusmnrr)

* [Euler Characteristics computing tool](https://github.com/kaifczxc-lab/pysimplicial/blob/SiritoriProjects/Documents/Documentation-Pysimplicial.md#euler-characteristics-computing-tool): [euler_characteristics](https://github.com/kaifczxc-lab/pysimplicial/blob/SiritoriProjects/Documents/Documentation-Pysimplicial.md#euler_characteristics)

* [Experimental tools](https://github.com/kaifczxc-lab/pysimplicial/blob/SiritoriProjects/Documents/Documentation-Pysimplicial.md#experimental-tools): [state_sum](https://github.com/kaifczxc-lab/pysimplicial/blob/SiritoriProjects/Documents/Documentation-Pysimplicial.md#state_sumc-b_inv-v_p-g_edges-open_ports-type2d), [graph](https://github.com/kaifczxc-lab/pysimplicial/blob/SiritoriProjects/Documents/Documentation-Pysimplicial.md#graphfigure-type2d--3d)

---

<div align="center">
  <h1>Tools for visualization</h1>
</div>


Right now, this sector is only in its infancy, because there is no full 3D visualization with preservation of the structure of figures yet, so far there is only 2D

Tests:

* [Tutorials\Pachner_moves](https://github.com/kaifczxc-lab/pysimplicial/blob/SiritoriProjects/Tutorials/Pachner_moves.ipynb)

<div align="center">
  <h2>visualize_triangulation_2D(figure, type="Triangles")</h2>
</div>

This function works on top of networkx.Graph() and networkx.spring_layout, it takes vertices, connects them and renders them based on the given shape

We take a triangle, a list of the form (a,b,c) or (a,b,c,d) and distribute each of its vertices, then with the help of spring_layout we build a dict and then visualize it using draw


Parameters
----------

figure: list of tuple
* Triangles mesh list

type: str
* if type="Triangles" then function work with list of tuple in form of (a,b,c)

* if type="Tetrahedrons" then function work with list of tuple in form of (a,b,c,d)

Returns
-------

Visualized figure with using matplotlib
    
Examples
--------

The example can be found in official pysimplicial repository in Tutorials/showcase


---

<div align="center">
  <h2>visualize_triangulation_3D(figure, fs1=8, fs2=6, xlim=-1, ylim=-1, zlim = -1, xlimright=1, ylimright=1, zlimright=1, enable_random_face_colors=False, xlab="X axis", ylab="Y axis", zlab="Z axis", facecolor="Purple", edgecolor="White", custom_pos=None, show=True)</h2>
</div>


This function draws a figure using matplotlib's 3D projection. To set xyz correctly, it uses spring_layout with dimension = 3 from networkx. This function is still under development, but it works well with Triangles mesh list (a,b,c)
    
Parameters
----------

figure: list of tuple in form of
* (a,b,c) is triangles mesh list

* (a,b,c,d) is tetrahedrons mesh list


figsize=(fs1, fs2): ArrayLike
* figsize integer numbers

xlim / xlimright: float, optional
* The left/right xlim in data coordinates

ylim / ylimright: float, optional
* The left/right ylim in data coordinates
    
zlim / zlimright: float, optional
* The left/right zlim in data coordinates

enable_random_face_colors: boolean
* if true then ```face_colors = [[random.random() for _ in range(3)] for _ in figure]```

* else: user need to choose his own colors

xlab: str
* set_xlabel text
    
ylab: str
* set_ylabel text
    
zlab: str
* set_zlabel text
    
facecolor: str
* the figure face color
    
* if user make the enable_random_face_colors = False, then user can choose his own color. Standart is "Purple"

edgecolor: str
* the figure edge color

* if user make the enable_random_face_colors = False, then user can choose his own color. Standart is "White"

custom_pos: Any
* custom coords position (without spring_layout pos generation)
    
show: boolean
* If true: then user can see visualized by matplotlib figure

* else: return ax, fig

        
Returns
-------

Visualized figure

fig & ax: Figure and Axes3D

Examples
--------

>>> octahedron = [(0,1,2), (0,2,3), (0,3,4), (0,4,1),(5,2,1), (5,3,2), (5,4,3), (5,1,4)]

>>> PySimplicial.utils.visualize_triangulation_3D(octahedron, enable_random_face_colors=False)

>>> 3d_figure = PySimplicial.utils.move_1_3(octahedron)

>>> returns = PySimplicial.utils.visualize_triangulation_3D(abcd, enable_random_face_colors=False)

>>> print(returns)

(<Figure size 800x600 with 1 Axes>, <Axes3D: xlabel='X axis', ylabel='Y axis', zlabel='Z axis'>)
    
---

<div align="center">
  <h1>Pachner Moves</h1>
</div>

More information can be found:

1. [Open-Closed State Sum Neural Network Maths Introduction](https://github.com/kaifczxc-lab/OCSSN/blob/SiritoriProjects/OCSSN-Maths-Introduction.md)

2. [Wikipedia: Pachner Moves](https://en.wikipedia.org/wiki/Pachner_moves) (and from there you can get to the original source, the article by Udo Pachner)

Visualization can be found:

* [Tutorials\Pachner_moves](https://github.com/kaifczxc-lab/pysimplicial/blob/SiritoriProjects/Tutorials/Pachner_moves.ipynb)

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
  <h2>move_3_2(tetrahedrons)</h2>
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


---

---


<div align="center">
  <h1>Converters</h1>
</div>

Converter functions convert mesh data arrays into formats understandable for popular neural network architectures

Some experiments were conducted on synthetic data, and the results do not yet clearly indicate the value of these functions, but this will be clarified in future experiments

Tests:

1. [experiments\Converters_test](https://github.com/kaifczxc-lab/pysimplicial/blob/SiritoriProjects/experiments/converters_test.py)

2. [experiments\Converters_experiments](https://github.com/kaifczxc-lab/pysimplicial/blob/SiritoriProjects/experiments/converters_experiments.py)

3. [chain_test](https://github.com/kaifczxc-lab/pysimplicial/blob/SiritoriProjects/Tests/chain_test.py)

4. Tests\converter_mini_test

---

<div align="center">
  <h2>relabel(self, simplices)</h2>
</div>


Renumber vertices of a triangle mesh to consecutive integers starting from 0

Parameters
----------

figure: list of tuple
* list of tuple with form of (a,b,c) or (a,b,c,d) ; anything else right now unsupported
        
Returns
-------

list of tuple:
* Renumbered triangle mesh list

Examples
--------

>>> octahedron_ = [(0,10,20), (0,20,30), (0,30,40), (0,40,10),(50,20,10), (50,30,20), (50,40,30), (50,10,40)]
>>> octahedron_relabeled = PySimplicial.utils.relabel(octahedron_)
>>> print(f"Octahedron={octahedron_relabeled}")
Octahedron=[(0, 1, 2), (0, 2, 3), (0, 3, 4), (0, 4, 1), (5, 2, 1), (5, 3, 2), (5, 4, 3), (5, 1, 4)]

---

<div align="center">
  <h2>to_gnn(self, simplices)</h2>
</div>

Here we calculate the matrix from all vertices of tris-mesh, sum it and return:

Parameters
----------

figure: list of tuple
* list in form of (a,b,c) or (a,b,c,d) ; anything else are unsupported right now

Returns
-------

torch.Tensor:
* Normalized adjacency matrix of shape

* A / (s + 1e-8)

torch.Tensor:
* Node feature matrix of shape

* L

Notes
-----

* num_nodes = max(max(t) for t in tris)

* A = torch.zeros((num_nodes, num_nodes))
        
* L = torch.cat([degree, torch.ones(num_nodes, 1)], dim=1

* s = A.sum()

Examples
--------

>>> relabel = [(0, 1, 2), (0, 2, 3), (0, 3, 4), (0, 4, 1), (5, 2, 1), (5, 3, 2), (5, 4, 3), (5, 1, 4)]
>>> converter_GNN_2D = PySimplicial.utils.converter_for_gnn(relabel)
>>> print("CONVERTER GNN")
>>> print(converter_GNN)
CONVERTER GNN
(tensor([[0.0000, 0.0417, 0.0417, 0.0417, 0.0417, 0.0000],
  [0.0417, 0.0000, 0.0417, 0.0000, 0.0417, 0.0417],
  [0.0417, 0.0417, 0.0000, 0.0417, 0.0000, 0.0417],
  [0.0417, 0.0000, 0.0417, 0.0000, 0.0417, 0.0417],
  [0.0417, 0.0417, 0.0000, 0.0417, 0.0000, 0.0417],
  [0.0000, 0.0417, 0.0417, 0.0417, 0.0417, 0.0000]]), tensor([[0.1667, 1.0000],
  [0.1667, 1.0000],
  [0.1667, 1.0000],
  [0.1667, 1.0000],
  [0.1667, 1.0000],
  [0.1667, 1.0000]]))

---

>>> relabel = [(0, 1, 2, 3), (4, 1, 2, 3), (4, 0, 2, 3), (4, 0, 1, 3), (4, 0, 1, 2)]
>>> converter_gnn = PySimplicial.utils.converter_for_gnn(relabel)
>>> print("CONVERTER GNN")
>>> print(converter_gnn)
CONVERTER GNN
(tensor([[0.0000, 0.0500, 0.0500, 0.0500, 0.0500],
  [0.0500, 0.0000, 0.0500, 0.0500, 0.0500],
  [0.0500, 0.0500, 0.0000, 0.0500, 0.0500],
  [0.0500, 0.0500, 0.0500, 0.0000, 0.0500],
  [0.0500, 0.0500, 0.0500, 0.0500, 0.0000]]), tensor([[0.2000, 1.0000],
  [0.2000, 1.0000],
  [0.2000, 1.0000],
  [0.2000, 1.0000],
  [0.2000, 1.0000]]))

---

<div align="center">
  <h2>to_tnn(self, simplices, N)</h2>
</div>

Here we calculate the symmetric normalized adjacency matrix from tris-mesh data

Parameters
----------

figure: list of tuple
* list in form of (a,b,c) or (a,b,c,d) ; anything else are unsupported right now
        
N: int
* torch.zeros matrix N x N

Returns
-------

torch.Tensor:
* Normalized adjacency matrix of shape 

Examples
--------

>>> relabel_ = [(0, 1, 2), (0, 2, 3), (0, 3, 4), (0, 4, 1), (5, 2, 1), (5, 3, 2), (5, 4, 3), (5, 1, 4)]
>>> converter_TNN = PySimplicial.utils.converter_for_tnn(relabel_, 6)
>>> print("CONVERTER TNN")
>>> print(converter_TNN)
CONVERTER TNN
tensor([[0.0000, 0.2500, 0.2500, 0.2500, 0.2500, 0.0000],
    [0.2500, 0.0000, 0.2500, 0.0000, 0.2500, 0.2500],
    [0.2500, 0.2500, 0.0000, 0.2500, 0.0000, 0.2500],
    [0.2500, 0.0000, 0.2500, 0.0000, 0.2500, 0.2500],
    [0.2500, 0.2500, 0.0000, 0.2500, 0.0000, 0.2500],
    [0.0000, 0.2500, 0.2500, 0.2500, 0.2500, 0.0000]])
---

>>> relabel = [(0, 1, 2, 3), (4, 1, 2, 3), (4, 0, 2, 3), (4, 0, 1, 3), (4, 0, 1, 2)]
>>> converter_TNN = PySimplicial.utils.converter_for_tnn(relabel, 6)
>>> print("CONVERTER TNN")
>>> print(converter_TNN)
CONVERTER TNN
tensor([[0.0000, 0.2500, 0.2500, 0.2500, 0.2500, 0.0000],
[0.2500, 0.0000, 0.2500, 0.2500, 0.2500, 0.0000],
[0.2500, 0.2500, 0.0000, 0.2500, 0.2500, 0.0000],
[0.2500, 0.2500, 0.2500, 0.0000, 0.2500, 0.0000],
[0.2500, 0.2500, 0.2500, 0.2500, 0.0000, 0.0000],
[0.0000, 0.0000, 0.0000, 0.0000, 0.0000, 0.0000]])

---

<div align="center">
  <h2>to_mlp(self, simplices, return_chi=True)</h2>
</div>

Here we calculate the Histogram of vertex degrees, euler's characteristics, tris_per_vertex (F / V) and average deegree number

Histogram of verted degrees algorithm: 

>>> get the degree count for every node in tris

>>> count how many nodes share each degree value

Euler's Charactertic formula (2D):

>>> V = unique vertices, E = unique edges, F = number of faces, g = surface genus

>>> x = V - E + F = 2 - 2g

Calculating tris_per_vertex:

>>> Number of faces / unique vertices

Calculating average degree:

>>> 2 * unique edges / unique vertices

Parameters
----------

figure: list of tuple

* list in form of (a,b,c) or (a,b,c,d) ; anything else are unsupported right now

return_chi: boolean

Returns
------

if return_chi=True => return F, V, E, chi, bins[0], bins[1], bins[2], bins[3], avg_degree, tpv

else: return F, V, E, bins[0], bins[1], bins[2], bins[3], avg_degree, tpv

Examples
--------

>>> relabel_ = [(0, 1, 2), (0, 2, 3), (0, 3, 4), (0, 4, 1), (5, 2, 1), (5, 3, 2), (5, 4, 3), (5, 1, 4)]
>>> converter_MLP = PySimplicial.utils.converter_for_mlp(relabel_, return_chi=True)
>>> print("CONVERTED MLP")
>>> print(converter_MLP)
CONVERTED MLP
(8, 6, 12, 0, 0, 6, 0, 0, 4.0, 1.3333333333333333)


>>> relabel = [(0, 1, 2, 3), (4, 1, 2, 3), (4, 0, 2, 3), (4, 0, 1, 3), (4, 0, 1, 2)]
>>> converter_MLP = PySimplicial.utils.converter_for_mlp(relabel, return_chi=True)
>>> print("CONVERTED MLP")
>>> print(converter_MLP)
CONVERTED MLP
(10, 5, 10, 0, 0, 5, 0, 0, 4.0, 2.0)
---



<div align="center">
  <h2>chain_2D(base, label, K, p_13=0.35, p_22=0.55, p_31=0.10, return_stats=True)</h2>
</div>

synthetic dataset generator function

in foundation of this function we have Markov chain algorithm: 
    
P(X_n+1 = x_n+1 | X_n = x_n, X_n-1 = x_n-1, ... , X_0 = x_0) = P(X_n+1 = x_n+1 | X_n = x_n)
    
This algorithm models transitions from one state to another

The sum of all Pachner Moves chances must not exceed 1

Parameters
----------

base: list of tuple
* Figure (torus, triangle)
    
label: int
* The genus of figure ; out.append((current, label)) (where current - figure with using pachner move and label is id of this figure)

K: int
* Amount of figure's what you want to be returned
    
p_13: int
* Chance of pachner move 1-3 (NEED TO BE 0.0-1.0)
    
p_31: int
* Chance of pachner move 3-1 (NEED TO BE 0.0-1.0)
    
p_22: int
* Chance of pachner move 2-2 (NEED TO BE 0.0-1.0)

return_stats: boolean

* Calculates how much pachner moves of all type's has been done by this function ; **if true**: return out, stats_1_3, stats_2_2, stats_3_1 ; **if false**: return out 

Returns
-------

out: list of tuple
* Generated dataset with K amount of figure's with different Pachner Moves

---

<div align="center">
  <h2>chain_3D(base, label, K, p_14 = 0.25, p_41=0.15, p_32=0.40, p_23=0.20, return_stats=True)</h2>
</div>


synthetic dataset generator function

in foundation of this function we have Markov chain algorithm: 

P(X_n+1 = x_n+1 | X_n = x_n, X_n-1 = x_n-1, ... , X_0 = x_0) = P(X_n+1 = x_n+1 | X_n = x_n)

This algorithm models transitions from one state to another

The sum of all Pachner Moves chances must not exceed 1

Parameters
----------

base: list of tuple
* Figure (torus, triangle)

label: int
* The genus of figure ; out.append((current, label)) (where current - figure with using pachner move and label is id of this figure)

K: int
* Amount of figure's what you want to be returned

p_14: int
* Chance of pachner move 1-4 (NEED TO BE 0.0-1.0)
    
p_41: int
* Chance of pachner move 4-1 (NEED TO BE 0.0-1.0)

p_23: int
* Chance of pachner move 2-3 (NEED TO BE 0.0-1.0)

p_32: int
* Chance of pachner move 3-2 (NEED TO BE 0.0-1.0)

return_stats: boolean
* Calculates how much pachner moves of all type's has been done by this function ; if true: return out, stats_1_3, stats_2_2, stats_3_1 ; if false: return out 

Returns
-------

out: list of tuple
* Generated dataset with K amount of figure's with different Pachner Moves

---

<div align="center">
  <h1>Generators</h1>
</div>

This section of the toolkit allows the user to generate certain shapes, such as a torus and a Klein bottle. This is primarily used for creating synthetic datasets

Used: 

* [Genus-invariance-under-Pachner-moves](https://github.com/kaifczxc-lab/pysimplicial/blob/SiritoriProjects/Tests/Genus-invariance-under-Pachner-moves.py)

* [chain_test](https://github.com/kaifczxc-lab/pysimplicial/blob/SiritoriProjects/Tests/chain_test.py)

<div align="center">
  <h2>combinatorial_torus(m, n)</h2>
</div>

The function generates a combinatorial form of the torus figure, resulting in a list (matrix) of triangles (2D)

Parameters
----------

m: int

* Size of torus

n: int

* Size of torus

Returns
-------

tris: list of tuple

* Torus with size m x n

Examples
--------

>>> combinatorial_torus_2D = PySimplicial.utils.combinatorial_torus(3,3)

>>> print("combinatorial torus 2d")

>>> print(combinatorial_torus_2D)

combinatorial torus 2d

[(0, 1, 3), (1, 4, 3), (1, 2, 4), (2, 5, 4), (2, 0, 5), (0, 3, 5), (3, 4, 6), (4, 7, 6), (4, 5, 7), (5, 8, 7), (5, 3, 8), (3, 6, 8), (6, 7, 0), (7, 1, 0), (7, 8, 1), (8, 2, 1), (8, 6, 2), (6, 0, 2)]

---

<div align="center">
  <h2>geometry_torus(m,n,R,r)</h2>
</div>

This function generates a geometric torus (suitable for custom visualization) in the form of a point cloud or surface

The function is based on basic torus generation formulas

x = (R + r * np.cos(v)) * np.cos(u)

y = (R + r * np.cos(v)) * np.sin(u)

z = r * np.sin(v)
    
Parameters
----------

m: int

* Number of partition points based on parameters u

n: int

* Number of partition points based on parameters v

R: int

* R major

r: int

* r minor

Returns
-------

result: dict[int, tuple[float, float, float]]

* geometric torus

Examples
--------
    
>>> geometry_torus_3D = PySimplicial.utils.geometry_torus(3,3,2,1)

>>> print("geometry torus 3d")

>>> print(geometry_torus_3D)

geometry torus 3d

{0: (np.float64(3.0), np.float64(0.0), np.float64(0.0)), 1: (np.float64(1.5000000000000002), np.float64(0.0), np.float64(0.8660254037844387)), 2: (np.float64(1.4999999999999996), np.float64(0.0), np.float64(-0.8660254037844385)), 3: (np.float64(-1.4999999999999993), np.float64(2.598076211353316), np.float64(0.0)), 4: (np.float64(-0.7499999999999998), np.float64(1.2990381056766582), np.float64(0.8660254037844387)), 5: (np.float64(-0.7499999999999994), np.float64(1.2990381056766578), np.float64(-0.8660254037844385)), 6: (np.float64(-1.5000000000000013), np.float64(-2.5980762113533156), np.float64(0.0)), 7: (np.float64(-0.7500000000000008), np.float64(-1.299038105676658), np.float64(0.8660254037844387)), 8: (np.float64(-0.7500000000000004), np.float64(-1.2990381056766573), np.float64(-0.8660254037844385))}

---

<div align="center">
  <h2>combinatorial_torus_3D(m, n, p)</h2>
</div>

The function generates a combinatorial form of the torus figure, resulting in a list (matrix) of triangles (3D)

Parameters
----------

m: int

* Size of torus

n: int

* Size of torus

p: int

* Size of torus

Returns
-------

tets: list of tuple
* Torus with size m x n x p

Examples
--------

>>> combinatorial_torus_3D = PySimplicial.utils.combinatorial_torus_3D(2,2,2)

>>> print("combinatorial torus 3d")

>>> print(combinatorial_torus_3D)

combinatorial torus 3d

[(0, 4, 6, 7), (0, 4, 5, 7), (0, 2, 6, 7), (0, 2, 3, 7), (0, 1, 5, 7), (0, 1, 3, 7), (1, 5, 7, 6), (1, 5, 4, 6), (1, 3, 7, 6), (1, 3, 2, 6), (1, 0, 4, 6), (1, 0, 2, 6), (2, 6, 4, 5), (2, 6, 7, 5), (2, 0, 4, 5), (2, 0, 1, 5), (2, 3, 7, 5), (2, 3, 1, 5), (3, 7, 5, 4), (3, 7, 6, 4), (3, 1, 5, 4), (3, 1, 0, 4), (3, 2, 6, 4), (3, 2, 0, 4), (4, 0, 2, 3), (4, 0, 1, 3), (4, 6, 2, 3), (4, 6, 7, 3), (4, 5, 1, 3), (4, 5, 7, 3), (5, 1, 3, 2), (5, 1, 0, 2), (5, 7, 3, 2), (5, 7, 6, 2), (5, 4, 0, 2), (5, 4, 6, 2), (6, 2, 0, 1), (6, 2, 3, 1), (6, 4, 0, 1), (6, 4, 5, 1), (6, 7, 3, 1), (6, 7, 5, 1), (7, 3, 1, 0), (7, 3, 2, 0), (7, 5, 1, 0), (7, 5, 4, 0), (7, 6, 2, 0), (7, 6, 4, 0)]

---

<div align="center">
  <h2>geometry_bottle_of_klein(u, v)</h2>
</div>

Calculates the coordinates of the Klein bottle points given the parameterization

Parameters
----------

u: np.ndarray

* Array of first parameter values

v: np.ndarray
* Array of second parameter values (must have the same shape as u)

Returns
-------

x : np.ndarray

* x-coordinates of surface points ; shape matches u, v
y : np.ndarray

* y-coordinates of surface points
z : np.ndarray

* z-coordinates of surface points

Examples
--------

>>> u = np.linspace(0, 2*np.pi, 100)

>>> v = np.linspace(0, 2*np.pi, 100)

>>> u, v = np.meshgrid(u, v)

>>> x, y, z = PySimplicial.utils.geometry_bottle_of_klein(u, v)

>>> fig = plt.figure()

>>> ax = fig.add_subplot(111, projection='3d')

>>> ax.plot_surface(x, y, z)

>>> plt.show()

---

<div align="center">
  <h1>Euler Characteristics computing tool</h1>
</div>

Now, in library we have only one tool

Tests:

* Tests\showcase

* utils\converters

* Tests\Genus-invariance-under-Pachner-moves

---

<div align="center">
  <h2>euler_characteristics</h2>
</div>


Calculates the Euler's characteristics for mesh in form of (a,b,c) and mesh in form of (a,b,c,d)

(a,b,c): The Euler's Characteristics has invented by Leonard Euler and looks like that x = V - E + F = 2 - 2g, so, we can find g if we change this formula (Assumes the mesh is a closed orientable surface)

(a,b,c,d): Formula: χ = V - E + F - T

Note
----

* Vertices and edges are counted uniquely

* V is unique vertices

* E is unique edges

* F is unique faces

* T is amount of tetrahedrons

Parameters
----------
mesh: list of tuple

* Enter triangulation list
    
Returns
-------

g / x: int
    
* Natural number that says the genus of the surface

2D - g. Formula "g = (2 - (V-E+F)) // 2"

3D - x. Formula "χ = V - E + F - T"

Examples
--------

>>> octahedron = [(0,1,2), (0,2,3), (0,3,4), (0,4,1),(5,2,1), (5,3,2), (5,4,3), (5,1,4)]
>>> print(euler_characteristics(octahedron))
0
>>> tetrahedron = [(0, 1, 2, 3),(0, 1, 2, 4)]
>>> print(euler_characteristics(tetrahedra))
1



---


<div align="center">
  <h1>Experimental tools</h1>
</div>

This section contains experimental items, which, in the author's understanding, are items whose value is very difficult to assess and were added only out of simple interest

Tests:

* Tutorials\showcase

---

<div align="center">
  <h2>state_sum(C, b_inv, v_p, g_edges, open_ports=(), type="2D")</h2>
</div>


This function deserves a separate discussion:

it implements convolution over triangulation, but by itself does not guarantee topological invariance. Invariance depends on the tensors C and b_inv, which in the trained version may not satisfy the Frobenius axioms. That is, for the correct result you need a fixed Frobenius algebra

More information can be found in https://github.com/kaifczxc-lab/OCSSN (the description of each parameter is quite complex and sometimes heavily depends on the context)

* type == "2D" State-sum for triangles

* type == "3D" State-sum for tetrahedrons (# 3d is experimental because we have questions about the math part)

Returns
-------

torch.Tensor or numpy.ndarray
* Result of the state-sum contraction where rank equals the number of open ports

Examples
--------

>>> C = np.array([[[1.,0.],[0.,1.]],[[0.,1.],[1.,0.]]])

>>> b_inv = np.array([[1.,0.],[0.,1.]])

>>> before = state_sum(C, b_inv, [(0,1,2),(3,4,5)], [(0,3),(1,4),(2,5)], ())

>>> after = state_sum(C, b_inv, [(0,1,2),(3,4,5)], [(0,4),(1,3),(2,5)], ())

>>> print(before, after, np.isclose(before, after))

4.0 4.0 True

---


<div align="center">
  <h2>graph(figure, type="2D / 3D")</h2>
</div>


A helper function for state-sum that can calculate the number of open ports / vertice ports / glued edges

Parameters
----------

figure: list of tuple
* Tetrahedrons/Triangles mesh list

Returns
-------

v_p: list of tuple
* vertice ports

g_edges: list of tuple
* glued edges

open_ports: list of tuple
* external unconnected ends of the network

Examples
--------

>>> triangles = [(0, 1, 2), (0, 2, 3)]

>>> v_p, g_edges, open_ports = ps.graph(triangles)

>>> print("v_p: ", v_p)

>>> print("g_edges: ", g_edges)

>>> print("open_ports: ", open_ports)

>>> tetrahedrons = [(0, 1, 2, 3),(0, 1, 2, 4)]

>>> v_p_3D, g_edges_3D, open_ports_3D = ps.graph(tetrahedrons)

>>> print("v_p_3D: ", v_p_3D)

>>> print("g_edges_3D: ", g_edges_3D)

>>> print("open_ports_3D: ", open_ports_3D)

v_p:  [(0, 1, 2), (3, 4, 5)]

g_edges:  [(2, 3)]

open_ports:  [0, 1, 4, 5]

v_p_3D:  [(0, 1, 2, 3), (4, 5, 6, 7)]

g_edges_3D:  [(0, 4)]

open_ports_3D:  [1, 2, 3, 5, 6, 7]

---

<div align="center">
  <h1>Changelog</h1>
</div>


Here author will write all about changes in updates

<div align="center">
  <h2>Version 1.3</h2>
</div>

* State-sum has optimized and fixed one bug, the graph() function return a g_edges with 2 ports for (a,b,c) and (a,b,c,d) list of tuples, but in 3D state-sum was ```for (x,y,z) in g_edges```

* Fixed bug: in converter_for_gnn fixed `A[u,w]=1.0` to `A[u,w]=A[w,u]=1.0`

* Merged `compute_connected_components_3D` and `compute_genus` into a single function. Also, the name `compute_connected_components_3D` is a bit of a misnomer—it would be better to name it more generally, such as `eulers_characteristics`

* In PachnerMoves in move_3_1 added e_count check: `if e_count[tuple(sorted((u,v)))] != 2: ; break`

* Optimized Converters, merged 2d and 3d functions in one general class

* The documentation was rewritten

* Added new ```converters_test``` and rewritten the ```Genus-invariance-under-Pachner-moves```




