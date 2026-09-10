import networkx
import matplotlib.pyplot as plt
import mpl_toolkits
import random
from mpl_toolkits.mplot3d.art3d import Poly3DCollection

def visualize_triangulation_2D(figure): # 2D visualization
    """
    This function works on top of networkx.Graph() and networkx.spring_layout, it takes vertices, connects them and renders them based on the given shape

    We take a triangle, a list of the form (a,b,c) or (a,b,c,d) and distribute each of its vertices, then with the help of spring_layout we build a dict and then visualize it using draw


    Parameters
    ----------

    figure: list of tuple
        Triangles mesh list

    type: str
        if type="Triangles" then function work with list of tuple in form of (a,b,c)

        if type="Tetrahedrons" then function work with list of tuple in form of (a,b,c,d)

    Returns
    -------

    Visualized figure with using matplotlib
    
    Examples
    --------

    The example can be found in official pysimplicial repository in Tutorials/showcase

    """
    if len(figure[0]) == 3:
        G = networkx.Graph() # create empty graph
        for a,b,c in figure: # add edges from triangle
            G.add_edge(a,b)
            G.add_edge(b,c)
            G.add_edge(c,a)
        pos = networkx.spring_layout(G, seed=1) # define vertices position
        plt.figure(figsize=(5,5))
        networkx.draw(G, pos, with_labels=True, node_color="lightblue", node_size=500, font_size=10)
        plt.axis("off")
        plt.show()
    elif len(figure[0]) == 4:
        G = networkx.Graph() # create empty graph
        for a,b,c,d in figure: # add edges from triangle
            G.add_edge(a,b)
            G.add_edge(a,c)
            G.add_edge(a,d)
            G.add_edge(b,c)
            G.add_edge(b,d)
            G.add_edge(c,d)
        pos = networkx.spring_layout(G, seed=1) # define vertices position
        plt.figure(figsize=(5,5))
        networkx.draw(G, pos, with_labels=True, node_color="lightblue", node_size=500, font_size=10)
        plt.axis("off")
        plt.show()

