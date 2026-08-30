import PySimplicial.utils as ps
from collections import Counter
import random
from PySimplicial.utils.converters import chain_2D
import torch

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

octahedron = [(0,1,2), (0,2,3), (0,3,4), (0,4,1),(5,2,1), (5,3,2), (5,4,3), (5,1,4)] #8 triangles list
octabipyramid = [(0,1,2), (0,2,3), (0,3,4), (0,4,5), (0,5,6), (0,6,7), (0,7,8), (0,8,1),(9,2,1), (9,3,2), (9,4,3), (9,5,4), (9,6,5), (9,7,6), (9,8,7), (9,1,8)] #16 triangles list
hexabipyramid = [(0,1,2), (0,2,3), (0,3,4), (0,4,5), (0,5,6), (0,6,1),(7,2,1), (7,3,2), (7,4,3), (7,5,4), (7,6,5), (7,1,6)] #12 triangles list
icosahedron = [(0,11,5), (0,5,1), (0,1,7), (0,7,10), (0,10,11),(1,5,9), (5,11,4), (11,10,2), (10,7,6), (7,1,8),(3,9,4), (3,4,2), (3,2,6), (3,6,8), (3,8,9),(4,9,5), (2,4,11), (6,2,10), (8,6,7), (9,8,1)] # 20 triangles, 12 edges, by euler characteristic x=12 - 30 + 20 = 2 => 2 = 2 - 2g = 2g = 0 => g=0 (sphere)
tetrahedron = [(0, 1, 2, 3),(0, 1, 2, 4)]
spheres = [icosahedron, hexabipyramid, octahedron, octabipyramid]

def dataset(k, n=None, p=None):
    if n is None:
        n = k // len(spheres)
    if p is None:
        p = k // n
    out = []
    for b in spheres:
        out += ps.chain_2D(b, 0, n, return_stats=False) # generation g=0 (spheres)
    out += ps.chain_2D(ps.combinatorial_torus(3, 3), 1, k, return_stats=False) # generation g=1 (torus)
    #out += ps.chain_3D(tetrahedron, 0, p, return_stats=False)
    return out

trainset = dataset(200, 200, 200)
print(trainset)

class gnn(torch.nn.Module):
    def __init__(self):
        super().__init__()
        self.W1 = torch.nn.Parameter(torch.randn(2, 8) * 0.1)
        self.W2 = torch.nn.Parameter(torch.randn(8, 8) * 0.1)
        self.classifier = torch.nn.Linear(8, 2)
    def forward(self, a, L):
        agg1 = a @ L # in basic gnn agg its looking like that: agg1 = (a @ L) / degree.reshape(-1,1) ; If i remember well (its been 3-4 weeks ago) with that basic construction i had some kind of problems with prediction, everytime the basic version was 50% pred
        L1 = torch.nn.functional.relu(agg1 @ self.W1)
        agg2 = a @ L1
        L2 = torch.nn.functional.relu(agg2 @ self.W2)
        graph_vec = L2.mean(dim=0)
        logits = self.classifier(graph_vec)
        return logits
def prep(A):
    a = A + torch.eye(A.shape[0], device=A.device)
    return a

model = gnn()
optim = torch.optim.AdamW(model.parameters(), lr=0.01)

for i in range(200):
    model.to(device)
    model.train()
    err_sum, correct = 0.0, 0
    for fig, label in trainset:
        y = torch.tensor([label], dtype=torch.long).to(device)
        A,L = ps.converter_for_gnn(fig)
        A = A.to(device)
        L = L.to(device)
        optim.zero_grad()
        A_hat1 = prep(A)
        pred_gnn = model(A_hat1,L)
        err_gnn = torch.nn.functional.cross_entropy(pred_gnn.unsqueeze(0), y)
        err_gnn.backward()
        optim.step()
        err_sum += err_gnn.item()
        correct += int(pred_gnn.argmax().item() == label)
    print(f"GNN ep={i}, loss={err_sum/len(trainset):.8f}, train_acc={correct/len(trainset):.2%}")

"""GNN ep=0, loss=0.11319234, train_acc=98.60%
GNN ep=1, loss=0.34295302, train_acc=87.70%
GNN ep=2, loss=0.34015434, train_acc=87.00%
GNN ep=3, loss=0.34406800, train_acc=86.70%
GNN ep=4, loss=0.34577674, train_acc=86.50%
GNN ep=5, loss=0.34653714, train_acc=86.50%
GNN ep=6, loss=0.34687929, train_acc=86.50%
GNN ep=7, loss=0.34703397, train_acc=86.50%
GNN ep=8, loss=0.34710385, train_acc=86.50%
GNN ep=9, loss=0.34713535, train_acc=86.50%
GNN ep=10, loss=0.34714967, train_acc=86.40%
GNN ep=11, loss=0.34715626, train_acc=86.40%
GNN ep=12, loss=0.34715913, train_acc=86.40%
GNN ep=13, loss=0.34716054, train_acc=86.40%"""