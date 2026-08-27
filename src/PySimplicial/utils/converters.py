# Here we will write functions for converting geometric information (meshes) into input data understandable for popular neural network architectures
# Writed on base of OCSSN ; link=https://github.com/kaifczxc-lab/OCSSN

import torch
from collections import defaultdict

def relabel(tris):
    """
    Renumber vertices of a triangle mesh to consecutive integers starting from 0

    Parameters
    ----------

    tris: list
        Triangle mesh list
    
    Returns
    -------

    list of tuple:
        Renumbered triangle mesh list

    Examples
    --------

    >>> octahedron_ = [(0,10,20), (0,20,30), (0,30,40), (0,40,10),(50,20,10), (50,30,20), (50,40,30), (50,10,40)]
    >>> octahedron_relabeled = PySimplicial.utils.relabel(octahedron_)
    >>> print(f"Octahedron={octahedron_relabeled}")
    Octahedron=[(0, 1, 2), (0, 2, 3), (0, 3, 4), (0, 4, 1), (5, 2, 1), (5, 3, 2), (5, 4, 3), (5, 1, 4)]
    """

    map = {}
    n_tris = []
    for a,b,c in tris:
        for v in (a,b,c):
            if v not in map:
                map[v] = len(map)
        n_tris.append((map[a], map[b], map[c]))
    return n_tris

def converter_for_gnn(tris):
    """
    Here we calculate the matrix from all vertices of tris-mesh, sum it and return:

    Parameters
    ----------
    
    tris: list
        Triangle mesh list

    Returns
    -------

    torch.Tensor:
        Normalized adjacency matrix of shape
        
        A / (s + 1e-8)

    torch.Tensor:
        Node feature matrix of shape

        L

    Notes
    -----

    num_nodes = max(max(t) for t in tris)

    A = torch.zeros((num_nodes, num_nodes))
    
    L = torch.cat([degree, torch.ones(num_nodes, 1)], dim=1
    s = A.sum()

    Examples
    --------

    >>> relabel_ = [(0, 1, 2), (0, 2, 3), (0, 3, 4), (0, 4, 1), (5, 2, 1), (5, 3, 2), (5, 4, 3), (5, 1, 4)]
    >>> converter_GNN_2D = PySimplicial.utils.converter_for_gnn(relabel_)
    >>> print("CONVERTER GNN")
    >>> print(converter_GNN_2D)
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

    """
    tris = relabel(tris) # we make it so that the difference between the vertices in the list is not so big (let's say like [1,49])
    num_nodes = max(max(t) for t in tris) + 1 
    A = torch.zeros((num_nodes, num_nodes))
    for (u,v,w) in tris:
        A[u,v]=A[v,u]=1.0; A[v,w]=A[w,v]=1.0; A[u,w]=1.0
    s = A.sum()
    degree = (A.sum(dim=1, keepdim=True) / (s + 1e-8))
    L = torch.cat([degree, torch.ones(num_nodes, 1)], dim=1)
    return A / (s + 1e-8), L

def converter_for_tnn(tris, N):
    """
    Here we calculate the symmetric normalized adjacency matrix from tris-mesh data

    Parameters
    ----------

    tris: list
        Triangle mesh list
    
    N: int
        torch.zeros matrix N x N

    Returns
    -------

    torch.Tensor:
        Normalized adjacency matrix of shape 

    Examples
    --------

    >>> relabel_ = [(0, 1, 2), (0, 2, 3), (0, 3, 4), (0, 4, 1), (5, 2, 1), (5, 3, 2), (5, 4, 3), (5, 1, 4)]
    >>> converter_TNN_2D = PySimplicial.utils.converter_for_tnn(relabel_, 6)
    >>> print("CONVERTER TNN")
    >>> print(converter_TNN_2D)
    CONVERTER TNN
    tensor([[0.0000, 0.2500, 0.2500, 0.2500, 0.2500, 0.0000],
        [0.2500, 0.0000, 0.2500, 0.0000, 0.2500, 0.2500],
        [0.2500, 0.2500, 0.0000, 0.2500, 0.0000, 0.2500],
        [0.2500, 0.0000, 0.2500, 0.0000, 0.2500, 0.2500],
        [0.2500, 0.2500, 0.0000, 0.2500, 0.0000, 0.2500],
        [0.0000, 0.2500, 0.2500, 0.2500, 0.2500, 0.0000]])

    """
    tris = relabel(tris)
    A = torch.zeros((N,N))
    for (u,v,w) in tris:
        A[u,v]=A[v,u]=1.0; A[v,w]=A[w,v]=1.0; A[u,w]=A[w,u]=1.0
    deg = A.sum(dim=1)
    deg1 = torch.where(deg > 0, deg.pow(-0.5), torch.zeros_like(deg))
    D = torch.diag(deg1)
    A_norm = D @ A @ D 
    return A_norm

