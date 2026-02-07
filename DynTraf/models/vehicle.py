class Vehicle:
    def __init__(self, env, vehicle_id, network, route):
        self.env = env
        self.id = vehicle_id
        self.network = network
        self.route = route 
        self.current_edge = None
        self.action = env.process(self.drive())

    def drive(self):
        for i in range(len(self.route) - 1):
            u = self.route[i]
            v = self.route[i+1]
            
            self.current_edge = (u, v)
            self.network[u][v]['vehicles'].append(self)
            travel_time = self.calculate_travel_time(u, v)
            yield self.env.timeout(travel_time)
            
            # May add intersection access below
            # yield request_access_to_intersection(v)
            self.network[u][v]['vehicles'].remove(self)

    def calculate_travel_time(self, u, v):
        return 5 # Fixed time for now
