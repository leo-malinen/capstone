import sys
import random
import networkx as nx
from PyQt5.QtWidgets import QApplication
from models.network_builder import TrafficNetwork
from models.traffic_light import TrafficLight
from models.vehicle import Vehicle
from algorithms.optimizer import SignalOptimizer
from simulation.env_manager import SimulationManager
import config

from ui.window import MainWindow

def vehicle_spawner(env, network):
    vehicle_count = 0
    nodes = list(network.nodes()) 
    while True:
        yield env.timeout(random.randint(5, 15))       
        vehicle_count += 1
        
        start_node = random.choice(nodes) # Random start and ends
        end_node = random.choice(nodes)
        
        if start_node != end_node:
            try:
                if nx.has_path(network, start_node, end_node):
                    path = nx.shortest_path(network, start_node, end_node, weight='length')                    
                    Vehicle(env, vehicle_count, network, path) # Vehicle spawn
                else:
                    print(f"Skipping spawn: No path possible from {start_node} to {end_node}")
                    
            except nx.NetworkXNoPath:
                pass

def main():
    app = QApplication(sys.argv)

    print("Building Grid")
    net_builder = TrafficNetwork()
    graph = net_builder.build_grid_network(rows=5, cols=5)

    print("Initializing Environment")
    sim_manager = SimulationManager(graph, config)

    optimizer = SignalOptimizer(graph)

    print("Deploying Traffic Lights")
    for node in graph.nodes():
        TrafficLight(sim_manager.env, node, optimizer)

    sim_manager.register_spawner(vehicle_spawner)

    # Launch the Visualization (View)
    window = MainWindow(sim_manager)
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
