import numpy as np
import matplotlib.pyplot as plt


def combinatorial_torus(m, n):
    """
    The function generates a combinatorial form of the torus figure, resulting in a list (matrix) of triangles (2D)

    Parameters
    ----------

    m: int
        Size of torus

    n: int
        Size of torus

    Returns
    -------

    tris: list of tuple
        Torus with size m x n
    
    Examples
    --------

    >>> combinatorial_torus_2D = PySimplicial.utils.combinatorial_torus(3,3)
    >>> print("combinatorial torus 2d")
    >>> print(combinatorial_torus_2D)
    combinatorial torus 2d
    [(0, 1, 3), (1, 4, 3), (1, 2, 4), (2, 5, 4), (2, 0, 5), (0, 3, 5), (3, 4, 6), (4, 7, 6), (4, 5, 7), (5, 8, 7), (5, 3, 8), (3, 6, 8), (6, 7, 0), (7, 1, 0), (7, 8, 1), (8, 2, 1), (8, 6, 2), (6, 0, 2)]
    """
    def vid(r,c):
        return (r % m) * n + (c % n)
    tris = []
    for r in range(m):
        for c in range(n):
            v00 = vid(r,c)
            v01 = vid(r, c+1)
            v10 = vid(r+1, c)
            v11 = vid(r+1,c+1)
            tris.append((v00, v01, v10))
            tris.append((v01, v11, v10))
    return tris

def geometry_torus(m,n,R,r):
    """
    
    This function generates a geometric torus (suitable for custom visualization) in the form of a point cloud or surface

    The function is based on basic torus generation formulas

    x = (R + r * np.cos(v)) * np.cos(u)
    y = (R + r * np.cos(v)) * np.sin(u)
    z = r * np.sin(v)
    
    Parameters
    ----------

    m: int
        Number of partition points based on parameters u

    n: int
        Number of partition points based on parameters v

    R: int
        R major
    
    r: int
        r minor
    
    Returns
    -------

    result: dict[int, tuple[float, float, float]]
        geometric torus

    Examples
    --------
    
    >>> geometry_torus_3D = PySimplicial.utils.geometry_torus(3,3,2,1)
    >>> print("geometry torus 3d")
    >>> print(geometry_torus_3D)
    geometry torus 3d
    {0: (np.float64(3.0), np.float64(0.0), np.float64(0.0)), 1: (np.float64(1.5000000000000002), np.float64(0.0), np.float64(0.8660254037844387)), 2: (np.float64(1.4999999999999996), np.float64(0.0), np.float64(-0.8660254037844385)), 3: (np.float64(-1.4999999999999993), np.float64(2.598076211353316), np.float64(0.0)), 4: (np.float64(-0.7499999999999998), np.float64(1.2990381056766582), np.float64(0.8660254037844387)), 5: (np.float64(-0.7499999999999994), np.float64(1.2990381056766578), np.float64(-0.8660254037844385)), 6: (np.float64(-1.5000000000000013), np.float64(-2.5980762113533156), np.float64(0.0)), 7: (np.float64(-0.7500000000000008), np.float64(-1.299038105676658), np.float64(0.8660254037844387)), 8: (np.float64(-0.7500000000000004), np.float64(-1.2990381056766573), np.float64(-0.8660254037844385))}

    """
    result = {}
    for id in range(m * n):
        row = id // n
        col = id % n
        u = 2 * np.pi * row / m
        v = 2 * np.pi * col / n
        x = (R + r * np.cos(v)) * np.cos(u)
        y = (R + r * np.cos(v)) * np.sin(u)
        z = r * np.sin(v)
        result[id] = (x,y,z)
    return result


