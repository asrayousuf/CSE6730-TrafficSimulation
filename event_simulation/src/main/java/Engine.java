package main.java;

public class Scheduler {

    public static Vehicle generateVehicle(int id, float startTime){
        Vehicle vehicle = new Vehicle(id,20, 1,  1,  10, 1, startTime, 0);
        return vehicle;
    }
    public static Event generateEvent(float currentTS, int id){
        Event event = new Event(generateVehicle(id, currentTS), currentTS);
        return event;
    }
}
