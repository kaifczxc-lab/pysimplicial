from collections import defaultdict
import random    
from collections import Counter

def move_2_2(tris):
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
    index = random.randrange(len(tris))
    a,b,c = tris[index]
    n_v = max(max(t) for t in tris) + 1 # +1 gives guaranteed unique ID
    n_triangles = [t for i,t in enumerate(tris) if i != index]
    n_triangles += [(a,b,n_v), (b,c,n_v), (a,c,n_v)]
    return n_triangles 

def move_3_1(tris):
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
    index = random.randrange(len(tetrahedron))
    a,b,c,d = tetrahedron[index]
    n_v = max(max(t) for t in tetrahedron) + 1 # +1 gives guaranteed unique ID
    n_triangles = [t for i,t in enumerate(tetrahedron) if i != index]
    n_triangles += [(a, b, c, n_v),(a, b, d, n_v),(a, c, d, n_v),(b, c, d, n_v)]
    return n_triangles 

def move_4_1(tetrahedron):
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
    # we need to construct a mapping : edge -> list of tris containing it
    ett = defaultdict(list) # edge to tris
    for idx, (a,b,c,d) in enumerate(tetrahedron):
        for edge in [tuple(sorted((a,b,c))), tuple(sorted((a,b,d))), tuple(sorted((a,c,d))), tuple(sorted((b,c,d)))]:
            ett[edge].append(idx) # add the index of the current triangle to the list of triangles that own this edge
    exist=set(ett.keys()) # set of all exist edges ; it is necessary to check whether a new diagonal already exists
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
    edge_to_tetrahedrons = defaultdict(list)
    for idx, tetrahedron_ in enumerate(tetrahedron):
        a, b, c, d = tetrahedron_
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
        a, b, c = sorted(all_ext)
        new_t1 = tuple(sorted((a, b, c, u)))
        new_t2 = tuple(sorted((a, b, c, v)))
        result = [t for i, t in enumerate(tetrahedron) if i not in tetrahedron_idx]
        result.extend([new_t1, new_t2])
        return result
    return tetrahedron