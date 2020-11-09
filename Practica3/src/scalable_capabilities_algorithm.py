from collections import deque
import copy
import numpy as np
""" 
La función encontrará una ruta desde s a t.
Durante la busqueda los aristas tienen capacidades por debajo de delta 
se ignoran para realizar el escalado de capacidad. 

Los vecinos de un nodo se definen como nodos que 
están conectados con un arco mayor que la capacidad Delta.
"""
def find_path_from_source_to_target(graph, Delta):
    s, t = graph[1], graph[-1]
    # Se ponen a todos los vecinos de s a empezar a buscar
    linked_list = deque(s.get_adjacent_nodes(Delta))
    # Usamos una lista de booleanos para saber qué nodos fueron visitados. 
    # Cada índice corresponde al nodo con el mismo id
    is_marked = [False] * (len(graph.node_list) + 1) 
    is_marked[1] = True # set source as visited
    # Rastrea desde dónde se llega a cualquier nodo
    where_path_came_from = {node: s for node in linked_list}
    path_found = False
    while linked_list and not path_found:
        current_node = linked_list.popleft()

        # Obtener vecinas wrt Delta
        discovered_nodes = current_node.get_adjacent_nodes(Delta)
        for node in discovered_nodes:
            node_id = node.node_id
            # Si este nodo está marcado antes, ignórelo.
            if not is_marked[node_id]:
                # se agrega al final de la lista
                linked_list.append(node)
                # Si encuentra una ruta a un nuevo nodo, establezca su seguimiento
                if node not in where_path_came_from:
                    where_path_came_from[node] = current_node
                # Encontré una ruta al nodo de destino, establezca la bandera y salga
                if node.node_id == t.node_id:
                    path_found = True
                is_marked[node_id] = True

    # Construye la ruta a partir de las trazas y establezca el delta de capacidad de aumento
    # durante la construcción.
    
    if path_found:
        node_i = where_path_came_from[t]
        path = [t, node_i]
        delta = node_i.adjacency_map[t]
        while node_i != s:
            prev_node_i = node_i
            node_i = where_path_came_from[node_i]
            path.append(node_i)
            delta = min(delta,node_i.
                        adjacency_map[prev_node_i])
        
        path.reverse()
        return path, delta
    return False, False
#%%
# Aumenta las unidades delta de flujo a lo largo de la ruta dada y actualice la red residual.
# Actualiza el heap del gráfico si se usa el heap para escalar la capacidad.
def augment(graph, path, delta):
    # Para cada nodo en la ruta, elimine la unidad delta de capacidad del arco entrante
    # y agrega delta a la dirección inversa
    # print(path)
    for i in range(len(path)-1):
        from_node, to_node = path[i], path[i+1]
        print('------------- ' + 'ruta' + ' -------------')
        print('from' , from_node)
        print('to' , to_node)
        from_node_id, to_node_id = from_node.node_id, to_node.node_id
        graph[from_node_id].adjacency_map[path[i+1]] -= delta
        graph[to_node_id].adjacency_map[path[i]] += delta
        # print('from', graph[from_node_id])
        # print('to', graph[to_node_id])

# Calcula el flujo resultante en el sistema simplemente sumando el flujo en 
# los arcos inversos del objetivo
def get_max_flow(graph):
    t = graph[-1]
    adjacency_map = t.adjacency_map
    # print(adjacency_map)
    return sum([flow for flow in adjacency_map.values()])

# Esta función es una implementación de escalamiento de capacidad 
# que admite el uso de heap para la actualización Delta para la búsqueda de rutas.
def solve_with_capacity_scaling(graph, use_heap=False):
    # Establezca Delta inicial por su fórmula y continúe hasta que se establezca en 0.
    U = graph.maximum_capacity
    Delta = 2**np.floor(np.log(U))
    Deltas,deltas = [],[]
    while Delta > 0:
        path, delta = find_path_from_source_to_target(graph, Delta)
        # Almacene Delta y deltas para un análisis más detallado
        Deltas.append(Delta)
        deltas.append(delta)
        # Si se encuentra una ruta, simplemente aumenta y actualiza delta de lo contrario
        if path:
            augment(graph, path, delta)
        else:
            Delta = int(Delta / 2)

    # Solo devuelve el flujo máximo como un número entero
    max_flow = get_max_flow(graph)
    print('Flujo Máximo: ', max_flow)
    return int(max_flow), Deltas, deltas
