from collections import defaultdict
import random    
from collections import Counter

def move_2_2(tris):
    """
    This function implements Pachner Move type 2-2

    The 2-2 move is applied to adjacent triangles connected by a common interior edge, forming a quadrilateral. The function replaces the common edge with the opposite diagonal of the quadrilateral, resulting in two new triangles covering the same area
    
    Parameters
    ----------

    tris: list of tuples of three ints
        Triangles mesh list

    Returns
    -------

    new_triangles: list of tuple
        tris but with 2-2 Pachner move

    tris: list of tuple
        If we couldn't find a candidate for a 2-2 Pachner move (=flip), then we return the original set, that is, we look for an edge that belongs to exactly two triangles (len(tris) == 2), this is the candidate for the flip, otherwise, we return the same figure

    
    Examples
    --------

    >>> Pachner_move_2_2 = move_2_2(octahedron)
    >>> print(f"Basic octahedron={octahedron}")
    >>> print(f"Pachner_move_2_2 Octahedron={Pachner_move_2_2}")
    Basic octahedron=[(0, 1, 2), (0, 2, 3), (0, 3, 4), (0, 4, 1), (5, 2, 1), (5, 3, 2), (5, 4, 3), (5, 1, 4)]
    Pachner_move_2_2 Octahedron=[(0, 1, 2), (0, 2, 3), (0, 4, 1), (5, 2, 1), (5, 3, 2), (5, 1, 4), (3, 0, 5), (0, 4, 5)]
    
    """
    # we need to construct a mapping : edge -> list of tris containing it
    ett = defaultdict(list) # edge to tris
    for idx, (a,b,c) in enumerate(tris): # first triangle: (0, (0,1,2)) ; second triangle: (1, (0,2,3))
        # for each triangle, we iterate over its three edges for ensure that the edges (a,b) and (b,a) are considered the same
        for edge in [tuple(sorted((a,b))), tuple(sorted((b,c))), tuple(sorted((a,c)))]:
            ett[edge].append(idx) # add the index of the current triangle to the list of triangles that own this edge
    exist=set(ett.keys()) # set of all exist edges ; it is necessary to check whether a new diagonal already exists
    # choose an edge that has exactly two tris
    inter=[e for e, tris in ett.items() if len(tris) == 2] # A move 2/2 can only be done on an edge that is adjacent to exactly two triangles
    random.shuffle(inter)
    #edge=random.choice(inter) # choose random
    for edge in inter:
        t1_idx,t2_idx=ett[edge]
        a,b = edge # a,b = end of this edge
        t1 = tris[t1_idx]
        t2 = tris[t2_idx]
        c = [v for v in t1 if v != a and v != b]
        d = [v for v in t2 if v != a and v != b]
        if not c or not d: # empty check
            continue
        c,d = c[0], d[0]
        new_edge=tuple(sorted((c,d)))
        if c==d or new_edge in exist:
            continue
        new_triangles = [t for i, t in enumerate(tris) if i != t1_idx and i != t2_idx] # all triangles except those with indices 0 and 1 will be empty []
        new_triangles.append((a,c,d))
        new_triangles.append((c,b,d))
        return new_triangles
    return tris

def move_1_3(tris):
    """
    This function implements Pachner Move type 1-3

    Divides the triangle into three smaller ones by connecting them with one common vertex (that is, to determine the correctness of the move 1-3, we must ensure that there is a new vertex and it is connected to the other 3)
    
    Parameters
    ----------

    tris: list of tuples of three ints
        Triangles mesh list

    Returns
    -------

    n_triangles: list of tuple
        New triangles mesh list with move 1-3

    Examples
    --------

    >>> Pachner_move_1_3 = PySimplicial.utils.move_1_3(octahedron)
    >>> print(f"Basic octahedron={octahedron}")
    >>> print(f"Octahedron with move 3-1={Pachner_move_1_3}")
    Basic octahedron=[(0, 1, 2), (0, 2, 3), (0, 3, 4), (0, 4, 1), (5, 2, 1), (5, 3, 2), (5, 4, 3), (5, 1, 4)]
    Octahedron with move 3-1=[(0, 1, 2), (0, 2, 3), (0, 3, 4), (0, 4, 1), (5, 2, 1), (5, 3, 2), (5, 4, 3), (5, 1, 6), (1, 4, 6), (5, 4, 6)]
    """
    index = random.randrange(len(tris))
    a,b,c = tris[index]
    n_v = max(max(t) for t in tris) + 1 # +1 gives guaranteed unique ID
    n_triangles = [t for i,t in enumerate(tris) if i != index]
    n_triangles += [(a,b,n_v), (b,c,n_v), (a,c,n_v)]
    return n_triangles 

