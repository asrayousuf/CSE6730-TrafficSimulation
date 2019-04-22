package main.java;

import main.java.FileOperations.InputProcessor;
import main.java.FileOperations.OutputProcessor;
import main.java.Utilities.OutputAnalysis;
import main.java.Utilities.TimestampComparator;

import java.io.IOException;
import java.util.*;

public class Engine {
    static HashMap<Integer, double[][]> signalMap;
    static HashMap<Integer, Road> roadMap;
    static HashMap<Integer, Vehicle> vehicleList = new HashMap<Integer, Vehicle>();
    static ArrayList<Vehicle> result = new ArrayList<Vehicle>();
    public static PriorityQueue<Event> eventList = new PriorityQueue<Event>(100000, new TimestampComparator());
    public static int departedCount = 0;
    public static double firstExit = 0;
    public static int eventCount=0;
    public static int vehicleId =0;
    public static Vehicle generateVehicle(int id, int section, double startTime){
        Vehicle vehicle = new Vehicle(id,18, 1,  1,  25, section, startTime, 0, section, -1);
        vehicleList.put(id, vehicle);
        return vehicle;
    }
    public static Event generateEvent(double currentTS, int id, int section, String eventType){
        Event event = new Event(generateVehicle(id, section, currentTS), currentTS, eventType);
        return event;
    }
    public  static void schedule(Event event){
        Vehicle vehicle = event.getVehicle();
        double ts = event.timestamp;
        int section = vehicle.section;
        int nextSection = section + 1;
        if(section == 5){
            SimulateTraffic.departFromSystem(event);
        }
        else {
            int color = Signal.getColor(section, ts, 2, 1);
            OutputProcessor.displayEvent(event, color);
            if (color == 0 && !Road.isRoadFull(vehicle, nextSection)) {
                if(Math.random() < roadMap.get(section).exitProb){
                    SimulateTraffic.departFromSystem(event);
                }else {
                    SimulateTraffic.arriveAtIntersection(event);
                }

            } else {
                if (Road.isRoadFull(vehicle, nextSection)) {
                    System.out.println("Intersection " + nextSection + " is FULL!");
                }
                SimulateTraffic.waitAtIntersection(event, color);
            }
        }
    }

    public static void runSim(int endTime){
        double ts =0;
        SimulateTraffic.generateNewVehicle(ts, 1, roadMap.get(1).lambda);
        SimulateTraffic.generateNewVehicle(ts, 2, roadMap.get(2).lambda);
        SimulateTraffic.generateNewVehicle(ts, 3, roadMap.get(3).lambda);
        SimulateTraffic.generateNewVehicle(ts, 4, roadMap.get(4).lambda);
        SimulateTraffic.generateNewVehicle(ts, 5, roadMap.get(5).lambda);


        while(!Engine.eventList.isEmpty() && Engine.eventList.peek().timestamp <  endTime ) {
            Event event = Engine.eventList.poll();
            eventCount++;
            if(event.eventType.equals("new")){
                int section = event.vehicle.enterSection;
                SimulateTraffic.generateNewVehicle(event.timestamp, section, Engine.roadMap.get(section).lambda);
            }
            schedule(event);

        }
        OutputAnalysis.printStats(result);

    }


    public static void main(String args[]) throws IOException {
        signalMap = InputProcessor.readSignalData("../resources/noYellowSignal.csv"); // edited vesion of signalTiming.csv with no yellow lights
        roadMap= Road.initialiseRoadMap();
        int endTime = Integer.parseInt(args[0]);
        runSim(endTime);
    }

}