def visualize_triangulation_3D(figure, fs1=8, fs2=6, xlim=-1, ylim=-1, zlim = -1, xlimright=1, ylimright=1, zlimright=1, enable_random_face_colors=False, xlab="X axis", ylab="Y axis", zlab="Z axis", facecolor="Purple", edgecolor="White", custom_pos=None, show=True):
    """
    This function draws a figure using matplotlib's 3D projection. To set xyz correctly, it uses spring_layout with dimension = 3 from networkx. This function is still under development, but it works well with Triangles mesh list in form of (a,b,c) and Tetrahedrons mesh list in form of (a,b,c,d)
    
    Parameters
    ----------

    figure: list of tuple in form of
        (a,b,c) is triangles mesh list

        (a,b,c,d) is tetrahedrons mesh list

    figsize=(fs1, fs2): ArrayLike
        figsize integer numbers

    xlim / xlimright: float, optional
        The left/right xlim in data coordinates

    ylim / ylimright: float, optional
        The left/right ylim in data coordinates
    
    zlim / zlimright: float, optional
        The left/right zlim in data coordinates

    enable_random_face_colors: boolean
        if true then ```face_colors = [[random.random() for _ in range(3)] for _ in figure]```

        else: user need to choose his own colors

    xlab: str
        set_xlabel text
    
    ylab: str
        set_ylabel text
    
    zlab: str
        set_zlabel text
    
    facecolor: str
        the figure face color
    
        if user make the enable_random_face_colors = False, then user can choose his own color. Standart is "Purple"

    edgecolor: str
        the figure edge color

        if user make the enable_random_face_colors = False, then user can choose his own color. Standart is "White"

    custom_pos: Any
        custom coords position (without spring_layout pos generation)
    
    show: boolean
        If true: then user can see visualized by matplotlib figure

        else: return ax, fig

        
    Returns
    -------

    Visualized figure

    fig & ax: Figure and Axes3D

    Examples
    --------

    >>> octahedron = [(0,1,2), (0,2,3), (0,3,4), (0,4,1),(5,2,1), (5,3,2), (5,4,3), (5,1,4)]
    >>> PySimplicial.utils.visualize_triangulation_3D(octahedron, enable_random_face_colors=False)
    >>> 3d_figure = PySimplicial.utils.move_1_3(octahedron)
    >>> returns = PySimplicial.utils.visualize_triangulation_3D(abcd, enable_random_face_colors=False)
    >>> print(returns)
    (<Figure size 800x600 with 1 Axes>, <Axes3D: xlabel='X axis', ylabel='Y axis', zlabel='Z axis'>)
    
    """
    coords = []
    fig = plt.figure(figsize=(fs1, fs2))
    ax = fig.add_subplot(111, projection="3d")
    if custom_pos is not None:
        if not isinstance(custom_pos, dict):
            print("custom pos is not dict")
            return None
    if len(figure[0]) == 3:
        if custom_pos==None:
            G = networkx.Graph() # create empty graph
            for a,b,c in figure: # add edges from triangle
                G.add_edge(a,b)
                G.add_edge(b,c)
                G.add_edge(c,a)
            pos = networkx.spring_layout(G, seed=1, dim=3) # define vertices position
        else:
            pos = custom_pos
            vertices = {v for triangle in figure for v in triangle}
            custom_pos_vertices = set(pos.keys())
            missing = vertices - custom_pos_vertices
            if missing:
                raise ValueError(f"Missing vertices: {missing}")
            for v, coord in pos.items():
                if len(coord) != 3:
                    raise ValueError(f"vertex {v} has {len(coord)} coordinates, expected 3")
        for a,b,c in figure:
            coords.append([pos[a], pos[b], pos[c]])
    elif len(figure[0]) == 4:
        if custom_pos==None:
            G = networkx.Graph() # create empty graph
            for a,b,c,d in figure: # add edges from triangle
                G.add_edge(a,b)
                G.add_edge(a,c)
                G.add_edge(a,d)
                G.add_edge(b,c)
                G.add_edge(b,d)
                G.add_edge(c,d)
            pos = networkx.spring_layout(G, seed=1, dim=3) # define vertices position
        else:
            pos = custom_pos
            vertices = {v for tetrahedron in figure for v in tetrahedron}
            custom_pos_vertices = set(pos.keys())
            missing = vertices - custom_pos_vertices
            if missing:
                raise ValueError(f"Missing vertices: {missing}")
            for v, coord in pos.items():
                if len(coord) != 3:
                    raise ValueError(f"vertex {v} has {len(coord)} coordinates, expected 3")
        for a,b,c,d in figure:

            coords.append([pos[a], pos[b], pos[c]])
            coords.append([pos[a], pos[b], pos[d]])
            coords.append([pos[a], pos[c], pos[d]])
            coords.append([pos[b], pos[c], pos[d]]) 
        else:
            raise ValueError("Unsupported simplex dimension")
    if enable_random_face_colors:
        face_colors = [[random.random() for _ in range(3)] for _ in coords]
        pol = Poly3DCollection(coords, facecolors=face_colors)
    else:
        pol = Poly3DCollection(coords, facecolors=facecolor, edgecolors=edgecolor)
    ax.add_collection3d(pol)
    ax.set_xlim([xlim, xlimright])
    ax.set_ylim([ylim, ylimright])
    ax.set_zlim([zlim, zlimright])
    ax.set_xlabel(xlab)
    ax.set_ylabel(ylab)
    ax.set_zlabel(zlab)
    ax.set_box_aspect([1,1,1])
    if show:
        plt.show()
    return fig, ax
        
"""def visualize_triangulation_3D(tetrahedron): # 3D visualization

    This function works on top of networkx.Graph() and networkx.spring_layout, it takes vertices, connects them and renders them based on the given shape

    Does not implement 3D visualization, the function simply accepts a tetrahedron with 4 vertices instead of a triangle with 3 vertices.

    We take a tetrahedron, a list of the form (a,b,c,d) and distribute each of its vertices, then through spring_layout we build a dict and then visualize it through draw
    
    Parameters
    ----------

    tetrahedron: list of tuple
        Tetrahedrons mesh list

    Returns
    -------

    Visualized figure with using matplotlib
    
    Examples
    --------

    The example can be found in official pysimplicial repository in Tutorials/showcase

    G = networkx.Graph() # create empty graph
    for a,b,c,d in tetrahedron: # add edges from triangle
        G.add_edge(a,b)
        G.add_edge(a,c)
        G.add_edge(a,d)
        G.add_edge(b,c)
        G.add_edge(b,d)
        G.add_edge(c,d)
    pos = networkx.spring_layout(G, seed=1) # define vertices position
    plt.figure(figsize=(5,5))
    networkx.draw(G, pos, with_labels=True, node_color="lightblue", node_size=500, font_size=10)
    plt.axis("off")
    plt.tight_layout()
    plt.show()"""

# TODO: I need to make the same visualization, but in 3D space, but I don't know exactly how to do it yet ; Add function checks that the triangulation is a closed two-dimensional surface