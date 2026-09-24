# Here we will write functions for converting geometric information (meshes) into input data understandable for popular neural network architectures
# Writed on base of OCSSN ; link=https://github.com/kaifczxc-lab/OCSSN

import torch
from collections import defaultdict
from collections import Counter
import random
import PySimplicial.utils as ps

class Converters:
    def relabel(self, simplices):
        """
        Renumber vertices of a triangle mesh to consecutive integers starting from 0

        Parameters
        ----------

        figure: list of tuple
            list of tuple with form of (a,b,c) or (a,b,c,d) ; anything else right now unsupported
        
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
        n_figure = []
        map = {}
        if not simplices:
            raise ValueError("ValueError: here's not figure")
        if len(simplices[0]) == 3:
            for a,b,c in simplices:
                for v in (a,b,c):
                    if v not in map:
                        map[v] = len(map)
                n_figure.append((map[a], map[b], map[c]))
        elif len(simplices[0]) == 4:
            for a,b,c,d in simplices:
                for v in (a,b,c,d):
                    if v not in map:
                        map[v] = len(map)
                n_figure.append((map[a], map[b], map[c], map[d]))
        else:
            raise ValueError("ValueError: the list of tuple with form of more than (a,b,c,d) are unsupported right now")
        return n_figure
    
    def to_gnn(self, simplices):
        """
        Here we calculate the matrix from all vertices of tris-mesh, sum it and return:

        Parameters
        ----------
        
        figure: list of tuple
            list in form of (a,b,c) or (a,b,c,d) ; anything else are unsupported right now

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

        """
        if not simplices:
            raise ValueError("ValueError: tris must not be empty")
        if len(simplices[0]) == 3:
            tris = self.relabel(simplices) # we make it so that the difference between the vertices in the list is not so big (let's say like [1,49])
            num_nodes = max(max(t) for t in tris) + 1 
            A = torch.zeros((num_nodes, num_nodes))
            for (u,v,w) in tris:
                A[u,v]=A[v,u]=1.0; A[v,w]=A[w,v]=1.0; A[u,w]=A[w,u]=1.0 # fixed A[u,w]=1.0 to A[u,w]=A[w,u]=1.0
        elif len(simplices[0]) == 4:
            tetrahedron = self.relabel(simplices)
            num_nodes = max(max(t) for t in tetrahedron) + 1
            A = torch.zeros((num_nodes, num_nodes))
            for (a,b,c,d) in tetrahedron:
                A[a,b]=A[b,a]=1.0 ; A[a,c]=A[c,a]=1.0 ; A[a,d]=A[d,a]=1.0;A[b,c]=A[c,b]=1.0 ; A[b,d]=A[d,b]=1.0;A[c,d]=A[d,c]=1.0
        else:
            raise ValueError("ValueError: right now the list of tuple as a figure in form of more than (a,b,c,d) are not supported")
        s = A.sum()
        degree = (A.sum(dim=1, keepdim=True) / (s + 1e-8))
        L = torch.cat([degree, torch.ones(num_nodes, 1)], dim=1)
        if torch.equal(A, A.T) == False:
            print(f"warning, torch.equal(A, A.T) is false")    
        return A / (s + 1e-8), L
    def to_tnn(self, simplices, N):
        """
        Here we calculate the symmetric normalized adjacency matrix from tris-mesh data

        Parameters
        ----------

        figure: list of tuple
            list in form of (a,b,c) or (a,b,c,d) ; anything else are unsupported right now
        
        N: int
            torch.zeros matrix N x N

        Returns
        -------

        torch.Tensor:
            Normalized adjacency matrix of shape 

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
        """
        if not simplices:
            raise ValueError("ValueError: figure must not be empty")
        
        if len(simplices[0]) == 3:
            tris = self.relabel(simplices)
            A = torch.zeros((N,N))
            for (u,v,w) in tris:
                A[u,v]=A[v,u]=1.0; A[v,w]=A[w,v]=1.0; A[u,w]=A[w,u]=1.0

        elif len(simplices[0]) == 4:
            tetrahedron = self.relabel(simplices)
            A = torch.zeros((N,N))
            for (a,b,c,d) in tetrahedron:
                A[a,b]=A[b,a]=1.0 ; A[a,c]=A[c,a]=1.0 ; A[a,d]=A[d,a]=1.0;A[b,c]=A[c,b]=1.0 ; A[b,d]=A[d,b]=1.0;A[c,d]=A[d,c]=1.0

        else:
            raise ValueError("ValueError: right now the list of tuple as a figure in form of more than (a,b,c,d) are not supported")
        
        deg = A.sum(dim=1)
        deg1 = torch.where(deg > 0, deg.pow(-0.5), torch.zeros_like(deg))
        D = torch.diag(deg1)
        A_norm = D @ A @ D 
        return A_norm


    def to_mlp(self, simplices, return_chi=True):
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

        Parameters
        ----------

        figure: list of tuple

            list in form of (a,b,c) or (a,b,c,d) ; anything else are unsupported right now

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

        ---

        >>> relabel = [(0, 1, 2, 3), (4, 1, 2, 3), (4, 0, 2, 3), (4, 0, 1, 3), (4, 0, 1, 2)]
        >>> converter_MLP = PySimplicial.utils.converter_for_mlp(relabel, return_chi=True)
        >>> print("CONVERTED MLP")
        >>> print(converter_MLP)
        CONVERTED MLP
        (10, 5, 10, 0, 0, 5, 0, 0, 4.0, 2.0)
        """
        if not simplices:
            raise ValueError("ValueError: figure must not be empty")
        T = len(simplices)
        vert = set() # guarantees no duplicates
        edges = set()
        faces=set()
        vertice_neighbors = defaultdict(set)
        if len(simplices[0]) == 3:
            F = len(simplices)
            for (a,b,c) in simplices: # calculate V
                vert.add(a)
                vert.add(b)
                vert.add(c)
            V = len(vert) 
            for (a,b,c) in simplices: # calculate E
                # if 2 triangles share one edge ; Example. Upper: 1-2 & Lower: 2-1 ; They will be written in edges as (1,2) 
                edges.add(tuple(sorted((a,b)))) # About python base: tuple() is list ensures that it cannot be modified after creation ; sorted(()) sorts values ​​in ascending order
                edges.add(tuple(sorted((b,c))))
                edges.add(tuple(sorted((a,c))))
            E = len(edges)
            chi = (2 - (V-E+F)) // 2
            for (a,b,c) in simplices:
                vertice_neighbors[a].update([b,c])
                vertice_neighbors[b].update([a,c])
                vertice_neighbors[c].update([a,b])
        elif len(simplices[0]) == 4:
            for (a,b,c,d) in simplices: # calculate V
                vert.add(a)
                vert.add(b)
                vert.add(c)
                vert.add(d)
            V = len(vert) 
            for (a,b,c,d) in simplices: # calculate E
                # if 2 triangles share one edge ; Example. Upper: 1-2 & Lower: 2-1 ; They will be written in edges as (1,2) 
                edges.add(tuple(sorted((a,b))))
                edges.add(tuple(sorted((a,c))))
                edges.add(tuple(sorted((a,d))))
                edges.add(tuple(sorted((b,c))))
                edges.add(tuple(sorted((b,d)))) 
                edges.add(tuple(sorted((c,d))))
            E = len(edges) 
            for (a,b,c,d) in simplices:
                faces.add(tuple(sorted((a,b,c))))
                faces.add(tuple(sorted((a,b,d))))
                faces.add(tuple(sorted((a,c,d))))
                faces.add(tuple(sorted((b,c,d))))
            F = len(faces)
            chi = V-E+F-T
            for (a,b,c,d) in simplices:
                vertice_neighbors[a].update([b,c,d])
                vertice_neighbors[b].update([a,c,d])
                vertice_neighbors[c].update([a,b,d])
                vertice_neighbors[d].update([a,b,c])
        else:
            raise ValueError("ValueError: right now the list of tuple as a figure in form of more than (a,b,c,d) are not supported")
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
        avg_degree = 2 * E / V
        tpv = F / V
        if return_chi:
            return F, V, E, chi, bins[0], bins[1], bins[2], bins[3], avg_degree, tpv
        else:
            return F, V, E, bins[0], bins[1], bins[2], bins[3], avg_degree, tpv





