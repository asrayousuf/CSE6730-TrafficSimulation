from __future__ import division

import heapq

from threading import Lock, Thread, Condition

from CorridorNetwork import Car, CorridorNetwork




#Simulator Data Structures
futureEventList = []

# Corridor Network
corridor = CorridorNetwork()

# Cars
car1 = Car('Car 1')
car2 = Car('Car 2')
car3 = Car('Car 3')
car4 = Car('Car 4')

# controlling thread
controller = 'Scheduler'
execControl = Condition(Lock())

# time stamp tracker
now = 0.0


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
    section_clearance_time = inbound_section.car_count * corridor.car_length / corridor.speed_limit
    section_travel_time = inbound_section.length / corridor.speed_limit
    heapq.heappush(futureEventList, (now + section_clearance_time + section_travel_time, car.identifier))


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
    section_clearance_time = (inbound_section.car_count - 1) * corridor.car_length / corridor.speed_limit
    next_green_time = now + section_clearance_time
    traffic_light = intersection.northbound_trafficLight
    if int(next_green_time) % traffic_light.cycle_time >= traffic_light.green_duration:
        next_green_time += traffic_light.cycle_time - next_green_time % traffic_light.cycle_time
    heapq.heappush(futureEventList, (next_green_time, car.identifier))

if __name__ == '__main__':
    section1 = corridor.intersections[0].inbound_section

    heapq.heappush(futureEventList, (0.0, car1.identifier))
    car1Thread = Thread(target=traverse_car, args=(car1,))
    section1.car_count += 1

    heapq.heappush(futureEventList, (1 * corridor.car_length / corridor.speed_limit, car2.identifier))
    car2Thread = Thread(target=traverse_car, args=(car2,))
    section1.car_count += 1

    heapq.heappush(futureEventList, (2 * corridor.car_length / corridor.speed_limit, car3.identifier))
    car3Thread = Thread(target=traverse_car, args=(car3,))
    section1.car_count += 1

    heapq.heappush(futureEventList, (3 * corridor.car_length / corridor.speed_limit, car4.identifier))
    car4Thread = Thread(target=traverse_car, args=(car4,))
    section1.car_count += 1

    execControl.acquire()
    while controller != 'Scheduler':
        execControl.wait()
    while futureEventList:
        process = heapq.heappop(futureEventList)

        now = process[0]
        controller = process[1]

        if controller == car1.identifier:
            if not car1Thread.is_alive():
                car1Thread.start()
        elif controller == car2.identifier:
            if not car2Thread.is_alive():
                car2Thread.start()
        elif controller == car3.identifier:
            if not car3Thread.is_alive():
                car3Thread.start()
        elif controller == car4.identifier:
            if not car4Thread.is_alive():
                car4Thread.start()

        execControl.notifyAll()
        execControl.release()

        execControl.acquire()
        while controller != 'Scheduler':
            execControl.wait()









