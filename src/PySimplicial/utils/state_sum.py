import opt_einsum
import numpy as np


def state_sum(C, b_inv, v_p, g_edges, open_ports=(), type="2D"): # pass values from graph() and C (c3) and b_inv

    """
    This function deserves a separate discussion:

    it implements convolution over triangulation, but by itself does not guarantee topological invariance. Invariance depends on the tensors C and b_inv, which in the trained version may not satisfy the Frobenius axioms. That is, for the correct result you need a fixed Frobenius algebra
    
    More information can be found in https://github.com/kaifczxc-lab/OCSSN (the description of each parameter is quite complex and sometimes heavily depends on the context)

    type == "2D" State-sum for triangles
    
    type == "3D" State-sum for tetrahedrons

    Returns
    -------

    torch.Tensor or numpy.ndarray
        Result of the state-sum contraction where rank equals the number of open ports

        
    Examples
    --------

    >>> C = np.array([[[1.,0.],[0.,1.]],[[0.,1.],[1.,0.]]])
    >>> b_inv = np.array([[1.,0.],[0.,1.]])
    >>> before = state_sum(C, b_inv, [(0,1,2),(3,4,5)], [(0,3),(1,4),(2,5)], ())
    >>> after = state_sum(C, b_inv, [(0,1,2),(3,4,5)], [(0,4),(1,3),(2,5)], ())
    >>> print(before, after, np.isclose(before, after))
    4.0 4.0 True
    """
    if type == "2D":
        ops = [] # main list for opt_einsum, here we will add all arguments
        for (a,b,c) in v_p: # as example let take v_p = [(0,1,2),(3,4,5)]
            ops += [C, (a,b,c)] # for every unique port ID lets compare the index =>
            # => (t0,t1,t2,t3,t4,t5) => ops += [C, (0,1,2)] => C_t0,t1,t2 ; ops += [C,(3,4,5)] => C_t3,t4,t5 ; C_a,b,c for each triangle
        for (x,y) in g_edges: # g_edges=[1,5]
            ops += [b_inv, (x,y)] # b_inv = (B^-1)_t1,t5
        ops += [tuple(open_ports)] # open_ports=[0,2,3,4]
        # After all: Z_T0 = sum_t1,t2,t3,t4,t5 C_t0,t1,t2 * C_t3,t4,t5 * (B^-1)_t1,t5
        return opt_einsum.contract(*ops, optimize="greedy") # opt_einsum its just better version of basic einsum, it searches the best way to sum huge values
    elif type == "3D":
        # 3d is experimental because we have questions about the math part
        ops = []
        for (a,b,c,d) in v_p:
            ops += [C, (a,b,c,d)]
        for (x,y,z) in g_edges:
            ops += [b_inv, (x,y,z)]
        ops += [tuple(open_ports)]
        return opt_einsum.contract(*ops, optimize="greedy")

# Conceptually, this is a rather confusing function in the entire code (it transforms mesh geometry into a combinatorial for tensor network), so I will add a more extensive amount of explanation here, I tried to make it as clear as I could
def graph(figure, type="2D"):
    """
    A helper function for state-sum that can calculate the number of open ports / vertice ports / glued edges

    Parameters
    ----------

    figure: list of tuple
        Tetrahedrons/Triangles mesh list
    
    type: str
        type="2D" for triangles, 3 vertices in list, example: [(0,1,2), (0,2,3), (0,3,4), (0,4,1),(5,2,1), (5,3,2), (5,4,3), (5,1,4)]

        type="3D" for tetrahedrons, 4 vertices in list, example: [(0, 1, 2, 3),(0, 1, 2, 4)]

    Returns
    -------

    v_p: list of tuple
        vertice ports

    g_edges: list of tuple
        glued edges

    open_ports: list of tuple
        external unconnected ends of the network
    
    Examples
    --------

    >>> triangles = [(0, 1, 2), (0, 2, 3)]
    >>> v_p, g_edges, open_ports = ps.graph(triangles, type="2D")
    >>> print("v_p: ", v_p)
    >>> print("g_edges: ", g_edges)
    >>> print("open_ports: ", open_ports)
    >>> tetrahedrons = [(0, 1, 2, 3),(0, 1, 2, 4)]
    >>> v_p_3D, g_edges_3D, open_ports_3D = ps.graph(tetrahedrons, type="3D")
    >>> print("v_p_3D: ", v_p_3D)
    >>> print("g_edges_3D: ", g_edges_3D)
    >>> print("open_ports_3D: ", open_ports_3D)
    v_p:  [(0, 1, 2), (3, 4, 5)]
    g_edges:  [(2, 3)]
    open_ports:  [0, 1, 4, 5]
    v_p_3D:  [(0, 1, 2, 3), (4, 5, 6, 7)]
    g_edges_3D:  [(0, 4)]
    open_ports_3D:  [1, 2, 3, 5, 6, 7]
    
    """
    slot = {} # dictionary who will contain unique ID for every port
    def sid(t,e):
        if (t,e) not in slot:
            slot[(t,e)] = len(slot)
        return slot[(t,e)] 
        # sid() is function for generation a lot of unique ID's, t = triangle number, e = this triangle edge
        # if this both are first time here then we give to it an ordinal number equal to the current length of the dictionary (len(slot), like 0,1,2,3,4,5...
        # this gives us the condition that if two triangles share one edge, they will store a unique port ID for it
    if type == "2D":
        v_p = [] # vertices ports, list of 3 triangles ID's 
        e_slots = {} # here we will store the connection of vertices
        # on numbered triangles, we sort their 3 edges, all this needed for make edge (2,1) and edge (1,2) similar
        for t, (a,b,c) in enumerate(figure):
            eab = tuple(sorted((a,b)))
            ebc = tuple(sorted((b,c)))
            eac = tuple(sorted((a,c)))
            s0,s1,s2 = sid(t,eab), sid(t, ebc), sid(t, eac) # generation 3 unique port ID's for current triangle t
            v_p.append((s0,s1,s2)) # add this 3 ports in v_p and we gonna know that fact the triangle t are manage indexes s0,s1,s2
            # If edge eab is internal, then e_slots[eab] will contain two ID's: the port from the first triangle and the port from the second triangle
            e_slots.setdefault(eab,[]).append(s0)
            e_slots.setdefault(ebc,[]).append(s1)
            e_slots.setdefault(eac,[]).append(s2) 
        g_edges, open_ports = [], []
        for s in e_slots.values():
            if len(s) == 2: # 2 ports of different triangles
                g_edges.append((s[0], s[1]))
            else: # if we have more or less than 2 ports
                open_ports += s # we just send it into free lists
        return v_p, g_edges, open_ports
    elif type == "3D":
        v_p = []
        e_slots = {}
        for t, (a,b,c,d) in enumerate(figure):
            eabc = tuple(sorted((a,b,c)))
            eabd = tuple(sorted((a,b,d)))
            eacd = tuple(sorted((a,c,d)))
            ebcd = tuple(sorted((b,c,d)))
            s0,s1,s2,s3 = sid(t,eabc), sid(t,eabd), sid(t,eacd), sid(t, ebcd)
            v_p.append((s0,s1,s2,s3))
            e_slots.setdefault(eabc, []).append(s0)
            e_slots.setdefault(eabd, []).append(s1)
            e_slots.setdefault(eacd, []).append(s2)
            e_slots.setdefault(ebcd, []).append(s3)
        g_edges, open_ports = [], []
        for s in e_slots.values():
            if len(s) == 2:
                g_edges.append((s[0], s[1]))
            else:
                open_ports += s 
        return v_p, g_edges, open_ports

