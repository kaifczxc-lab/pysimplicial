# pick fugire (list) and calculate type of surface g by Eulers Characteristic: x = V - E + F = 2 - 2g
# V = unique vertices, E = unique edges, F = number of faces, g = surface genus

def compute_genus_2D(triangle_mesh2D):

    """
    Calculates the type of surface in 2D mesh and depends of number says how much there holes

    The Euler's Characteristics has invented by Leonard Euler and looks like that x = V - E + F = 2 - 2g, so, we can find g if we change this formula (Assumes the mesh is a closed orientable surface)

    Vertices and edges are counted uniquely

    Parameters
    ----------
    triangle_mesh2D: list of tuple

        Enter triangulation in form list of triangles

        Every triangle is a tuple of three integers (vertex indices)
    
    Returns
    -------

    g: int
    
        Natural number that says the genus of the surface

    Examples
    --------

    >>> octahedron = [(0,1,2), (0,2,3), (0,3,4), (0,4,1),(5,2,1), (5,3,2), (5,4,3), (5,1,4)]
    >>> print(compute_genus_2D(octahedron))
    0

    """
    F = len(triangle_mesh2D) # In example of octahedron: F=8
    vert = set() # set() guarantees no duplicates
    for (a,b,c) in triangle_mesh2D: # calculate V
        vert.add(a)
        vert.add(b)
        vert.add(c)
    V = len(vert) # In example of octahedron: V=6 
    edges = set()
    for (a,b,c) in triangle_mesh2D: # calculate E
        # if 2 triangles share one edge ; Example. Upper: 1-2 & Lower: 2-1 ; They will be written in edges as (1,2) 
        edges.add(tuple(sorted((a,b)))) # About python base: tuple() is list ensures that it cannot be modified after creation ; sorted(()) sorts values ​​in ascending order
        edges.add(tuple(sorted((b,c))))
        edges.add(tuple(sorted((a,c))))
    E = len(edges) # In example of octahedron: E=12
    g = (2 - (V-E+F)) // 2 # Pick our values: 6 - 12 + 8 = 2 ==> 2 - 2 = 0 // 2 ==> g = 0 
    return g


def compute_connected_components_3D(tetrahedron_mesh3D):
    """
    Calculates the number of connected components of a 3D space
    
    Formula: χ = V - E + F - T

    Where:

    V is unique vertices

    E is unique edges

    F is unique faces

    T is amount of tetrahedrons

    Parameters
    ----------

    tetrahedron_mesh3D : list of tuple

        Enter triangulation in form list of tetrahedrons

        Every tetrahedron is a tuple of four integers (vertex indices)

    Returns
    -------

    x: int

        Natural number that says amount of connected components of a 3D space
    
    Examples
    --------

    >>> tetrahedron = [(0, 1, 2, 3),(0, 1, 2, 4)]
    >>> print(compute_genus_3D(tetrahedra))
    1
    
    """
    T = len(tetrahedron_mesh3D)
    vert = set()
    for (a,b,c,d) in tetrahedron_mesh3D:
        vert.add(a)
        vert.add(b)
        vert.add(c)
        vert.add(d)
    V = len(vert)
    edges = set()
    for (a,b,c,d) in tetrahedron_mesh3D:
        edges.add(tuple(sorted((a,b)))), 
        edges.add(tuple(sorted((a,c)))), 
        edges.add(tuple(sorted((a,d)))), 
        edges.add(tuple(sorted((b,c))))
        edges.add(tuple(sorted((b,d)))), 
        edges.add(tuple(sorted((c,d))))
    E = len(edges)
    faces=set()
    for (a,b,c,d) in tetrahedron_mesh3D:
        faces.add(tuple(sorted((a,b,c))))
        faces.add(tuple(sorted((a,b,d))))
        faces.add(tuple(sorted((a,c,d))))
        faces.add(tuple(sorted((b,c,d))))
    F = len(faces)
    x = V-E+F-T
    return x