package main.java;

import main.java.FileOperations.InputProcessor;
import main.java.FileOperations.OutputProcessor;
import main.java.Utilities.TimestampComparator;

import java.io.IOException;
import java.util.HashMap;
import java.util.PriorityQueue;

public class SimulateTraffic {
    static HashMap<Integer, float[][]> signalMap;
    static HashMap<Integer, Road> roadMap;
    static HashMap<Integer, Vehicle> vehicleList = new HashMap<Integer, Vehicle>();

    static PriorityQueue<Event> eventList = new PriorityQueue<Event>(new TimestampComparator());

    public static void arrival(Event event){
        Vehicle vehicle = event.getVehicle();
        float ts = event.timestamp;
        int section = vehicle.section;
        int nextSection = section +1;
        int color = Signal.getColor(section, ts, 2, 1, signalMap);

        OutputProcessor.displayEvent(event, color);

        if(color == 0 && (roadMap.get(nextSection).length - roadMap.get(nextSection).occupiedLength > vehicle.len)) {
            float future_ts = ts + (roadMap.get(section+1).length / vehicle.velocity);
            vehicle.setSection(section+1);
            if(nextSection == 6){
                System.out.println("Depart Vehicle "+ vehicle.id+ " at ts: "+ event.timestamp);
                roadMap.get(section).vehiclesOnRoad.remove(vehicle);
                roadMap.get(section).setOccupiedLength(vehicle.len, false);
                vehicleList.remove(vehicle.id);
            }else {
                System.out.println("Vehicle "+ vehicle.id+ " moves to section "+ nextSection);
                roadMap.get(nextSection).vehiclesOnRoad.add(vehicle);
                roadMap.get(nextSection).setOccupiedLength(vehicle.len, true);
                roadMap.get(section).vehiclesOnRoad.remove(vehicle);
                roadMap.get(section).setOccupiedLength(vehicle.len, false);
                Event future_event = new Event(vehicle, future_ts);
                eventList.add(future_event);
                vehicleList.put(vehicle.id, vehicle);
            }


        }else if(color == 0 && roadMap.get(nextSection).length - roadMap.get(nextSection).occupiedLength < vehicle.len) {
            System.out.println("Section "+ nextSection + " is full! \n" );
            float future_ts = Signal.getTimeForGreenSignal(nextSection, ts, 2,1, signalMap);
            Event future_event = new Event(vehicle, future_ts);
            eventList.add(future_event);
        }else if(color==2){
           float future_ts = Signal.getTimeForGreenSignal(section, ts, 2,1, signalMap);
            //System.out.println(totalTime+" "+ timeMod+" "+ts);
            //System.out.println(future_ts);
            Event future_event = new Event(vehicle, future_ts);
            eventList.add(future_event);
        }
    }
    public static void drive(Event event){
          System.out.println("Drive:  " + event.vehicle.id + "at  section: "+ event.vehicle.section + " ts: "+ event.timestamp);
    }


    public static void main(String args[]) throws IOException {
        signalMap = InputProcessor.readSignalData("../resources/noYellowSignal.csv");
        roadMap= Road.initialiseRoadMap();

        int vehicleId =1;
        float ts =0;
        Vehicle vehicle1 = Scheduler.generateVehicle(vehicleId++, ts);
        eventList.add(new Event(vehicle1, ts));
        roadMap.get(1).vehiclesOnRoad.add(vehicle1);
        roadMap.get(1).setOccupiedLength(vehicle1.len, true);
        ts+=2;
        Vehicle vehicle2 = Scheduler.generateVehicle(vehicleId++, ts);
        eventList.add(new Event(vehicle2, ts));
        roadMap.get(1).vehiclesOnRoad.add(vehicle2);
        roadMap.get(1).setOccupiedLength(vehicle2.len, true);

        while(!eventList.isEmpty() && eventList.peek().timestamp <  260 ) {
            Event event = eventList.poll();

            if(Math.random()<0.7) {
                ts = ts + (float)(Math.random()*10);
                Event newEvent = Scheduler.generateEvent(ts, vehicleId++);
                eventList.add(newEvent);
                roadMap.get(1).vehiclesOnRoad.add(newEvent.vehicle);
                roadMap.get(1).setOccupiedLength(newEvent.vehicle.len, true);
            }
            arrival(event);
        }
    }
}
