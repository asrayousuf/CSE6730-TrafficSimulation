import Constants


class Car:
    def __init__(self, id_num):
        self.id = id_num
        self.identifier = 'Car ' + str(id_num)
        self.length = Constants.CAR_LENGTH


class CorridorNetwork:
    def __init__(self):
        intersection1 = self.Intersection(34.7, 28, 8)
        intersection2 = self.Intersection(41.5, 20.3, 8)
        intersection3 = self.Intersection(60.9, 27.3, 8)
        intersection4 = self.Intersection(float('inf'), 0, 0)
        intersection5 = self.Intersection(34.6, 22.4, 9.8)

        self.intersections = [intersection1, intersection2, intersection3, intersection4, intersection5]

        self.speed_limit = Constants.SPEED_LIMIT

    class Intersection:
        def __init__(self, northbound_green_duration, westbound_green_duration, eastbound_green_duration):
            self.light_cycle_time = northbound_green_duration + westbound_green_duration + eastbound_green_duration

            self.northbound_section = self.Section()
            self.northbound_trafficLight = self.TrafficLight(0, northbound_green_duration)

            # right turn onto corridor
            self.westbound_section = self.Section()
            self.westbound_trafficLight = self.TrafficLight(northbound_green_duration, westbound_green_duration)

            # left turn onto corridor
            self.eastbound_section = self.Section()
            self.eastbound_trafficLight = self.TrafficLight(northbound_green_duration + westbound_green_duration,
                                                            eastbound_green_duration)

        class Section:
            def __init__(self):
                self.length = Constants.SECTION_LENGTH
                self.car_count = 0

        class TrafficLight:
            def __init__(self, green_start_time, green_duration):
                self.green_duration = green_duration
                self.green_start_time = green_start_time
                self.green_end_time = green_start_time + green_duration





