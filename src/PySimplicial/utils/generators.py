import numpy as np
import matplotlib.pyplot as plt


def combinatorial_torus(m, n):
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
    returns point cloud / surface
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
    returns point cloud / surface
    """
    half = (0 <= u) & (u < pi)
    r = 4*(1 - cos(u)/2)
    x = 6*cos(u)*(1 + sin(u)) + r*cos(v + pi)
    x[half] = ((6*cos(u)*(1 + sin(u)) + r*cos(u)*cos(v))[half])
    y = 16 * sin(u)
    y[half] = (16*sin(u) + r*sin(u)*cos(v))[half]
    z = r * sin(v)
    return x, y, z