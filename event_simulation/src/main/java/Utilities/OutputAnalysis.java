package main.java.Utilities;

import main.java.Engine;
import main.java.Vehicle;

import java.text.DecimalFormat;
import java.util.ArrayList;

public class OutputAnalysis {
    public static String calculateMeanTravel(ArrayList<Vehicle> result) {
        double totalTime = 0;
        double min = 1000;
        double max = 0;
        for (int i = 0; i < result.size(); i++) {
            double time_taken = (result.get(i).getEndTime() - result.get(i).getStartTime());
            totalTime += time_taken;
            if (time_taken < min) {
                min = time_taken;
            }
            if (time_taken > max)
                max = time_taken;
        }
        DecimalFormat df = new DecimalFormat("###.###");
        System.out.println("Minimum Travel Time: " + df.format(min));
        System.out.println("Maximum Travel Time : " + df.format(max));
        double meanTravelTime =totalTime / result.size();

        return df.format(meanTravelTime);

    }

    public static void printStats(ArrayList<Vehicle> result) {
        System.out.println("\n--------------- Final Statistics -------------------------------");
        System.out.println("Warm up Time : " + Engine.firstExit);
        System.out.println("Total Number of Vehicles in the system = " + Engine.vehicleId);
        System.out.println("Total number of events processed = " + Engine.eventCount);
        System.out.println("Number of vehicles exited the system = " + Engine.departedCount);
        System.out.println("Total number of events yet to be processed = " + Engine.eventList.size());
        System.out.println("# Cars for which stats are collected : " + result.size());
        System.out.println("Mean Travel Time : " + calculateMeanTravel(result));

    }
}