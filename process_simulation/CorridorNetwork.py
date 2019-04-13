class Car:
    def __init__(self, identifier):
        self.identifier = identifier


class CorridorNetwork:
    def __init__(self):
        intersection1 = self.Intersection(41.5, 3.2 + 55.4)
        intersection2 = self.Intersection(41.5, 3.2 + 55.4)
        intersection3 = self.Intersection(41.5, 3.2 + 55.4)
        intersection4 = self.Intersection(41.5, 3.2 + 55.4)
        intersection5 = self.Intersection(41.5, 3.2 + 55.4)

        self.intersections = [intersection1, intersection2, intersection3, intersection4, intersection5]

        self.speed_limit = 44
        self.car_length = 18

    class Intersection:
        def __init__(self, green_duration, red_duration):
            self.inbound_section = self.Section()
            self.northbound_trafficLight = self.TrafficLight(green_duration, red_duration)

        class Section:
            def __init__(self):
                self.length = 528
                self.car_count = 0

        class TrafficLight:
            def __init__(self, green_duration, red_duration):
                self.green_duration = green_duration
                self.cycle_time = green_duration + red_duration





