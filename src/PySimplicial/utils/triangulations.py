import networkx
import matplotlib.pyplot as plt
import mpl_toolkits


def visualize_triangulation_2D(tris): # 2D visualization
    """
    This function works on top of networkx.Graph() and networkx.spring_layout, it takes vertices, connects them and renders them based on the given shape

    Parameters
    ----------

    tris: list of tuple
        Triangles mesh list

    Returns
    -------

    Visualized figure with using matplotlib
    
    Examples
    --------

    The example can be found in official pysimplicial repository in Tutorials/showcase

    """
    G = networkx.Graph() # create empty graph
    for a,b,c in tris: # add edges from triangle
        G.add_edge(a,b)
        G.add_edge(b,c)
        G.add_edge(c,a)
    pos = networkx.spring_layout(G, seed=1) # define vertices position
    plt.figure(figsize=(5,5))
    networkx.draw(G, pos, with_labels=True, node_color="lightblue", node_size=500, font_size=10)
    plt.axis("off")
    plt.tight_layout()
    plt.show()

def visualize_triangulation_3D(tetrahedron): # 3D visualization
    """
    This function works on top of networkx.Graph() and networkx.spring_layout, it takes vertices, connects them and renders them based on the given shape

    Does not implement 3D visualization, the function simply accepts a tetrahedron with 4 vertices instead of a triangle with 3 vertices.

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

    """
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
    plt.show()

# TODO: I need to make the same visualization, but in 3D space, but I don't know exactly how to do it yet ; Add function checks that the triangulation is a closed two-dimensional surface