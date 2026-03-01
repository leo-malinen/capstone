import networkx as nx

class TrafficNetwork:
    def __init__(self):
        self.graph = nx.DiGraph()
        self.h_streets = ["1st St", "2nd St", "3rd St", "4th St", "5th St", "6th St", "7th St"]
        self.v_streets = ["A Ave", "B Ave", "C Ave", "D Ave", "E Ave", "F Ave", "G Ave"]

    def build_grid_network(self, rows=7, cols=7):
        self.graph = nx.grid_2d_graph(rows, cols, periodic=False)
        self.graph = self.graph.to_directed()
        
        for u, v in self.graph.edges():
            self.graph[u][v]['length'] = 100
            self.graph[u][v]['vehicles'] = []
            self.graph[u][v]['blocked'] = False 
            

            if u[0] == v[0]: 
                self.graph[u][v]['name'] = self.v_streets[u[0]]
            else: 
                self.graph[u][v]['name'] = self.h_streets[u[1]]

        self._assign_districts_by_borders()
        self.graph.graph['type'] = 'grid' 
        return self.graph

    def build_sample_network(self):
        """Builds a messy, non-uniform grid to simulate an OSM import MVP."""
        self.graph = nx.DiGraph()
        edges = [
            (0,1), (1,2), (2,3), (1,4), (4,5), (5,6), (4,7), (7,8), (2,8),
            (8,9), (9,10), (10,3), (7,11), (11,12), (12,10)
        ]
        self.graph.add_edges_from(edges)
        self.graph.add_edges_from([(v, u) for u, v in edges]) 
        
        for u, v in self.graph.edges():
            self.graph[u][v]['length'] = random_length = 50
            self.graph[u][v]['vehicles'] = []
            self.graph[u][v]['blocked'] = False
            self.graph[u][v]['name'] = "Sample Rd"

        for node in self.graph.nodes():
            self.graph.nodes[node]['district'] = 'Downtown' 
            
        self.graph.graph['type'] = 'sample'
        return self.graph

    def _assign_districts_by_borders(self):
        """Assigns districts by defining a boundary of 4 street names."""
        v_idx = {name: i for i, name in enumerate(self.v_streets)}
        h_idx = {name: i for i, name in enumerate(self.h_streets)}

        districts = {
            'Residential': ('A Ave', 'D Ave', '1st St', '4th St'),
            'Commercial':  ('D Ave', 'G Ave', '1st St', '4th St'),
            'Industrial':  ('A Ave', 'D Ave', '4th St', '7th St'),
            'Downtown':    ('D Ave', 'G Ave', '4th St', '7th St')
        }

        for node in self.graph.nodes():
            x, y = node 
            self.graph.nodes[node]['district'] = 'Unknown'
            
            for dist_name, (w, e, s, n) in districts.items():
                if w in v_idx and e in v_idx and s in h_idx and n in h_idx:
                    if v_idx[w] <= x <= v_idx[e] and h_idx[s] <= y <= h_idx[n]:
                        self.graph.nodes[node]['district'] = dist_name
