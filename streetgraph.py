class TrafficLight:
    def __init__(self):
        self.state = "red"
        self.timer = 0

    def change_state(self):
        if self.state == "red":
            self.state = "green"
        elif self.state == "green":
            self.state = "yellow"
        elif self.state == "yellow":
            self.state = "red"
        self.timer = 0

class Intersection:
    def __init__(self, id):
        self.id = id
        self.traffic_light = TrafficLight()

    def update(self):
        self.traffic_light.change_state()

class StreetGraph:
    def __init__(self):
        self.intersections = [Intersection(i) for i in range(5)]
    
    def update_traffic_lights(self):
        for intersection in self.intersections:
            intersection.update()