def converter_for_mlp(tris, return_g=False):
    """
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

    Return
    ------

    if return_g=True => return F, V, E, g, bins[0], bins[1], bins[2], bins[3], avg_degree, tpv

    else: return F, V, E, bins[0], bins[1], bins[2], bins[3], avg_degree, tpv

    Examples
    --------

    >>> relabel_ = [(0, 1, 2), (0, 2, 3), (0, 3, 4), (0, 4, 1), (5, 2, 1), (5, 3, 2), (5, 4, 3), (5, 1, 4)]
    >>> converter_MLP_2D = PySimplicial.utils.converter_for_mlp(relabel_, return_g=True)
    >>> print("CONVERTED MLP")
    >>> print(converter_MLP_2D)
    CONVERTED MLP
    (8, 6, 12, 0, 0, 6, 0, 0, 4.0, 1.3333333333333333)
    """

    F = len(tris) # In example of octahedron: F=8
    vert = set() # set() guarantees no duplicates
    for (a,b,c) in tris: # calculate V
        vert.add(a)
        vert.add(b)
        vert.add(c)
    V = len(vert) # In example of octahedron: V=6 
    edges = set()
    for (a,b,c) in tris: # calculate E
        # if 2 triangles share one edge ; Example. Upper: 1-2 & Lower: 2-1 ; They will be written in edges as (1,2) 
        edges.add(tuple(sorted((a,b)))) # About python base: tuple() is list ensures that it cannot be modified after creation ; sorted(()) sorts values ​​in ascending order
        edges.add(tuple(sorted((b,c))))
        edges.add(tuple(sorted((a,c))))
    E = len(edges) # In example of octahedron: E=12
    g = (2 - (V-E+F)) // 2 # Pick our values: 6 - 12 + 8 = 2 ==> 2 - 2 = 0 // 2 ==> g = 0 
    avg_degree = 2 * E / V
    tpv = F / V
    vertice_neighbors = defaultdict(set)
    for (a,b,c) in tris:
        vertice_neighbors[a].update([b,c])
        vertice_neighbors[b].update([a,c])
        vertice_neighbors[c].update([a,b])
    deg = [len(vertice_neighbors[v]) for v in vertice_neighbors]
    bins = [0] * 4
    for a in deg:
        if a <= 3:
            bins[0] += 1
        elif a <= 5:
            bins[1] += 1
        elif a <= 7:
            bins[2] += 1
        else:
            bins[3] += 1
    if return_g:
        return F, V, E, g, bins[0], bins[1], bins[2], bins[3], avg_degree, tpv
    else:
        return F, V, E, bins[0], bins[1], bins[2], bins[3], avg_degree, tpv


def relabel_3D(tetrahedron):
    """
    Renumber vertices of a tetrahedrons mesh to consecutive integers starting from 0

    Parameters
    ----------

    tetrahedron: list
        Tetrahedrons mesh list
    
    Returns
    -------

    list of tuple:
        Renumbered tetrahedrons mesh list
    
    Examples
    --------

    >>> tetrahedron_for_relabel = [(100,200,300,400),(0,200,300,400),(0,100,300,400),(0,100,200,400),(0,100,200,300)]
    >>> relabel_3D_ = PySimplicial.utils.relabel_3D(tetrahedron_for_relabel)
    >>> print("RELABEL 3D")
    >>> print(relabel_3D_)
    RELABEL 3D
    [(0, 1, 2, 3), (4, 1, 2, 3), (4, 0, 2, 3), (4, 0, 1, 3), (4, 0, 1, 2)]
    """
    map = {}
    n_tetrahedron = []
    for a,b,c,d in tetrahedron:
        for v in (a,b,c,d):
            if v not in map:
                map[v] = len(map)
        n_tetrahedron.append((map[a], map[b], map[c], map[d]))
    return n_tetrahedron