def combinatorial_torus_3D(m, n, p):
    """
    The function generates a combinatorial form of the torus figure, resulting in a list (matrix) of triangles (3D)

    Parameters
    ----------

    m: int
        Size of torus

    n: int
        Size of torus

    p: int
        Size of torus

    Returns
    -------

    tets: list of tuple
        Torus with size m x n x p
    
    Examples
    --------
    
    >>> combinatorial_torus_3D = PySimplicial.utils.combinatorial_torus_3D(2,2,2)
    >>> print("combinatorial torus 3d")
    >>> print(combinatorial_torus_3D)
    combinatorial torus 3d
    [(0, 4, 6, 7), (0, 4, 5, 7), (0, 2, 6, 7), (0, 2, 3, 7), (0, 1, 5, 7), (0, 1, 3, 7), (1, 5, 7, 6), (1, 5, 4, 6), (1, 3, 7, 6), (1, 3, 2, 6), (1, 0, 4, 6), (1, 0, 2, 6), (2, 6, 4, 5), (2, 6, 7, 5), (2, 0, 4, 5), (2, 0, 1, 5), (2, 3, 7, 5), (2, 3, 1, 5), (3, 7, 5, 4), (3, 7, 6, 4), (3, 1, 5, 4), (3, 1, 0, 4), (3, 2, 6, 4), (3, 2, 0, 4), (4, 0, 2, 3), (4, 0, 1, 3), (4, 6, 2, 3), (4, 6, 7, 3), (4, 5, 1, 3), (4, 5, 7, 3), (5, 1, 3, 2), (5, 1, 0, 2), (5, 7, 3, 2), (5, 7, 6, 2), (5, 4, 0, 2), (5, 4, 6, 2), (6, 2, 0, 1), (6, 2, 3, 1), (6, 4, 0, 1), (6, 4, 5, 1), (6, 7, 3, 1), (6, 7, 5, 1), (7, 3, 1, 0), (7, 3, 2, 0), (7, 5, 1, 0), (7, 5, 4, 0), (7, 6, 2, 0), (7, 6, 4, 0)]
    """
    def vid3D(i, j, k):
        return ((i % m) * n + (j % n)) * p + (k % p)
    tets = []
    for i in range(m):
        for j in range(n):
            for k in range(p):
                v000 = vid3D(i, j, k)
                v100 = vid3D(i+1, j, k)
                v010 = vid3D(i, j+1, k)
                v001 = vid3D(i, j, k+1)
                v110 = vid3D(i+1, j+1, k)
                v101 = vid3D(i+1, j, k+1)
                v011 = vid3D(i, j+1, k+1)
                v111 = vid3D(i+1, j+1, k+1)
                tets.extend([(v000, v100, v110, v111),(v000, v100, v101, v111),(v000, v010, v110, v111),(v000, v010, v011, v111),(v000, v001, v101, v111),(v000, v001, v011, v111)])
    return tets

cos = np.cos
sin = np.sin
sqrt = np.sqrt
pi = np.pi

def geometry_bottle_of_klein(u, v):
    """
    Calculates the coordinates of the Klein bottle points given the parameterization

    Parameters
    ----------

    u: np.ndarray
        Array of first parameter values

    v: np.ndarray
        Array of second parameter values (must have the same shape as u)

    Returns
    -------

    x : np.ndarray
        x-coordinates of surface points ; shape matches u, v
    y : np.ndarray
        y-coordinates of surface points
    z : np.ndarray
        z-coordinates of surface points

    Examples
    --------

    >>> u = np.linspace(0, 2*np.pi, 100)
    >>> v = np.linspace(0, 2*np.pi, 100)
    >>> u, v = np.meshgrid(u, v)
    >>> x, y, z = PySimplicial.utils.geometry_bottle_of_klein(u, v)
    >>> fig = plt.figure()
    >>> ax = fig.add_subplot(111, projection='3d')
    >>> ax.plot_surface(x, y, z)
    >>> plt.show()

    """
    half = (0 <= u) & (u < pi)
    r = 4*(1 - cos(u)/2)
    x = 6*cos(u)*(1 + sin(u)) + r*cos(v + pi)
    x[half] = ((6*cos(u)*(1 + sin(u)) + r*cos(u)*cos(v))[half])
    y = 16 * sin(u)
    y[half] = (16*sin(u) + r*sin(u)*cos(v))[half]
    z = r * sin(v)
    return x, y, z