from streetgraph import StreetGraph
from utils import log_event

class Simulation:
    def __init__(self):
        self.graph = StreetGraph()
        self.time = 0

    def run(self, steps):
        for _ in range(steps):
            self.step()

    def step(self):
        self.update()
        log_event(f"Time: {self.time}")
        self.time += 1

    def update(self):
        self.graph.update_traffic_lights()
