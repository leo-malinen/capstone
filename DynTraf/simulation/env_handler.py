import simpy
from simulation.event_handler import EventHandler

class SimulationManager:
    def __init__(self, network_graph, config):
        self.env = simpy.Environment()
        self.network = network_graph
        self.config = config
        self.event_handler = EventHandler(self.env, self.network)
        
        self.stats = {
            'accidents': 0,
            'completed_trips': 0
        }

    def register_spawner(self, spawner_func):
        """
        Registers the vehicle spawning process.
        """
        self.env.process(spawner_func(self.env, self.network))

    def register_traffic_lights(self, traffic_lights):
        """
        Registers all traffic light agents.
        """
        for tl in traffic_lights:
            pass 

    def start(self):
        """
        Kicks off the simulation loop.
        """
        print(f"--- Simulation Started (Duration: {self.config.SIMULATION_TIME}) ---")
                self.event_handler.start_random_events()

        self.env.run(until=self.config.SIMULATION_TIME)
        print("--- Simulation Ended ---")
