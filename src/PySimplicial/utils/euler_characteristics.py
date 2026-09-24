# pick fugire (list) and calculate type of surface g by Eulers Characteristic: x = V - E + F = 2 - 2g
# V = unique vertices, E = unique edges, F = number of faces, g = surface genus

def euler_characteristics(mesh):

    """
    Calculates the Euler's characteristics for mesh in form of (a,b,c) and mesh in form of (a,b,c,d)

    (a,b,c): The Euler's Characteristics has invented by Leonard Euler and looks like that x = V - E + F = 2 - 2g, so, we can find g if we change this formula (Assumes the mesh is a closed orientable surface)

    (a,b,c,d): Formula: χ = V - E + F - T

    Note
    ----

    * Vertices and edges are counted uniquely

    * V is unique vertices

    * E is unique edges

    * F is unique faces

    * T is amount of tetrahedrons

    Parameters
    ----------
    mesh: list of tuple

        Enter triangulation list
    
    Returns
    -------

    g / x: int
    
        Natural number that says the genus of the surface

        2D - g. Formula "g = (2 - (V-E+F)) // 2"

        3D - x. Formula "χ = V - E + F - T"

    Examples
    --------

    >>> octahedron = [(0,1,2), (0,2,3), (0,3,4), (0,4,1),(5,2,1), (5,3,2), (5,4,3), (5,1,4)]
    >>> print(euler_characteristics(octahedron))
    0
    >>> tetrahedron = [(0, 1, 2, 3),(0, 1, 2, 4)]
    >>> print(euler_characteristics(tetrahedra))
    1

    """
    if not mesh:
        raise ValueError("mesh must not be empty")    
    if len(mesh[0]) == 3:
        F = len(mesh) # In example of octahedron: F=8
        vert = set() # set() guarantees no duplicates
        for (a,b,c) in mesh: # calculate V
            vert.add(a)
            vert.add(b)
            vert.add(c)
        V = len(vert) # In example of octahedron: V=6 
        edges = set()
        for (a,b,c) in mesh: # calculate E
            # if 2 triangles share one edge ; Example. Upper: 1-2 & Lower: 2-1 ; They will be written in edges as (1,2) 
            edges.add(tuple(sorted((a,b)))) # About python base: tuple() is list ensures that it cannot be modified after creation ; sorted(()) sorts values ​​in ascending order
            edges.add(tuple(sorted((b,c))))
            edges.add(tuple(sorted((a,c))))
        E = len(edges) # In example of octahedron: E=12
        x = V-E+F
        if x > 2 or (2-x) % 2 != 0:
            raise ValueError("euler's characteristics is incompatible with this surface")
        g = (2 - (V-E+F)) // 2
        return g
    elif len(mesh[0]) == 4:
        T = len(mesh)
        vert = set()
        for (a,b,c,d) in mesh:
            vert.add(a)
            vert.add(b)
            vert.add(c)
            vert.add(d)
        V = len(vert)
        edges = set()
        for (a,b,c,d) in mesh:
            edges.add(tuple(sorted((a,b)))) 
            edges.add(tuple(sorted((a,c))))
            edges.add(tuple(sorted((a,d))))
            edges.add(tuple(sorted((b,c))))
            edges.add(tuple(sorted((b,d))))
            edges.add(tuple(sorted((c,d))))
        E = len(edges)
        faces=set()
        for (a,b,c,d) in mesh:
            faces.add(tuple(sorted((a,b,c))))
            faces.add(tuple(sorted((a,b,d))))
            faces.add(tuple(sorted((a,c,d))))
            faces.add(tuple(sorted((b,c,d))))
        F = len(faces)
        x = V-E+F-T
        return x
    else:
        raise NotImplementedError("only triangles and tetrahedra are supported")
