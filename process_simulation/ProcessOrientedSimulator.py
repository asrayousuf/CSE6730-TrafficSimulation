from __future__ import division

import random

import math

import heapq

from threading import Lock, Thread, Condition

from CorridorNetwork import Car, CorridorNetwork

from Constants import CAR_LENGTH, SCALE


# Future Event List
fel = []

# Corridor Network
corridor = CorridorNetwork()

# Cars
cars = []

# car travel times
travel_times = []

#total tracked cars
tracked_car_count =  0

# incomplete car count
incomplete_car_count = 0

# controlling thread
controller = 'Scheduler'
execControl = Condition(Lock())

# time stamp tracker
now = 0.0


def generate_num_cars(rate_param):
    mean = 1 / rate_param
    u = random.uniform(0, 1)
    return int(round(-1 * mean * math.log(1 - u)))


def seed_section(intersection_num, section_name, rate_param):
    num_cars = generate_num_cars(rate_param)

    if section_name == 'eastbound':
        section = corridor.intersections[intersection_num - 1].eastbound_section
        start_time = now + 30
        is_tracked = False
    elif section_name == 'westbound':
        section = corridor.intersections[intersection_num - 1].westbound_section
        start_time = now + 50
        is_tracked = False
    else:
        section = corridor.intersections[intersection_num - 1].northbound_section
        start_time = now
        is_tracked = True
        global tracked_car_count
        tracked_car_count = num_cars
        global incomplete_car_count
        incomplete_car_count = num_cars

    section.car_count = num_cars

    for i in range(num_cars):
        car = Car(len(cars), is_tracked)
        if section_name == 'northbound':
            car_thread = Thread(target=traverse_car, args=(car,))
        else:
            car_thread = Thread(target=enhance_traffic, args=(car, intersection_num, section_name))
            car_thread.setDaemon(True)
        cars.append((car, car_thread))
        heapq.heappush(fel, (start_time + i * CAR_LENGTH / corridor.speed_limit, car.id))


def seed_traffic():
    seed_section(1, 'northbound', SCALE * 0.11157156518967166)

    seed_section(1, 'westbound', SCALE * 0.024334016393442622)
    seed_section(1, 'eastbound', SCALE * 0.027154494783478634)

    seed_section(2, 'westbound', SCALE * 0.01001401962747847)

    seed_section(3, 'eastbound', SCALE * 0.0061462814996926865)


def traverse_car(car):
    global controller

    leave(car, 1, 'northbound')
    arrive(car, 2)
    leave(car, 2, 'northbound')
    arrive(car, 3)
    leave(car, 3, 'northbound')
    arrive(car, 4)
    leave(car, 4, 'northbound')
    arrive(car, 5)


def enhance_traffic(car, intersection_num, direction):
    leave(car, intersection_num, direction)
    for i in range(intersection_num + 1, 5):
        arrive(car, i)
        leave(car, i, 'northbound')
    arrive(car, 5)


def leave(car, intersection_num, section_name):
    global controller

    execControl.acquire()
    while controller != car.identifier:
        execControl.wait()
    if intersection_num == 1:
        if car.is_tracked:
            car.entrance_time = now

    exit_intersection(corridor.intersections[intersection_num - 1], section_name)
    move(car, corridor.intersections[intersection_num], 'TR')

    controller = 'Scheduler'
    execControl.notifyAll()
    execControl.release()


def exit_intersection(intersection, section_name):
    if section_name == 'eastbound':
        section = intersection.eastbound_section
    elif section_name == 'westbound':
        section = intersection.westbound_section
    else:
        section = intersection.northbound_section
    section.car_count -= 1


def move(car, intersection, direction):
    if direction == 'TR':
        northbound_section = intersection.northbound_section
        section_clearance_time = northbound_section.car_count * CAR_LENGTH / corridor.speed_limit
        section_travel_time = northbound_section.length / corridor.speed_limit
        heapq.heappush(fel, (now + section_clearance_time + section_travel_time, car.id))


def arrive(car, intersection_num):
    global incomplete_car_count
    global controller

    execControl.acquire()
    while controller != car.identifier:
        execControl.wait()
    enter_intersection(corridor.intersections[intersection_num - 1])
    if intersection_num < 5:
        wait_for_green(car, corridor.intersections[intersection_num - 1], 'northbound')
    elif car.is_tracked:
        incomplete_car_count -= 1
        car.exit_time = now
        if tracked_car_count - incomplete_car_count > 1:
            travel_times.append(car.exit_time - car.entrance_time)
        else:
            print 'Warm Up Time: ' + str(car.exit_time - car.entrance_time)
    controller = 'Scheduler'
    execControl.notifyAll()
    execControl.release()


def enter_intersection(intersection):
    northbound_section = intersection.northbound_section
    northbound_section.car_count += 1


def wait_for_green(car, intersection, section_name):
    if section_name == 'eastbound':
        section = intersection.eastbound_section
        traffic_light = intersection.eastbound_trafficLight
    elif section_name == 'westbound':
        section = intersection.westbound_section
        traffic_light = intersection.westbound_trafficLight
    else:
        section = intersection.northbound_section
        traffic_light = intersection.northbound_trafficLight

    light_cycle_time = intersection.light_cycle_time
    green_start_time = traffic_light.green_start_time
    green_end_time = traffic_light.green_end_time

    section_clearance_time = (section.car_count - 1) * CAR_LENGTH / corridor.speed_limit
    next_green_time = now + section_clearance_time
    relative_next_green_time = next_green_time % light_cycle_time
    if not (green_start_time <= relative_next_green_time < green_end_time):
        if section_name == 'eastbound':
            next_green_time = next_green_time - relative_next_green_time + green_start_time
        elif section_name == 'westbound':
            if 0 <= relative_next_green_time < green_start_time:
                relative_next_green_time += light_cycle_time
            next_green_time = next_green_time - (relative_next_green_time - green_start_time) + light_cycle_time
        else:
            next_green_time = next_green_time - (relative_next_green_time - green_start_time) + light_cycle_time

    heapq.heappush(fel, (next_green_time, car.id))


if __name__ == '__main__':
    seed_traffic()

    print 'Total Vehicles Traversing Corridor: ' + str(tracked_car_count - 1)

    execControl.acquire()
    while controller != 'Scheduler':
        execControl.wait()
    while incomplete_car_count > 0:
        process = heapq.heappop(fel)

        now = process[0]
        car_id_num = process[1]
        car_tuple = cars[car_id_num]
        controller = car_tuple[0].identifier
        car_thread = car_tuple[1]

        if not car_thread.is_alive():
            car_thread.start()

        execControl.notifyAll()
        execControl.release()

        execControl.acquire()
        while controller != 'Scheduler':
            execControl.wait()

    if len(travel_times) > 0:
        print 'Mean Travel Time: ' + str(sum(travel_times) / len(travel_times))
    else:
        print 'No cars generated'
