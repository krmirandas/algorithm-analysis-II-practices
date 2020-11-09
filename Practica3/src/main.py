from graph_structure import Graph
from scalable_capabilities_algorithm import solve_with_capacity_scaling
  
#%%
# Create a simple demo graph to ease the debugging.
def construct_demo_graph():
    edge_list = [
        (1, 2, 5),
        (1, 3, 8),
        (1, 4, 3),
        (1, 5, 9),
        (2, 3, 2),
        (2, 6, 12),
        (3, 2, 5),
        (3, 6, 2),
        (4, 5, 3),
        (4, 6, 7),
        (5, 4, 6),
        (5, 6, 4)
        ]
    # edge_list = [
    #     (1,2,4), 
    #     (2,4,5),
    #     (1,3,3),
    #     (3,4,1),
    #     (3,2,3)
    #     ] 
    # Ejemplo practica 1: Flujo maximo 6
    # graph = Graph(4, edge_list)
    graph = Graph(6, edge_list)
    
    return graph

graph = construct_demo_graph()
solve_with_capacity_scaling(graph)
