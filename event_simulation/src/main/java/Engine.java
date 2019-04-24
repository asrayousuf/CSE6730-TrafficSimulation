package main.java;

import main.java.FileOperations.InputProcessor;
import main.java.FileOperations.OutputProcessor;
import main.java.Utilities.OutputAnalysis;
import main.java.Utilities.TimestampComparator;

import java.io.FileWriter;
import java.io.IOException;
import java.text.DecimalFormat;
import java.util.*;

public class Engine {
    public static HashMap<Integer, double[][]> signalMap;
    static HashMap<Integer, Road> roadMap;
    static HashMap<Integer, Vehicle> vehicleList = new HashMap<Integer, Vehicle>();
    static ArrayList<Vehicle> result = new ArrayList<Vehicle>();
    public static PriorityQueue<Event> eventList = new PriorityQueue<Event>(100000, new TimestampComparator());
    public static int departedCount=0;
    public static double firstExit = 0;
    public static int eventCount=0;
    public static int vehicleId =0;
    public static Vehicle generateVehicle(int id, int section, double startTime){
        Vehicle vehicle = new Vehicle(id,18, 1,  1,  18, section, startTime, 0, section, -1);
        vehicleList.put(id, vehicle);
        return vehicle;
    }
    public static Event generateEvent(double currentTS, int id, int section, String eventType){
        Event event = new Event(generateVehicle(id, section, currentTS), currentTS, eventType);
        return event;
    }


    public static void runSim(int endTime){
        double ts = 0;

        SimulateTraffic.generateInitialVehicle(ts, 1);
        SimulateTraffic.generateInitialVehicle(ts, 2);
        SimulateTraffic.generateInitialVehicle(ts, 3);
        SimulateTraffic.generateInitialVehicle(ts, 4);
        SimulateTraffic.generateInitialVehicle(ts, 5);

        while(!Engine.eventList.isEmpty() && Engine.eventList.peek().timestamp <  endTime ) {
            Event event = Engine.eventList.poll();
            eventCount++;
            if(event.eventType.equals("new")){
                int section = event.vehicle.enterSection;
                SimulateTraffic.generateNewVehicle(event.timestamp, section, Engine.roadMap.get(section).lambda);
            }
            SimulateTraffic.schedule(event);

        }
        OutputAnalysis.printStats(result);
    }


    public static void main(String args[]) throws IOException {
        signalMap = InputProcessor.readSignalData("../resources/noYellowSignal.csv"); // edited vesion of signalTiming.csv with no yellow lights

        int endTime = Integer.parseInt(args[0]);
       FileWriter fw = new FileWriter("output/NGSIM.txt");
       fw.write( "iterationNumber,MeanTravelTime,WarmUpTime,CarsInSimulationCount,CarsAcrossCorridorCount"+"\n" );
        int nRuns=Integer.parseInt(args[1]);
        double totalMeanTime = 0;
        for(int i=0; i<nRuns; i++) {
            departedCount = 0;
            firstExit = 0;
            eventCount=0;
            vehicleId =0;
            roadMap= Road.initialiseRoadMap();
            runSim(endTime);
            DecimalFormat df = new DecimalFormat("###.###");
            String meanTime = OutputAnalysis.calculateMeanTravel(result);
            fw.write(i +"," + meanTime +","+Engine.firstExit+","+ Engine.vehicleId+","+result.size()+ "\n" );
            totalMeanTime += Double.parseDouble(meanTime);
            eventList.clear();
            result.clear();
            vehicleList.clear();
            roadMap.clear();
        }
        System.out.println("Average across " + nRuns + " runs= "+ (totalMeanTime)/nRuns);
       fw.close();
    }
}
