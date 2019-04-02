package main.java;

import main.java.FileOperations.InputProcessor;
import main.java.FileOperations.OutputProcessor;
import main.java.Utilities.TimestampComparator;

import java.io.IOException;
import java.util.HashMap;
import java.util.PriorityQueue;

public class Engine {
    static HashMap<Integer, float[][]> signalMap;
    static HashMap<Integer, Road> roadMap;
    static HashMap<Integer, Vehicle> vehicleList = new HashMap<Integer, Vehicle>();
    static PriorityQueue<Event> eventList = new PriorityQueue<Event>(10000, new TimestampComparator());
    static int departedCount = 0;

    public static Vehicle generateVehicle(int id, float startTime){
        Vehicle vehicle = new Vehicle(id,10, 1,  1,  20, 1, startTime, 0);
        return vehicle;
    }
    public static Event generateEvent(float currentTS, int id){
        Event event = new Event(generateVehicle(id, currentTS), currentTS);
        return event;
    }
    public  static void schedule(Event event){
        Vehicle vehicle = event.getVehicle();
        float ts = event.timestamp;
        int section = vehicle.section;
        int nextSection = section +1;
        int color = Signal.getColor(section, ts, 2, 1);

        OutputProcessor.displayEvent(event, color);
        if(color == 0 && !Road.isRoadFull(vehicle, nextSection)) {
            if (nextSection == 6) {
                SimulateTraffic.departFromSystem(event);
            } else {
                SimulateTraffic.arriveAtIntersection(event);
            }
        }else{
            SimulateTraffic.waitAtIntersection(event, color);
        }

    }
    public static void runSim(){
        //Generate 2 initial vehicles
        int vehicleId =1;
        float ts =0;
        int eventCount=0;
        Vehicle vehicle1 = Engine.generateVehicle(vehicleId++, ts);
        Engine.eventList.add(new Event(vehicle1, ts));
        roadMap.get(1).vehiclesOnRoad.add(vehicle1);
        roadMap.get(1).setOccupiedLength(vehicle1.len, true);
        ts+=2;
        Vehicle vehicle2 = Engine.generateVehicle(vehicleId++, ts);
        Engine.eventList.add(new Event(vehicle2, ts));
        roadMap.get(1).vehiclesOnRoad.add(vehicle2);
        roadMap.get(1).setOccupiedLength(vehicle2.len, true);

        while(!Engine.eventList.isEmpty() && Engine.eventList.peek().timestamp <  260 ) {
            Event event = Engine.eventList.poll();
            eventCount++;
            if(Math.random()<0.3) {
                ts = ts + (float)(Math.random()*10);
                Event newEvent = Engine.generateEvent(ts, vehicleId++);
                Engine.eventList.add(newEvent);
                roadMap.get(1).vehiclesOnRoad.add(newEvent.vehicle);
                roadMap.get(1).setOccupiedLength(newEvent.vehicle.len, true);
            }
            schedule(event);
        }
        System.out.println("Total Number of Vehicles in the system = "+ vehicleId);
        System.out.println("Total number of events processed =" + eventCount);
        System.out.println("Number of vehicles exited the system =" + departedCount);
        System.out.println("Total number of events yet to be processed =" + eventList.size());
    }

    public static void main(String args[]) throws IOException {
        signalMap = InputProcessor.readSignalData("../resources/noYellowSignal.csv"); // edited vesion of signalTiming.csv with no yellow lights
        roadMap= Road.initialiseRoadMap();
        runSim();

    }
}