def chain_2D(base, label, K, p_13=0.35, p_22=0.55, p_31=0.10, return_stats=True):
    """
    chain is the one of the most important slice of dataset generation
    
    in foundation of this function we have Markov chain algorithm: 
    
    P(X_n+1 = x_n+1 | X_n = x_n, X_n-1 = x_n-1, ... , X_0 = x_0) = P(X_n+1 = x_n+1 | X_n = x_n)
    
    This algorithm models transitions from one state to another

    The sum of all Pachner Moves chances must not exceed 1

    Parameters
    ----------

    base: list of tuple
        Figure (torus, triangle)
    
    label: int
        The genus of figure

        out.append((current, label)) (where current - figure with using pachner move and label is id of this figure)

    K: int
        Amount of figure's what you want to be returned
    
    p_13: int
        Chance of pachner move 1-3 (NEED TO BE 0.0-1.0)
    
    p_31: int
        Chance of pachner move 3-1 (NEED TO BE 0.0-1.0)
    
    p_22: int
        Chance of pachner move 2-2 (NEED TO BE 0.0-1.0)

    return_stats: boolean
        Calculates how much pachner moves of all type's has been done by this function
        if true: return out, stats_1_3, stats_2_2, stats_3_1
        if false: return out 

    Returns
    -------

    out: list of tuple
        Generated dataset with K amount of figure's with different Pachner Moves
    """
    out = []
    current = base
    expected_genus = ps.euler_characteristics(current) # lock genus at start
    stats_1_3, stats_2_2, stats_3_1 = 0, 0, 0
    for _ in range(K):
        r = random.random()
        if r < p_13:
            candidate = ps.move_1_3(current)
            stats_1_3 += 1
        elif r < p_13 + p_31:
            candidate = ps.move_3_1(current)
            stats_3_1 += 1
            if candidate is None:
                candidate = ps.move_2_2(current)
                stats_2_2 += 1
        elif r < p_13 + p_31 + p_22:
            candidate = ps.move_2_2(current)
            stats_2_2 += 1
        if ps.euler_characteristics(candidate) == expected_genus:
            current = candidate
        out.append((current, label))
    if return_stats:
        return out, stats_1_3, stats_2_2, stats_3_1
    else:
        return out