def move_3_1(tris):
    """
    This function implements Pachner Move type 3-1

    The move 3-1 is the inverse of 1-3, removing an interior vertex of degree 3, surrounded by three triangles with no other elements attached to their faces, and combines them into a single triangle

    Parameters
    ----------

    tris: list of tuples of three ints
        Triangles mesh list

    Returns
    -------

    new_triangles: list of tuple
        Same triangles mesh list but with move 3-1

    Examples
    --------

    >>> Pachner_move_3_1 = PySimplicial.utils.move_3_1(Pachner_move_1_3)
    >>> print(f"Basic octahedron={octahedron}")
    >>> print(f"Octahedron with move 3-1={Pachner_move_3_1}")
    Basic octahedron=[(0, 1, 2), (0, 2, 3), (0, 3, 4), (0, 4, 1), (5, 2, 1), (5, 3, 2), (5, 4, 3), (5, 1, 4)]
    Octahedron with move 3-1=[(0, 1, 2), (0, 2, 3), (0, 3, 4), (0, 4, 1), (5, 2, 1), (5, 3, 2), (5, 4, 3), (5, 1, 4)]
    """
    e_count = Counter()
    for (a,b,c) in tris:
        for edge in [tuple(sorted((a,b))), tuple(sorted((b,c))), tuple(sorted((a,c)))]:
            e_count[edge] += 1
    vert_tris = defaultdict(list)
    for i, (a,b,c) in enumerate(tris):
        for v in (a,b,c):
            vert_tris[v].append(i)
    for v, incident in vert_tris.items():
        if len(incident) != 3:
            continue
        others = []
        for i in incident:
            a,b,c = tris[i]
            for u in (a,b,c):
                if u != v and u not in others:
                    others.append(u)
        if len(others) != 3:
            continue
        o1,o2,o3 = others
        new_tri = (o1,o2,o3)
        existing_edges = set(tuple(sorted((a,b))) for a,b,c in tris
                            for a,b in [(a,b), (b,c), (a,c)])
        if tuple(sorted((o1, o2))) in existing_edges and tuple(sorted((o2, o3))) in existing_edges and tuple(sorted((o1, o3))) in existing_edges:
            pass
        new_triangles = [t for i, t in enumerate(tris) if i not in incident]
        new_triangles.append(new_tri)
        return new_triangles
    return None

def move_1_4(tetrahedron):
    """
    This function implements Pachner Move type 1-4

    The Pachner move 1-4 divides one tetrahedron into four smaller tetrahedrons by introducing a new internal vertex. The boundary remains unchanged, but three edges and one vertex are added to the original tetrahedron

    Parameters
    ----------

    tetrahedron: list of tuples of four ints
        Tetrahedrons mesh list

    Returns
    -------

    n_triangles: list of tuple
        Same tetrahedrons mesh list but with move 1-4

    Examples
    --------
    >>> one_tetrahedron = [(0, 1, 2, 3)]
    >>> Pachner_move_1_4 = PySimplicial.utils.move_1_4(one_tetrahedron)
    >>> print(f"tetrahedron={one_tetrahedron}")
    >>> print(f"same tetrahedron but with move 1-4={Pachner_move_1_4}")
    tetrahedron=[(0, 1, 2, 3)]
    same tetrahedron but with move 1-4=[(0, 1, 2, 4), (0, 1, 3, 4), (0, 2, 3, 4), (1, 2, 3, 4)]
    
    """
    index = random.randrange(len(tetrahedron))
    a,b,c,d = tetrahedron[index]
    n_v = max(max(t) for t in tetrahedron) + 1 # +1 gives guaranteed unique ID
    n_triangles = [t for i,t in enumerate(tetrahedron) if i != index]
    n_triangles += [(a, b, c, n_v),(a, b, d, n_v),(a, c, d, n_v),(b, c, d, n_v)]
    return n_triangles 

def move_4_1(tetrahedron):
    """
    This function implements Pachner Move type 4-1

    Move 4-1 is the inverse of 1-4 and removes an internal vertex that is a common vertex of exactly four tetrahedra with no other internal simplices, collapsing them back into a single tetrahedron, thereby reducing the number of tetrahedra by three, removing one vertex and three edges
    
    Parameters
    ----------

    tetrahedron: list of tuples of four ints
        Tetrahedrons mesh list
    
    Returns
    -------

    new_triangles: list of tuple
        Same triangles mesh list but with move 4-1 (This move will work for you with 100% probability after using 1-4)

    Examples
    --------

    >>> one_tetrahedron = [(0, 1, 2, 3)]
    >>> Pachner_move_1_4 = PySimplicial.utils.move_1_4(one_tetrahedron)
    >>> Pachner_move_4_1 = PySimplicial.utils.move_4_1(Pachner_move_1_4)
    >>> print(f"Pachner_move_1_4={Pachner_move_1_4}")
    >>> print(f"Pachner_move_4_1={Pachner_move_4_1}")
    Pachner_move_1_4=[(0, 1, 2, 4), (0, 1, 3, 4), (0, 2, 3, 4), (1, 2, 3, 4)]
    Pachner_move_4_1=[(0, 1, 2, 3)]
    """
    vert_tetrahedron = defaultdict(list)
    for i, (a,b,c,d) in enumerate(tetrahedron):
        for v in (a,b,c,d):
            vert_tetrahedron[v].append(i)
    for v, incident in vert_tetrahedron.items():
        if len(incident) != 4:
            continue
        others = []
        for i in incident:
            a,b,c,d = tetrahedron[i]
            for u in (a,b,c,d):
                if u != v and u not in others:
                    others.append(u)
        if len(others) != 4:
            continue
        o1,o2,o3,o4 = others
        new_tetra = (o1,o2,o3,o4)
        new_triangles = [t for i, t in enumerate(tetrahedron) if i not in incident]
        new_triangles.append(new_tetra)
        return new_triangles
    return None


