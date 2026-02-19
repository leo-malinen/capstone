import random

class EventHandler:
    def __init__(self, env, network):
        self.env = env
        self.network = network
        self.env.process(self.accident_generator())

    def accident_generator(self):
        while True:
            yield self.env.timeout(random.randint(50, 200))
            edges = list(self.network.edges())
            if edges:
                u, v = random.choice(edges)
                self.env.process(self.trigger_accident(u, v))

    def trigger_accident(self, u, v):
        self.network[u][v]['blocked'] = True
        self.network[u][v]['weight'] = float('inf')
        yield self.env.timeout(50)
        self.network[u][v]['blocked'] = False
        self.network[u][v]['weight'] = 1
