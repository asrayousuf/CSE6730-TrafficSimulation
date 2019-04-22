package main.java.Utilities;

import main.java.Engine;
import main.java.Vehicle;
import java.util.ArrayList;

public class OutputAnalysis {
    public static double calculateMeanTravel(ArrayList<Vehicle> result) {
        double totalTime = 0;
        double min = 1000;
        double max = 0;
        int minVeh = 0;
        for (int i = 0; i < result.size(); i++) {
            double time_taken = (result.get(i).getEndTime() - result.get(i).getStartTime());
            totalTime += time_taken;
            //System.out.println(result.get(i).getEndTime() + " "+ result.get(i).getEndTime());
            if (time_taken < min) {
                minVeh = result.get(i).getId();
                min = time_taken;
            }
            if (time_taken > max)
                max = time_taken;
        }
        System.out.println("Vehicle with minimum travel time: " + minVeh);
        System.out.println("Minimum Travel Time: " + min);
        System.out.println("Maximum Travel Time : " + max);
        return totalTime / result.size();

    }

    public static void printStats(ArrayList<Vehicle> result) {
        System.out.println("\n--------------- Final Statistics -------------------------------");
        System.out.println("Warm up Time : " + Engine.firstExit);
        System.out.println("Total Number of Vehicles in the system = " + Engine.vehicleId);
        System.out.println("Total number of events processed = " + Engine.eventCount);
        System.out.println("Number of vehicles exited the system = " + Engine.departedCount);
        System.out.println("Total number of events yet to be processed = " + Engine.eventList.size());
        System.out.println("# Cars for which stats are collected : " + result.size());
        System.out.println("Average Travel Time : " + calculateMeanTravel(result));
    }
}