import heapq

from threading import Lock, Thread, Condition

#Simulator Data Structures
futureEventList = []

#Constants - checkpoint uses the following assumptions and simplifications
carLength = 14.0 #ft
speedLim = 44.0 #ft/sec
segmentLength = 528.0 #ft
greenLightDuration = 30 #sec
lightCycleTime = 60 #sec


#Road Segment Car Counts
numSourceSegCars = 0
numCorridorSegCars = 0


#current thread of execution with lock
execControl = Condition(Lock())
controller = 'Scheduler'

#time stamp tracker
now = 0.0


#traverse car across corridor (for checkpoint, corridor is from intersection 1 to intersection 2)
def traverseCar(car):
    global controller
    global now

    arriveEvent1(car)

    leaveEvent1(car)

    arriveEvent2(car)

    leaveEvent2(car)


def arriveEvent1(car):
    global controller
    execControl.acquire()
    while controller != car:
        execControl.wait()
    arriveAtIntersection1()
    print (car, now, "Arrive at Intersection 1 - START")

    waitForGreenLight1(car)
    controller = 'Scheduler'
    execControl.notifyAll()
    execControl.release()

def arriveAtIntersection1():
    global numSourceSegCars
    numSourceSegCars += 1

def waitForGreenLight1(car):
    curSegClearanceTime = (numSourceSegCars - 1) * carLength / speedLim
    nextGreenLightTime = now + curSegClearanceTime
    if int(nextGreenLightTime) % lightCycleTime >= 30:
        nextGreenLightTime += lightCycleTime - nextGreenLightTime % lightCycleTime
    heapq.heappush(futureEventList, (nextGreenLightTime, car))

def leaveEvent1(car):
    global controller
    execControl.acquire()
    while controller != car:
        execControl.wait()
    leaveFromIntersection1()
    print (car, now, "Leave from Intersection 1")

    move(car)
    controller = 'Scheduler'
    execControl.notifyAll()
    execControl.release()

def leaveFromIntersection1():
    global numSourceSegCars
    numSourceSegCars -= 1

def move(car):
    nextSegClearanceTime = numCorridorSegCars * carLength / speedLim
    nextSegFrontTravelTime = segmentLength / speedLim
    heapq.heappush(futureEventList, (now + nextSegClearanceTime + nextSegFrontTravelTime, car))

def arriveEvent2(car):
    global controller
    execControl.acquire()
    while controller != car:
        execControl.wait()
    arriveAtIntersection2()
    print (car, now, "Arrive at Intersection 2")

    waitForGreenLight2(car)
    controller = 'Scheduler'
    execControl.notifyAll()
    execControl.release()

def arriveAtIntersection2():
    global numCorridorSegCars
    numCorridorSegCars += 1

def waitForGreenLight2(car):
    curSegClearanceTime = (numCorridorSegCars - 1) * carLength / speedLim
    nextGreenLightTime = now + curSegClearanceTime
    if int(nextGreenLightTime) % lightCycleTime >= 30:
        nextGreenLightTime += lightCycleTime - nextGreenLightTime % lightCycleTime
    heapq.heappush(futureEventList, (nextGreenLightTime, car))

def leaveEvent2(car):
    global controller
    execControl.acquire()
    while controller != car:
        execControl.wait()
    leaveFromIntersection2()
    print (car, now, "Leave from Intersection 2 - FINISH")
    controller = 'Scheduler'
    execControl.notifyAll()
    execControl.release()

def leaveFromIntersection2():
    global numCorridorSegCars
    numCorridorSegCars -= 1

if __name__ == '__main__':
    heapq.heappush(futureEventList, (0.0, 'Car 1'))
    car1Thread = Thread(target=traverseCar, args=('Car 1',))

    heapq.heappush(futureEventList, (1 * carLength / speedLim, 'Car 2'))
    car2Thread = Thread(target=traverseCar, args=('Car 2',))

    heapq.heappush(futureEventList, (2 * carLength / speedLim, 'Car 3'))
    car3Thread = Thread(target=traverseCar, args=('Car 3',))

    heapq.heappush(futureEventList, (3 * carLength / speedLim, 'Car 4'))
    car4Thread = Thread(target=traverseCar, args=('Car 4',))

    execControl.acquire()
    while controller != 'Scheduler':
        execControl.wait()
    while futureEventList:
        process = heapq.heappop(futureEventList)

        now = process[0]
        controller = process[1]

        if controller == 'Car 1':
            if not car1Thread.is_alive():
                car1Thread.start()
        elif controller == 'Car 2':
            if not car2Thread.is_alive():
                car2Thread.start()
        elif controller == 'Car 3':
            if not car3Thread.is_alive():
                car3Thread.start()
        elif controller == 'Car 4':
            if not car4Thread.is_alive():
                car4Thread.start()

        execControl.notifyAll()
        execControl.release()

        execControl.acquire()
        while controller != 'Scheduler':
            execControl.wait()









