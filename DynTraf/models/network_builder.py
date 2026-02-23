import networkx as nx

class TrafficNetwork:
    def __init__(self):
        self.graph = nx.DiGraph()

    def build_grid_network(self, rows=7, cols=7):

        self.graph = nx.grid_2d_graph(rows, cols, periodic=False)
        self.graph = self.graph.to_directed()
        
        for u, v in self.graph.edges():
            self.graph[u][v]['length'] = 100
            self.graph[u][v]['max_speed'] = 50
            self.graph[u][v]['vehicles'] = []
            self.graph[u][v]['blocked'] = False 

        self._assign_districts(rows, cols)
        
        return self.graph

    def _assign_districts(self, rows, cols):
        mid_x = rows / 2
        mid_y = cols / 2

        for node in self.graph.nodes():
            x, y = node
            
            if x < mid_x and y < mid_y:
                district = 'Residential'
            elif x >= mid_x and y < mid_y:
                district = 'Commercial'
            elif x < mid_x and y >= mid_y:
                district = 'Industrial'
            else:
                district = 'Downtown'
                
            self.graph.nodes[node]['district'] = district
