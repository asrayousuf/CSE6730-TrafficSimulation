package main.java;

import main.java.FileOperations.InputProcessor;
import main.java.FileOperations.OutputProcessor;
import main.java.Utilities.TimestampComparator;

import java.io.IOException;
import java.util.HashMap;
import java.util.PriorityQueue;

public class SimulateTraffic {

    public static void arriveAtIntersection(Event event){
        Vehicle vehicle = event.getVehicle();
        float ts = event.timestamp;
        int section = vehicle.section;
        int nextSection = section +1;

        float future_ts = ts + (Engine.roadMap.get(nextSection).length / vehicle.velocity);
        vehicle.setSection(nextSection);
        System.out.println("Vehicle "+ vehicle.id+ " moves to section "+ nextSection);
        Engine.roadMap.get(nextSection).vehiclesOnRoad.add(vehicle);
        Engine.roadMap.get(nextSection).setOccupiedLength(vehicle.len, true);
        departFromIntersection(event);
        Event future_event = new Event(vehicle, future_ts);
        Engine.eventList.add(future_event);
        Engine.vehicleList.put(vehicle.id, vehicle);
    }
    public static void waitAtIntersection(Event event, int color){
        Vehicle vehicle = event.getVehicle();
        float ts = event.timestamp;
        int section = vehicle.section;
        int nextSection = section +1;
        float future_ts;
        if(color == 0 && Road.isRoadFull(vehicle, nextSection)) {
            System.out.println("Section "+ nextSection + " is full! \n" );
            future_ts = Signal.getTimeForGreenSignal(nextSection, ts, 2,1);
            if(future_ts == ts){
                future_ts = ts + (Engine.roadMap.get(nextSection).length/vehicle.velocity);
            }
            Event future_event = new Event(vehicle, future_ts);
            Engine.eventList.add(future_event);
        }else if(color==2){
            future_ts = Signal.getTimeForGreenSignal(section, ts, 2,1);
            Event future_event = new Event(vehicle, future_ts);
            Engine.eventList.add(future_event);
        }
    }
    public static void departFromIntersection(Event event){
        int section = event.vehicle.section;
        Engine.roadMap.get(section).vehiclesOnRoad.remove(event.vehicle);
        Engine.roadMap.get(section).setOccupiedLength(event.vehicle.len, false);
    }

    public static void departFromSystem(Event event){
        int section = event.vehicle.section;
        System.out.println("Depart Vehicle "+ event.vehicle.id+ " at ts: "+ event.timestamp);
        Engine.roadMap.get(section).vehiclesOnRoad.remove(event.vehicle);
        Engine.roadMap.get(section).setOccupiedLength(event.vehicle.len, false);
        Engine.vehicleList.remove(event.vehicle.id);
        Engine.departedCount ++;
    }
}