def converter_for_gnn_3D(tetrahedron):
    """
    Here we calculate the matrix from all vertices of tetrahedron-mesh, sum it and return:

    Parameters
    ----------
    
    tetrahedron: list
        tetrahedron mesh list

    Returns
    -------

    torch.Tensor:
        Normalized adjacency matrix of shape
        
        A / (s + 1e-8)

    torch.Tensor:
        Node feature matrix of shape

        L

    Notes
    -----

    num_nodes = max(max(t) for t in tetrahedron)

    A = torch.zeros((num_nodes, num_nodes))
    
    L = torch.cat([degree, torch.ones(num_nodes, 1)], dim=1

    s = A.sum()

    Examples
    --------

    >>> relabel_3D_ = [(0, 1, 2, 3), (4, 1, 2, 3), (4, 0, 2, 3), (4, 0, 1, 3), (4, 0, 1, 2)]
    >>> converter_GNN_3D = PySimplicial.utils.converter_for_gnn_3D(relabel_3D_)
    >>> print("CONVERTER GNN 3D")
    >>> print(converter_GNN_3D)
    CONVERTER GNN 3D
    (tensor([[0.0000, 0.0500, 0.0500, 0.0500, 0.0500],
            [0.0500, 0.0000, 0.0500, 0.0500, 0.0500],
            [0.0500, 0.0500, 0.0000, 0.0500, 0.0500],
            [0.0500, 0.0500, 0.0500, 0.0000, 0.0500],
            [0.0500, 0.0500, 0.0500, 0.0500, 0.0000]]), tensor([[0.2000, 1.0000],
            [0.2000, 1.0000],
            [0.2000, 1.0000],
            [0.2000, 1.0000],
            [0.2000, 1.0000]]))


    """
    tetrahedron = relabel_3D(tetrahedron)
    num_nodes = max(max(t) for t in tetrahedron) + 1
    A = torch.zeros((num_nodes, num_nodes))
    for (a,b,c,d) in tetrahedron:
        A[a,b]=A[b,a]=1.0 ; A[a,c]=A[c,a]=1.0 ; A[a,d]=A[d,a]=1.0;A[b,c]=A[c,b]=1.0 ; A[b,d]=A[d,b]=1.0;A[c,d]=A[d,c]=1.0
    s = A.sum()
    degree = (A.sum(dim=1, keepdim=True) / (s + 1e-8))
    L = torch.cat([degree, torch.ones(num_nodes, 1)], dim=1)
    return A / (s + 1e-8), L


def converter_for_tnn_3D(tetrahedron, N):
    """
    Here we calculate the symmetric normalized adjacency matrix from tetrahedron-mesh data

    Parameters
    ----------

    tetrahedron: list
        Tetrahedrons mesh list
    
    N: int
        torch.zeros matrix N x N

    Returns
    -------

    torch.Tensor:
        Normalized adjacency matrix of shape 

    Examples
    --------
    >>> relabel_3D_ = [(0, 1, 2, 3), (4, 1, 2, 3), (4, 0, 2, 3), (4, 0, 1, 3), (4, 0, 1, 2)]
    >>> converter_TNN_3D = PySimplicial.utils.converter_for_tnn_3D(relabel_3D_, 6)
    >>> print("CONVERTER TNN 3D")
    >>> print(converter_TNN_3D)
    CONVERTER TNN 3D
    tensor([[0.0000, 0.2500, 0.2500, 0.2500, 0.2500, 0.0000],
            [0.2500, 0.0000, 0.2500, 0.2500, 0.2500, 0.0000],
            [0.2500, 0.2500, 0.0000, 0.2500, 0.2500, 0.0000],
            [0.2500, 0.2500, 0.2500, 0.0000, 0.2500, 0.0000],
            [0.2500, 0.2500, 0.2500, 0.2500, 0.0000, 0.0000],
            [0.0000, 0.0000, 0.0000, 0.0000, 0.0000, 0.0000]])

    """
    tetrahedron = relabel_3D(tetrahedron)
    A = torch.zeros((N,N))
    for (a,b,c,d) in tetrahedron:
        A[a,b]=A[b,a]=1.0 ; A[a,c]=A[c,a]=1.0 ; A[a,d]=A[d,a]=1.0;A[b,c]=A[c,b]=1.0 ; A[b,d]=A[d,b]=1.0;A[c,d]=A[d,c]=1.0
    deg = A.sum(dim=1)
    deg1 = torch.where(deg > 0, deg.pow(-0.5), torch.zeros_like(deg))
    D = torch.diag(deg1)
    A_norm = D @ A @ D 
    return A_norm

