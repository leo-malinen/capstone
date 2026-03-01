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

current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.append(current_dir)

def vehicle_spawner(env, network):
    vehicle_count = 0
    nodes = list(network.nodes())
    
    while True:
        yield env.timeout(random.randint(3, 8)) 
        vehicle_count += 1
        
        if nodes:
            start_node = random.choice(nodes)
            end_node = random.choice(nodes)

            if start_node != end_node:
                try:
                    if nx.has_path(network, start_node, end_node):
                        path = nx.shortest_path(network, start_node, end_node, weight='length')
                        Vehicle(env, vehicle_count, network, path)
                except nx.NetworkXNoPath:
                    pass

def main():
    print(f"Starting DynTraf from: {current_dir}")
    app = QApplication(sys.argv)

    print("Initializing Framework")
    net_builder = TrafficNetwork()

    print("Launching Interface")
    window = MainWindow(net_builder, vehicle_spawner, SignalOptimizer)
    window.show()

    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
