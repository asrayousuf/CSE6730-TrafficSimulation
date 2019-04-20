import Constants


class Car:
    def __init__(self, id_num):
        self.id = id_num
        self.identifier = 'Car ' + str(id_num)
        self.length = Constants.CAR_LENGTH


class CorridorNetwork:
    def __init__(self):
        intersection1 = self.Intersection(34.7, 3.6 + 49.3, 28, 3.8 + 55, 30, 3.8 + 55)
        intersection2 = self.Intersection(41.5, 3.2 + 55.4, 20.3, 3.6 + 76.2, 20.2, 3.6 + 76.1)
        intersection3 = self.Intersection(60.9, 3.2 + 35.7, 27.3, 3.6 + 69.2, 27.3, 3.6 + 69.2)
        intersection4 = self.Intersection(float('inf'), 0, 0, 0, 0, 0)
        intersection5 = self.Intersection(34.6, 3.2 + 46.1, 22.4, 3.7 + 74, 36.9, 3.7 + 60.2)

        self.intersections = [intersection1, intersection2, intersection3, intersection4, intersection5]

        self.speed_limit = Constants.SPEED_LIMIT

    class Intersection:
        def __init__(self, northbound_green_duration, northbound_red_duration, westbound_green_duration,
                     westbound_red_duration, eastbound_green_duration, eastbound_red_duration):
            self.northbound_section = self.Section()
            self.northbound_trafficLight = self.TrafficLight(northbound_green_duration, northbound_red_duration)

            self.westbound_section = self.Section()
            self.westbound_trafficLight = self.TrafficLight(westbound_green_duration, westbound_red_duration)

            self.eastbound_section = self.Section()
            self.eastbound_trafficLight = self.TrafficLight(eastbound_green_duration, eastbound_red_duration)

        class Section:
            def __init__(self):
                self.length = Constants.SECTION_LENGTH
                self.car_count = 0

        class TrafficLight:
            def __init__(self, green_duration, red_duration):
                self.green_duration = green_duration
                self.cycle_time = green_duration + red_duration





