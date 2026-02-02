from config import MIN_GREEN_TIME, MAX_GREEN_TIME

class SignalOptimizer:
    def __init__(self, network_graph):
        self.graph = network_graph

    def calculate_green_time(self, node_id):
        incoming_edges = self.graph.in_edges(node_id)
        total_cars = 0
        
        for u, v in incoming_edges:
            total_cars += len(self.graph[u][v]['vehicles'])

        # Simple linear scaling logic
        calculated_time = max(MIN_GREEN_TIME, min(total_cars * 2, MAX_GREEN_TIME))
        
        return calculated_time