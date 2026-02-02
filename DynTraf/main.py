import simpy
import random
from models.network_builder import TrafficNetwork
from models.traffic_light import TrafficLight
from models.vehicle import Vehicle
from algorithms.optimizer import SignalOptimizer
from config import SIMULATION_TIME

# vehicles generate randomly first
def vehicle_spawner(env, network, spawn_rate=0.5):
    vehicle_count = 0
    nodes = list(network.nodes())
    
    while True:
        yield env.timeout(random.expovariate(spawn_rate))
        vehicle_count += 1
        start = random.choice(nodes)
        end = random.choice(nodes)
        if start != end:
            try:
                path = nx.shortest_path(network, start, end)
                Vehicle(env, vehicle_count, network, path)
                print(f"Vehicle {vehicle_count} spawned: {start} -> {end}")
            except nx.NetworkXNoPath:
                pass

def main():
    env = simpy.Environment()
    net_builder = TrafficNetwork()
    graph = net_builder.build_grid_network(rows=5, cols=5) # 5x5 grid
    
    optimizer = SignalOptimizer(graph)
    for node in graph.nodes():
        TrafficLight(env, node, optimizer)
    env.process(vehicle_spawner(env, graph))
    
    print("Starting DynTraf Simulation...")
    env.run(until=SIMULATION_TIME)
    print("Simulation complete.")

if __name__ == "__main__":
    main()