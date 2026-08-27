# Contributing to PySimplicial

Thanks for your interest! All contributions are welcome: bug reports, documentation, tests, new features

## How to contribute

1. Fork the repository
2. Make changes in your fork
3. Open a Pull Request with a description

## Code style

* Write readable code (PEP 8 if possible)
* Add docstrings for new functions (1-2 lines)
* No strict formatter required - just keep it consistent

## Ideas for contributions

* Add correct 3D visualization for torus (geometric)

* Add more geometric/combinatorial figure generators (twisted-torus, Mobius strip, Lens spaces L(p,q) and more)

* Add more converters for mesh data into input data native to neural network architectures

* Evaluate and improve the converters for GNN/TNN/MLP. Compare them with standard preprocessing pipelines from PyTorch Geometric or DGL, and propose better normalization schemes, feature vectors, or output formats if needed

* Find out why triangulation visualization sometimes varies (perhaps because the visualization is in 2D, or maybe something with Pachner Moves)

* Improve documentation/examples

### Research ideas

* Implement a strict Frobenius algebra checker

* Add self-loops into converters

* Write a code whose state-sum will show invariance to triangulations (that is, apply the axioms of commutative Frobenius algebra, count the numbers, and use the state-sum function before and after triangulations)

* Add Lens spaces L(p,q) generator

## Good first issues

* Improve documentation of specific functions (generators, Pachner Moves)

* Add docstring examples (in NumPy style)

* Optimization

Questions? Open an issue!