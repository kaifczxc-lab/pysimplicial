import torch
import PySimplicial.utils
import random
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
class tnn(torch.nn.Module):
    def __init__(self, N=64):
        super().__init__()
        self.N = N
        self.u = torch.nn.Parameter(torch.randn(N, 2) * 0.1)
        self.v = torch.nn.Parameter(torch.randn(N, 2) * 0.1)
        self.bias = torch.nn.Parameter(torch.zeros(2))
    def forward(self, A):
        logits = torch.einsum("bij, ic, jc -> bc", A, self.u, self.v)
        return logits + self.bias

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

class MLP(torch.nn.Module):
    def __init__(self, n_features):
        super().__init__()
        self.layer1 = torch.nn.Linear(n_features, 128)
        self.layer2 = torch.nn.Linear(128, 64)
        self.layer3 = torch.nn.Linear(64, 2)
    def forward(self, x):
        x = self.layer1(x)
        x = torch.nn.functional.relu(x)
        x = self.layer2(x)
        x = torch.nn.functional.relu(x)
        x = self.layer3(x)
        return x



def pachner_move_selection(base):
    current = base
    for _ in range(5):
        r = random.random()
        if r < 0.5:
            new = PySimplicial.utils.p_2_3(current)
            if new is not None:
                current = new
        else:
            current = PySimplicial.utils.p_1_4(current)
    return current

def dataset_(n_spheres, n_tors):
    dataset = []
    tetrahedra = [(1,2,3,4), (0,2,3,4), (0,1,3,4), (0,1,2,4), (0,1,2,3)]
    torus = PySimplicial.utils.combinatorial_torus_3D(3,3,3)

    for _ in range(n_spheres):
        new_tetra = pachner_move_selection(tetrahedra)
        dataset.append((new_tetra, 0))

    for _ in range(n_tors):
        new_torus = pachner_move_selection(torus)
        dataset.append((new_torus, 1))

    return dataset

data = dataset_(200, 200)
random.shuffle(data)

calc_n_features_in_mlp = PySimplicial.utils.converter_for_mlp_3D(data[0][0])
n_features = len(calc_n_features_in_mlp)

model_mlp = MLP(n_features)
optim_mlp = torch.optim.AdamW(model_mlp.parameters(), lr=0.01)

model_tnn = tnn()
optim_tnn = torch.optim.AdamW(model_tnn.parameters(), lr=0.01)

model_gnn = gnn()
optim_gnn = torch.optim.AdamW(model_gnn.parameters(), lr=0.01)


for tr in range(100):
    print(f"epoch {tr}")
    model_mlp = model_mlp.to(device)
    model_tnn = model_tnn.to(device)
    model_gnn = model_gnn.to(device)
    model_mlp.train()
    model_gnn.train()
    model_tnn.train()

    err_sum_mlp, err_sum_tnn, err_sum_gnn,correct_mlp, correct_gnn, correct_tnn = 0.0,0.0,0.0,0,0,0
    
    for tetra, label in data:
        y = torch.tensor([label], dtype=torch.long).to(device)
        features = PySimplicial.utils.converter_for_mlp_3D(tetra)
        A_mlp = torch.tensor(features, dtype=torch.float32).unsqueeze(0).to(device)
        optim_mlp.zero_grad()
        pred_mlp = model_mlp(A_mlp)
        err_mlp = torch.nn.functional.cross_entropy(pred_mlp, y)
        err_mlp.backward()
        optim_mlp.step()
        err_sum_mlp += err_mlp.item()
        correct_mlp += int(pred_mlp.argmax().item() == label)

        A_tnn = PySimplicial.utils.converter_for_tnn_3D(tetra, 64).to(device)
        A_tnn = A_tnn.unsqueeze(0)
        optim_tnn.zero_grad()
        pred_tnn = model_tnn(A_tnn)
        err_tnn = torch.nn.functional.cross_entropy(pred_tnn,y)
        err_tnn.backward()
        optim_tnn.step()
        err_sum_tnn += err_tnn.item()
        correct_tnn += int(pred_tnn.argmax().item() == label)

        A,L = PySimplicial.utils.converter_for_gnn_3D(tetra)
        A = A.to(device)
        L = L.to(device)
        optim_gnn.zero_grad()
        A_hat1 = prep(A)
        pred_gnn = model_gnn(A_hat1,L)
        err_gnn = torch.nn.functional.cross_entropy(pred_gnn.unsqueeze(0), y)
        err_gnn.backward()
        optim_gnn.step()
        err_sum_gnn += err_gnn.item()
        correct_gnn += int(pred_gnn.argmax().item() == label)

    print(f"MLP ep={tr}, loss={err_sum_mlp/len(data):.8f}, train_acc={correct_mlp/len(data):.2%}")
    print(f"GNN ep={tr}, loss={err_sum_gnn/len(data):.8f}, train_acc={correct_gnn/len(data):.2%}")
    print(f"TNN ep={tr}, loss={err_sum_tnn/len(data):.8f}, train_acc={correct_tnn/len(data):.2%}")


