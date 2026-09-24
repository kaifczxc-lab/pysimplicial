import PySimplicial.utils as ps
import torch
from PySimplicial.utils import Converters

conv = Converters(  )
k = [(0,1,2)]
a,x = conv.to_gnn(k)

assert a.shape == (3,3)
assert torch.equal(a, a.T)
assert a[0,1] != 0
assert a[1,2] != 0
assert a[0,2] != 0

# =-=-=-=-=-=-=-=-=-=-

A = conv.to_tnn(k, N=3)

assert A.shape == (3, 3)
assert torch.equal(A, A.T)
assert A[0,0] == 0 and A[1,1] == 0 and A[2,2] == 0
assert A[0,1] != 0
assert A[1,2] != 0
assert A[0,2] != 0

# =-=-=-=-=-=-=-=-=-=-

features = conv.to_mlp(k, return_chi=True)
F, V, E, chi, b0, b1, b2, b3, avg_degree, tpv = features

assert F == 1
assert V == 3
assert E == 3
assert b0 == 3
assert b1 == 0
assert b2 == 0
assert b3 == 0
assert avg_degree == 2.0
assert abs(tpv - 1/3) < 1e-9