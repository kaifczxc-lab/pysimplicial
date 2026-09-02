import PySimplicial.utils as ps

triangles = [(0, 1, 2), (0, 2, 3)]
v_p, g_edges, open_ports = ps.graph(triangles, type="2D")
print("v_p: ", v_p)
print("g_edges: ", g_edges)
print("open_ports: ", open_ports)

tetrahedrons = [(0, 1, 2, 3),(0, 1, 2, 4)]
v_p_3D, g_edges_3D, open_ports_3D = ps.graph(tetrahedrons, type="3D")
print("v_p_3D: ", v_p_3D)
print("g_edges_3D: ", g_edges_3D)
print("open_ports_3D: ", open_ports_3D)

"""
v_p:  [(0, 1, 2), (3, 4, 5)]
g_edges:  [(2, 3)]
open_ports:  [0, 1, 4, 5]
v_p_3D:  [(0, 1, 2, 3), (4, 5, 6, 7)]
g_edges_3D:  [(0, 4)]
open_ports_3D:  [1, 2, 3, 5, 6, 7]
"""