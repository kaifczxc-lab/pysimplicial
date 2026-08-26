# pysimplicial

PySimplicial is Python library for PL topology, Pachner moves, and TQFT-inspired state-sum, with converters for GNN/TNN/MLP

Note: This is experimental research code for topological deep learning. Not intended for production use

Author: siritoriyowai

Stage: Early development / experimental

## Installation

```
pip install git+https://github.com/kaifczxc-lab/pysimplicial.git
```

## Quick Start

(The visualization results can be found in [showcase](https://github.com/kaifczxc-lab/pysimplicial/blob/SiritoriProjects/showcase.ipynb))

```python

import PySimplicial.utils

octahedron_ = [(10, 50, 15),(10, 15, 25),(10, 25, 40),(10, 40, 50),(90, 15, 50),(90, 25, 15),(90, 40, 25),(90, 50, 40)]

octahedron_relabeled = PySimplicial.utils.relabel(octahedron_)

print("Let's visualize the octahedron!")
PySimplicial.utils.visualize_triangulation_2D(octahedron_relabeled)

print("Let's modify this octahedron with Pachner Move 1-3 and visualize it!")
octahedron_modify = PySimplicial.utils.move_1_3(octahedron_relabeled)
PySimplicial.utils.visualize_triangulation_2D(octahedron_modify)

print("Let's return all back with Pachner move 3-1 and visualize it!")
octahedron_return = PySimplicial.utils.move_3_1(octahedron_modify)
PySimplicial.utils.visualize_triangulation_2D(octahedron_return)

print("Let's calculate genus of this octahedron!")
Compute_genus = PySimplicial.utils.compute_genus_2D(octahedron_return)
print(f"genus={Compute_genus}")
"""
genus=0
"""

print("Let's convert this figure to into the feature vector for MLP!")
Converter = PySimplicial.utils.converter_for_mlp(octahedron_return, return_g=True) # return F, V, E, g, bins[0], bins[1], bins[2], bins[3], avg_degree, tpv ; 
# Where V = unique vertices, E = unique edges, F = number of faces, g = surface genus ; bins is Histogram of vertex degrees ; avg_degree is "2 * unique edges / unique vertices" ; tpv is "Number of faces / unique vertices"
print(f"result={Converter}")
"""
result=(8, 6, 12, 0, 0, 6, 0, 0, 4.0, 1.3333333333333333)
"""
```

## Features

* Pachner Moves (2-2 ; 3-1 ; 1-3 ; 2-3 ; 3-2 ; 1-4 ; 4-1)

* Triangulation generators (2D/3D torus)

* Topological invariants (genus, connected components)

* TQFT state-sum (on foundation of [Aaron D. Lauda , Hendryk Pfeiffer (2006): State sum construction of two-dimensional open-closed Topological Quantum Field Theories](https://arxiv.org/abs/math/0602047))

* Converters for GNN/TNN/MLP and 3D versions

## Documentation

See [showcase notebook](https://github.com/kaifczxc-lab/pysimplicial/blob/SiritoriProjects/showcase.ipynb) to see how all functions work (visualization & logs)

Full documentation will be available later

## Contributing

Contributions welcome! See [CONTRIBUTING.md](https://github.com/kaifczxc-lab/pysimplicial/blob/SiritoriProjects/CONTRIBUTING.md) for guidelines