"""
The results certainly look quite interesting and suspicious. Yes, it's most likely a shortcut
In any case, the purpose of this code is to demonstrate that converters work and that neural network architectures can detect and respond correctly.
Honestly, shortcuts will work on this synthetic test, but they probably won't on real data. TODO: check on a real dataset

epoch 0
MLP ep=0, loss=0.65292513, train_acc=96.50%
GNN ep=0, loss=0.36712480, train_acc=84.25%
TNN ep=0, loss=0.07746737, train_acc=97.25%
epoch 1
MLP ep=1, loss=0.00000647, train_acc=100.00%
GNN ep=1, loss=0.01021253, train_acc=100.00%
TNN ep=1, loss=0.00063966, train_acc=100.00%
epoch 2
MLP ep=2, loss=0.00001284, train_acc=100.00%
GNN ep=2, loss=0.00284870, train_acc=100.00%
TNN ep=2, loss=0.00028508, train_acc=100.00%
epoch 3
MLP ep=3, loss=0.00001750, train_acc=100.00%
GNN ep=3, loss=0.00158064, train_acc=100.00%
TNN ep=3, loss=0.00017610, train_acc=100.00%
epoch 4
MLP ep=4, loss=0.00001816, train_acc=100.00%
GNN ep=4, loss=0.00107070, train_acc=100.00%
TNN ep=4, loss=0.00012355, train_acc=100.00%
epoch 5
MLP ep=5, loss=0.00001669, train_acc=100.00%
GNN ep=5, loss=0.00078588, train_acc=100.00%
TNN ep=5, loss=0.00009216, train_acc=100.00%
epoch 6
MLP ep=6, loss=0.00001463, train_acc=100.00%
GNN ep=6, loss=0.00060274, train_acc=100.00%
TNN ep=6, loss=0.00007101, train_acc=100.00%
epoch 7
MLP ep=7, loss=0.00001252, train_acc=100.00%
GNN ep=7, loss=0.00047316, train_acc=100.00%
TNN ep=7, loss=0.00005571, train_acc=100.00%
epoch 8
MLP ep=8, loss=0.00001052, train_acc=100.00%
GNN ep=8, loss=0.00037667, train_acc=100.00%
TNN ep=8, loss=0.00004417, train_acc=100.00%
epoch 9
MLP ep=9, loss=0.00000871, train_acc=100.00%
GNN ep=9, loss=0.00030263, train_acc=100.00%
TNN ep=9, loss=0.00003523, train_acc=100.00%
epoch 10
MLP ep=10, loss=0.00000712, train_acc=100.00%
GNN ep=10, loss=0.00024480, train_acc=100.00%
TNN ep=10, loss=0.00002821, train_acc=100.00%
epoch 11
MLP ep=11, loss=0.00000578, train_acc=100.00%
GNN ep=11, loss=0.00019876, train_acc=100.00%
TNN ep=11, loss=0.00002264, train_acc=100.00%
epoch 12
MLP ep=12, loss=0.00000467, train_acc=100.00%
GNN ep=12, loss=0.00016187, train_acc=100.00%
TNN ep=12, loss=0.00001820, train_acc=100.00%
epoch 13
MLP ep=13, loss=0.00000375, train_acc=100.00%
GNN ep=13, loss=0.00013201, train_acc=100.00%
TNN ep=13, loss=0.00001464, train_acc=100.00%
epoch 14
MLP ep=14, loss=0.00000304, train_acc=100.00%
GNN ep=14, loss=0.00010799, train_acc=100.00%
TNN ep=14, loss=0.00001179, train_acc=100.00%
epoch 15
MLP ep=15, loss=0.00000330, train_acc=100.00%
GNN ep=15, loss=0.00008853, train_acc=100.00%
TNN ep=15, loss=0.00000950, train_acc=100.00%

"""