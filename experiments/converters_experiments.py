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
        dataset.append((tetrahedra, 0))

    for _ in range(n_tors):
        dataset.append((torus, 1))

    return dataset

data = dataset_(200, 200)
random.shuffle(data)



model_mlp = MLP(1)
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
        optim_mlp.zero_grad()

        x_mlp = torch.tensor([len(tetra)], dtype=torch.float32).unsqueeze(0).to(device)
        pred_mlp = model_mlp(x_mlp)
        err_mlp = torch.nn.functional.cross_entropy(pred_mlp, y)
        err_mlp.backward()
        optim_mlp.step()
        err_sum_mlp += err_mlp.item()
        correct_mlp += int(pred_mlp.argmax().item() == label)

        # gnn and tnn do not work if you feed them raw data (without using converter)

        """        
        optim_tnn.zero_grad()
        pred_tnn = model_tnn(tetra)
        err_tnn = torch.nn.functional.cross_entropy(pred_tnn,y)
        err_tnn.backward()
        optim_tnn.step()
        err_sum_tnn += err_tnn.item()
        correct_tnn += int(pred_tnn.argmax().item() == label)

        optim_gnn.zero_grad()
        A_hat1 = prep(tetra)
        pred_gnn = model_gnn(A_hat1,tetra)
        err_gnn = torch.nn.functional.cross_entropy(pred_gnn.unsqueeze(0), y)
        err_gnn.backward()
        optim_gnn.step()
        err_sum_gnn += err_gnn.item()
        correct_gnn += int(pred_gnn.argmax().item() == label)"""


    print(f"MLP ep={tr}, loss={err_sum_mlp/len(data):.8f}, train_acc={correct_mlp/len(data):.2%}")


"""MLP ep=0, loss=0.87179664, train_acc=87.75%
epoch 1
MLP ep=1, loss=0.00045968, train_acc=100.00%
epoch 2
MLP ep=2, loss=0.00058176, train_acc=100.00%
epoch 3
MLP ep=3, loss=0.00066816, train_acc=100.00%
epoch 4
MLP ep=4, loss=0.00068180, train_acc=100.00%
epoch 5
MLP ep=5, loss=0.00058149, train_acc=100.00%
epoch 6
MLP ep=6, loss=0.00043910, train_acc=100.00%
epoch 7
MLP ep=7, loss=0.00031280, train_acc=100.00%
epoch 8"""