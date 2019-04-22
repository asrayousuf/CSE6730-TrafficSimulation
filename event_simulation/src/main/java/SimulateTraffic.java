package main.java;

import main.java.FileOperations.InputProcessor;
import main.java.FileOperations.OutputProcessor;
import main.java.Utilities.RandomGenerator;
import main.java.Utilities.TimestampComparator;

import java.io.IOException;
import java.util.HashMap;
import java.util.PriorityQueue;

public class SimulateTraffic {

    public static void arriveAtIntersection(Event event){
        Vehicle vehicle = event.getVehicle();
        double ts = event.timestamp;
        int section = vehicle.section;
        int nextSection = section + 1;
        String eventType ="move";

        System.out.println("Vehicle "+ vehicle.id+ " moves to section "+ nextSection);

        departFromIntersection(event);

        vehicle.setSection(nextSection);
        Engine.roadMap.get(nextSection).vehiclesOnRoad.add(vehicle);
        Engine.roadMap.get(nextSection).setOccupiedLength(vehicle.len, true);
        double future_ts = ts + (Engine.roadMap.get(nextSection).length / vehicle.velocity);
        Event future_event = new Event(vehicle, future_ts, eventType );
        Engine.eventList.add(future_event);
        Engine.vehicleList.put(vehicle.id, vehicle);

    }
    public static void waitAtIntersection(Event event, int color){
        Vehicle vehicle = event.getVehicle();
        double ts = event.timestamp;
        int section = vehicle.section;
        int nextSection = section +1;
        double future_ts;
        String eventType = "wait";
        future_ts = Signal.getTimeForGreenSignal(section, ts, 2,1);
        Event future_event = new Event(vehicle, future_ts, eventType);
        Engine.eventList.add(future_event);

    }
    public static void departFromIntersection(Event event){
        int section = event.vehicle.section;
        Engine.roadMap.get(section).vehiclesOnRoad.remove(event.vehicle);
        Engine.roadMap.get(section).setOccupiedLength(event.vehicle.len, false);
    }

    public static void departFromSystem(Event event){
        int section = event.vehicle.section;
        Vehicle vehicle = event.vehicle;
        System.out.println("Vehicle "+ event.vehicle.id+ " departs at intersection " + section + " at ts: "+ event.timestamp);
        Engine.roadMap.get(section).vehiclesOnRoad.remove(event.vehicle);
        Engine.roadMap.get(section).setOccupiedLength(event.vehicle.len, false);
        Engine.departedCount ++;
        Engine.vehicleList.get(event.vehicle.id).setEndTime(event.timestamp);
        Engine.vehicleList.get(event.vehicle.id).setExitSection(section);
        if(Engine.firstExit ==0 && vehicle.enterSection==1 && (vehicle.exitSection == 5 || vehicle.exitSection==6)){
            Engine.firstExit = vehicle.endTime;
        }else{
            if(vehicle.startTime > Engine.firstExit && (vehicle.exitSection == 5 || vehicle.exitSection==6) && vehicle.enterSection == 1){
                Engine.result.add(Engine.vehicleList.get(event.vehicle.id));
            }
        }
    }
    public static void generateNewVehicle(double currentTS, int section, double lambda){
            String eventType = "new";
            int u = RandomGenerator.getPoisson(lambda);
            currentTS = currentTS + (double)(u);
            Engine.vehicleId = Engine.vehicleId + 1;
            System.out.println(String.format("\n Vehicle %d generated at section %d at timestamp %f ", Engine.vehicleId, section, currentTS));

            Event newEvent = Engine.generateEvent(currentTS, Engine.vehicleId, section, eventType);
            /*if(Road.isRoadFull(newEvent.vehicle, section)){
                   double waitTime = Signal.getTimeForGreenSignal(section, currentTS, 2,1);
                   newEvent.timestamp = currentTS + waitTime;
            }*/
            Engine.eventList.add(newEvent);
            Engine.roadMap.get(section).vehiclesOnRoad.add(newEvent.vehicle);
            Engine.roadMap.get(section).setOccupiedLength(newEvent.vehicle.len, true);
    }
}
