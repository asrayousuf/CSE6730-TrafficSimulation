package main.java.FileOperations;

import main.java.Event;
import main.java.Vehicle;

import java.text.DecimalFormat;

public class OutputProcessor {
    public static void displayVehicleEntry(Vehicle vehicle){
        System.out.println("Vehicle "+ vehicle.getId() + " enters at timestamp " + vehicle.getStartTime());
    }

    public static void displayVehicleExit(Vehicle vehicle){
        System.out.println(" "+ vehicle.getId() + " departs at timestamp " + vehicle.getEndTime());
    }
    public static void displayEvent(Event event, int color){
        DecimalFormat df = new DecimalFormat("###.###");
        System.out.println("\nAt Time: "+ df.format(event.getTimestamp())+" seconds");
        String lightColor = color==0 ? "Green" : "Red";
        System.out.println("Traffic Light TR at intersection "+ event.getVehicle().getSection() +" is "+ lightColor);
        System.out.println("Vehicle "+ event.getVehicle().getId()+" at section "+ event.getVehicle().getSection());

    }
}
