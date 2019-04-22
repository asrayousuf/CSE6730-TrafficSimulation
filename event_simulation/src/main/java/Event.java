package main.java;

public class Event {
    Vehicle vehicle;
    double timestamp;
    String eventType;
    public Event(Vehicle vehicle, double timestamp, String eventType) {
        this.vehicle = vehicle;
        this.timestamp = timestamp;
        this.eventType = eventType;

    }

    public Vehicle getVehicle() {
        return vehicle;
    }

    public void setVehicle(Vehicle vehicle) {
        this.vehicle = vehicle;
    }

    public double getTimestamp() {
        return timestamp;
    }

    public void setTimestamp(double timestamp) {
        this.timestamp = timestamp;
    }
}
