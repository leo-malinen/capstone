import simpy
from config import YELLOW_TIME

class TrafficLight:
    def __init__(self, env, node_id, optimizer):
        self.env = env
        self.node_id = node_id
        self.optimizer = optimizer
        self.direction_green = 0
        self.action = env.process(self.run())

    def run(self):
        while True:
            green_duration = self.optimizer.calculate_green_time(self.node_id)
            yield self.env.timeout(green_duration)
            yield self.env.timeout(YELLOW_TIME)
            self.switch_direction()

    def switch_direction(self):
        pass