def converter_for_mlp_3D(tetrahedron, return_x=False):
    """
    Here we calculate the Histogram of vertex degrees, euler's characteristics, tetrahedron_per_vertex (F / V) and average deegree number

    Histogram of verted degrees algorithm: 
        
        >>> get the degree count for every node in tetrahedron

        >>> count how many nodes share each degree value
    
    Euler's Charactertic formula (2D):

        >>> V = unique vertices, E = unique edges, F = number of faces, g = surface genus

        >>> x = V - E + F = 2 - 2g
    
    Calculating tetrahedron_per_vertex:

        >>> Number of faces / unique vertices

    Calculating average degree:

        >>> 2 * unique edges / unique vertices

    Return
    -------

    if return_x true => return F, V, E, x, bins[0], bins[1], bins[2], bins[3], avg_degree, tpv

    else: return F, V, E, bins[0], bins[1], bins[2], bins[3], avg_degree, tpv

    Examples
    --------
    >>> relabel_3D_ = [(0, 1, 2, 3), (4, 1, 2, 3), (4, 0, 2, 3), (4, 0, 1, 3), (4, 0, 1, 2)]
    >>> converter_MLP_3D = PySimplicial.utils.converter_for_mlp_3D(relabel_3D_, return_x=True)
    >>> print("CONVERTED MLP 3D")
    >>> print(converter_MLP_3D)
    CONVERTED MLP 3D
    (10, 5, 10, 0, 0, 5, 0, 0, 4.0, 2.0)
    """
    T = len(tetrahedron)
    # In example of octahedron: F=8
    vert = set() # set() guarantees no duplicates
    for (a,b,c,d) in tetrahedron: # calculate V
        vert.add(a)
        vert.add(b)
        vert.add(c)
        vert.add(d)
    V = len(vert) # In example of octahedron: V=6 
    edges = set()
    for (a,b,c,d) in tetrahedron: # calculate E
        # if 2 triangles share one edge ; Example. Upper: 1-2 & Lower: 2-1 ; They will be written in edges as (1,2) 
        edges.add(tuple(sorted((a,b)))), 
        edges.add(tuple(sorted((a,c)))), 
        edges.add(tuple(sorted((a,d)))), 
        edges.add(tuple(sorted((b,c)))),
        edges.add(tuple(sorted((b,d)))), 
        edges.add(tuple(sorted((c,d))))
    E = len(edges) # In example of octahedron: E=12
    faces=set()
    for (a,b,c,d) in tetrahedron:
        faces.add(tuple(sorted((a,b,c))))
        faces.add(tuple(sorted((a,b,d))))
        faces.add(tuple(sorted((a,c,d))))
        faces.add(tuple(sorted((b,c,d))))

    F = len(faces)
    x = V-E+F-T # Pick our values: 6 - 12 + 8 = 2 ==> 2 - 2 = 0 // 2 ==> g = 0 
    avg_degree = 2 * E / V
    tpv = F / V
    vertice_neighbors = defaultdict(set)
    for (a,b,c,d) in tetrahedron:
        vertice_neighbors[a].update([b,c,d])
        vertice_neighbors[b].update([a,c,d])
        vertice_neighbors[c].update([a,b,d])
        vertice_neighbors[d].update([a,b,c])
    deg = [len(vertice_neighbors[v]) for v in vertice_neighbors]
    bins = [0] * 4
    for a in deg:
        if a <= 3:
            bins[0] += 1
        elif a <= 5:
            bins[1] += 1
        elif a <= 7:
            bins[2] += 1
        else:
            bins[3] += 1
    if return_x:
        return F, V, E, x, bins[0], bins[1], bins[2], bins[3], avg_degree, tpv
    else:
        return F, V, E, bins[0], bins[1], bins[2], bins[3], avg_degree, tpv