def chain_3D(base, label, K, p_14 = 0.25, p_41=0.15, p_32=0.40, p_23=0.20, return_stats=True):
    """
    chain is the one of the most important slice of dataset generation
    
    in foundation of this function we have Markov chain algorithm: 
    
    P(X_n+1 = x_n+1 | X_n = x_n, X_n-1 = x_n-1, ... , X_0 = x_0) = P(X_n+1 = x_n+1 | X_n = x_n)
    
    This algorithm models transitions from one state to another

    The sum of all Pachner Moves chances must not exceed 1

    Parameters
    ----------

    base: list of tuple
        Figure (torus, triangle)
    
    label: int
        The genus of figure

        out.append((current, label)) (where current - figure with using pachner move and label is id of this figure)

    K: int
        Amount of figure's what you want to be returned
    
    p_14: int
        Chance of pachner move 1-4 (NEED TO BE 0.0-1.0)
    
    p_41: int
        Chance of pachner move 4-1 (NEED TO BE 0.0-1.0)
    
    p_23: int
        Chance of pachner move 2-3 (NEED TO BE 0.0-1.0)

    p_32: int
        Chance of pachner move 3-2 (NEED TO BE 0.0-1.0)

    return_stats: boolean
        Calculates how much pachner moves of all type's has been done by this function
        if true: return out, stats_1_3, stats_2_2, stats_3_1
        if false: return out 

    Returns
    -------
    
    out: list of tuple
        Generated dataset with K amount of figure's with different Pachner Moves
    """
    out = []
    current = base
    expected_connected_components = ps.euler_characteristics(current)
    stats_1_4, stats_4_1, stats_2_3, stats_3_2 = 0, 0, 0, 0
    for _ in range(K):
        r = random.random()
        if r < p_14:
            candidate = ps.move_1_4(current)
            stats_1_4 += 1
        elif r < p_14 + p_41:
            candidate = ps.move_4_1(current)
            stats_4_1 += 1
            if candidate is None:
                candidate = ps.move_1_4(current)
                stats_1_4 += 1
        elif r < p_14 + p_41 + p_23:
            candidate = ps.move_2_3(current)
            stats_2_3 += 1
        elif r < p_14 + p_41 + p_23 + p_32:
            candidate = ps.move_3_2(current)
            stats_3_2 += 1
            if candidate is None:
                candidate = ps.move_2_3(current)
                stats_2_3 += 1
            if ps.euler_characteristics(candidate) == expected_connected_components:
                current = candidate 
            out.append((current, label))
    if return_stats:
        return out, stats_1_4, stats_4_1, stats_2_3, stats_3_2 
    else:
        return out