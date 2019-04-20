from __future__ import division

import random

import math

import heapq

from threading import Lock, Thread, Condition

from CorridorNetwork import Car, CorridorNetwork

from Constants import CAR_LENGTH


# Future Event List
fel = []

# Corridor Network
corridor = CorridorNetwork()

# Cars
cars = []

# controlling thread
controller = 'Scheduler'
execControl = Condition(Lock())

# time stamp tracker
now = 0.0

#def setUpTraffic():
    #move set up code from main to here, including heap pushing
    #distribution for entering corridor at each intersection(with interarrival times)
    #distributions for exiting out of intersections 2, 3, 4, 5


def generate_num_cars(lambda_value):
    mean = 1 / lambda_value
    u = random.uniform(0, 1)
    return int(round(-1 * mean * math.log(1 - u)))


def seed_section(intersection, lambda_value):
    num_cars = generate_num_cars(lambda_value)

    section = corridor.intersections[intersection - 1].inbound_section
    section.car_count = num_cars

    for i in range(num_cars):
        car = Car(i)
        cars.append((car, Thread(target=traverse_car, args=(car,))))
        #remember to change entry time on side intersections so they don't conflict with values in heap already
        heapq.heappush(fel, (i * CAR_LENGTH / corridor.speed_limit, car.id))


def traverse_car(car):
    global controller
    global now

    leave(car, 1)
    arrive(car, 2)
    leave(car, 2)
    arrive(car, 3)
    leave(car, 3)
    arrive(car, 4)
    leave(car, 4)
    arrive(car, 5)


def leave(car, intersection):
    global controller

    execControl.acquire()
    while controller != car.identifier:
        execControl.wait()
    if intersection == 1:
        print (car.identifier, 'Entrance', now)
    exit_intersection(corridor.intersections[intersection - 1])
    move(car, corridor.intersections[intersection])
    controller = 'Scheduler'
    execControl.notifyAll()
    execControl.release()


def exit_intersection(intersection):
    inbound_section = intersection.inbound_section
    inbound_section.car_count -= 1


def move(car, intersection):
    inbound_section = intersection.inbound_section
    section_clearance_time = inbound_section.car_count * CAR_LENGTH / corridor.speed_limit
    section_travel_time = inbound_section.length / corridor.speed_limit
    heapq.heappush(fel, (now + section_clearance_time + section_travel_time, car.id))


def arrive(car, intersection):
    global controller

    execControl.acquire()
    while controller != car.identifier:
        execControl.wait()
    enter_intersection(corridor.intersections[intersection - 1])
    if intersection < 5:
        wait_for_green(car, corridor.intersections[intersection - 1])
    else:
        print (car.identifier, 'Exit', now)
    controller = 'Scheduler'
    execControl.notifyAll()
    execControl.release()


def enter_intersection(intersection):
    inbound_section = intersection.inbound_section
    inbound_section.car_count += 1


def wait_for_green(car, intersection):
    inbound_section = intersection.inbound_section
    section_clearance_time = (inbound_section.car_count - 1) * CAR_LENGTH / corridor.speed_limit
    next_green_time = now + section_clearance_time
    traffic_light = intersection.northbound_trafficLight
    if int(next_green_time) % traffic_light.cycle_time >= traffic_light.green_duration:
        next_green_time += traffic_light.cycle_time - next_green_time % traffic_light.cycle_time
    heapq.heappush(fel, (next_green_time, car.id))


if __name__ == '__main__':
    seed_section(1, 0.10174586657417042)

    execControl.acquire()
    while controller != 'Scheduler':
        execControl.wait()
    while fel:
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