def move_2_3(tetrahedron):
    """
    This function implements Pachner Move type 2-3

    Move 2-3 increases the number of tetrahedra by one and adds one new edge, preserving the number of vertices and locally modifying the faces

    Parameters
    ----------

    tetrahedron: list of tuples of four ints
        Tetrahedrons mesh list
    
    Returns
    -------
    new_tetrahedrons: list of tuple
        if there are common faces for two tetrahedrons
    
    tetrahedron: list of tuple
        if there are no common faces for two tetrahedrons

    Examples:

    >>> tetrahedron = [(0, 1, 2, 3),(0, 1, 2, 4)] # Visualize original figure
    >>> Pachner_move_2_3 = PySimplicial.utils.move_2_3(tetrahedron) # visualize the same figure but with Pachner Move 2-3 triangulation
    >>> print(f"basic tetrahedron={tetrahedron}")
    >>> print(f"same tetrahedron but with move 2-3={Pachner_move_2_3}")
    basic tetrahedron=[(0, 1, 2, 3), (0, 1, 2, 4)]
    same tetrahedron but with move 2-3=[(0, 1, 3, 4), (1, 2, 3, 4), (0, 2, 3, 4)]

    """
    # we need to construct a mapping : edge -> list of tris containing it
    ett = defaultdict(list) # edge to tris
    for idx, (a,b,c,d) in enumerate(tetrahedron):
        for edge in [tuple(sorted((a,b,c))), tuple(sorted((a,b,d))), tuple(sorted((a,c,d))), tuple(sorted((b,c,d)))]:
            ett[edge].append(idx) # add the index of the current triangle to the list of triangles that own this edge
    #exist=set(ett.keys()) # set of all exist edges ; it is necessary to check whether a new diagonal already exists
    # choose an edge that has exactly two tris
    inter=[e for e, idx in ett.items() if len(idx) == 2]
    random.shuffle(inter)
    #edge=random.choice(inter) # choose random
    for edge in inter:
        t1_idx,t2_idx=ett[edge]
        a,b,c = edge # a,b,c = end of this edge
        t1 = tetrahedron[t1_idx]
        t2 = tetrahedron[t2_idx]
        d = [v for v in t1 if v not in edge][0]
        e = [v for v in t2 if v not in edge][0]
        new_tetrahedrons = [t for i, t in enumerate(tetrahedron) if i != t1_idx and i != t2_idx] # all triangles except those with indices 0 and 1 will be empty []
        new_tetrahedrons.append((a, b, d, e))
        new_tetrahedrons.append((b, c, d, e))
        new_tetrahedrons.append((a, c, d, e))
        return new_tetrahedrons
    return tetrahedron

def move_3_2(tetrahedron):
    """
    This function implements Pachner Move type 3-1
    
    The 3-2 move is the inverse of the 2-3 move, replacing three tetrahedra meeting on an internal edge between two tetrahedra sharing a face, reducing the number of tetrahedra by one, and removing one edge without changing vertices
    
    Parameters
    ----------

    tetrahedron: list of tuples of four ints
        Tetrahedrons mesh list

    Returns
    -------

    result: list of tuple of four ints
        If there's a common edge that belongs to exactly three tetrahedra
    
    tetrahedron: list of tuple of four ints
        If there is no common edge that belongs to exactly three tetrahedra
    
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
    """
    edge_to_tetrahedrons = defaultdict(list)
    for idx, tetrahedron_ in enumerate(tetrahedron):
        a,b,c,d = tetrahedron_
        for edge in [(a,b), (a,c), (a,d), (b,c), (b,d), (c,d)]:
            edge = tuple(sorted(edge))
            edge_to_tetrahedrons[edge].append(idx)
    for edge, tetrahedron_idx in edge_to_tetrahedrons.items():
        if len(tetrahedron_idx) != 3:
            continue
        i1, i2, i3 = tetrahedron_idx
        t1 = tetrahedron[i1]
        t2 = tetrahedron[i2]
        t3 = tetrahedron[i3]
        u, v = edge
        exts = []
        for t in (t1, t2, t3):
            pair = [x for x in t if x not in (u, v)]
            exts.append(tuple(sorted(pair)))
        all_ext = list({x for pair in exts for x in pair})
        if len(all_ext) != 3:
            continue
        a,b,c = sorted(all_ext)
        new_t1 = tuple(sorted((a,b,c,u)))
        new_t2 = tuple(sorted((a,b,c,v)))
        result = [t for i, t in enumerate(tetrahedron) if i not in tetrahedron_idx]
        result.extend([new_t1, new_t2])
        return result
    return tetrahedron