import simpy
from simulation.event_handler import EventHandler

class SimulationManager:
    def __init__(self, network, config):
        self.env = simpy.Environment()
        self.network = network
        self.config = config
        self.event_handler = EventHandler(self.env, self.network)

    def register_spawner(self, spawner_func):
        self.env.process(spawner_func(self.env, self.network))
