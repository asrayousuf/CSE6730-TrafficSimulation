package main.java;

public class Event {
    Vehicle vehicle;
    float timestamp;
    public Event(Vehicle vehicle, float timestamp) {
        this.vehicle = vehicle;
        this.timestamp = timestamp;
    }

    public Vehicle getVehicle() {
        return vehicle;
    }

    public void setVehicle(Vehicle vehicle) {
        this.vehicle = vehicle;
    }

    public float getTimestamp() {
        return timestamp;
    }

    public void setTimestamp(float timestamp) {
        this.timestamp = timestamp;
    }
}
