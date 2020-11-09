from collections import defaultdict
from heapdict import heapdict


class Edge:
    
    def __init__(self, node_i, node_j, capacity):
        self.node_i = node_i
        self.node_j = node_j
        self.capacity = capacity

class Node:
    
    def __init__(self, node_id):
        self.node_id = node_id
        self.adjacency_map = defaultdict(int)

    def __str__(self):
        adjacency_str = ', '.join(['Node:' + str(node.node_id) + '->' + 'Capacity:' +str(capacity) for node, capacity in self.adjacency_map.items()])
        return 'Node id: ' + str(self.node_id) +'\n' + adjacency_str

    def add_edge(self, e):
        if e.node_i.node_id == self.node_id:
            self.adjacency_map[e.node_j] = e.capacity
        else:
            print('I can\'t add edge')

    def get_adjacent_nodes(self, delta=0):
        return [key for key,value in self.adjacency_map.items() if value >= delta]

class Graph:
    
    def __init__(self, node_count, edge_list):
        self.node_list = [Node(i) for i in range(node_count + 1)]
        self.maximum_capacity = -1
        self.edge_list = edge_list
        self.edge_heap = heapdict({(t[0], t[1]): t[2] for t in edge_list})
        for e in edge_list:
            # print(e[2])
            self.maximum_capacity = max(self.maximum_capacity, e[2])
            node_i_id = e[0]
            self.node_list[node_i_id].add_edge(
                    Edge(self.node_list[e[0]], self.node_list[e[1]], e[2]))

    """
    Con esta funcion no es necesario implementar getters y setters
    """
    def __getitem__(self, index):
        return self.node_list[index]
    
    def copy(self):
        node_count = len(self.node_list) - 1
        edge_list_copy = self.edge_list.copy()
        return Graph(node_count, edge_list_copy)