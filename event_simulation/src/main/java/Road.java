package main.java;

import java.util.HashMap;
import java.util.LinkedList;
import java.util.Queue;

public class Road {
    int id;
    Queue<Vehicle> vehiclesOnRoad;
    double length;
    double occupiedLength;
    double lambda;
    double exitProb;


    public Road(int id, Queue<Vehicle> vehiclesOnRoad, double length, double occupiedLength, double lambda, double exitProb) {
        this.id = id;
        this.vehiclesOnRoad = vehiclesOnRoad;
        this.length = length;
        this.occupiedLength = occupiedLength;
        this.lambda= lambda;
        this.exitProb = exitProb;
    }

    public  static HashMap<Integer, Road> initialiseRoadMap(){
        HashMap<Integer, Road> roadMap = new HashMap<Integer, Road>();
        double length = 528; //0.1 mile = 528ft
        double occupiedLength = 0; // no cars on road initially

        roadMap.put(1, new Road(1, new LinkedList<Vehicle>(), 0, occupiedLength,4.18, -1 ));
        roadMap.put(2, new Road(2, new LinkedList<Vehicle>(), 540, occupiedLength, 64.35 , 0.094));
        roadMap.put(3, new Road(3, new LinkedList<Vehicle>(), 478, occupiedLength, 42.67, 0.052));
        roadMap.put(4, new Road(4, new LinkedList<Vehicle>(), 426, occupiedLength, 68.06, 0.042));
        roadMap.put(5, new Road(5, new LinkedList<Vehicle>(), 360, occupiedLength, 10000, 0.811));
        roadMap.put(6, new Road(6, new LinkedList<Vehicle>(), 123, occupiedLength, 10000, -1.000 ));


        /*
        roadMap.put(1, new Road(1, new LinkedList<Vehicle>(), 10000, occupiedLength, ));
        roadMap.put(2, new Road(2, new LinkedList<Vehicle>(), 540, occupiedLength, 4.18 , 0.094));
        roadMap.put(3, new Road(3, new LinkedList<Vehicle>(), 478, occupiedLength, 64.35, 0.052));
        roadMap.put(4, new Road(4, new LinkedList<Vehicle>(), 426, occupiedLength, 42.67, 0.042));
        roadMap.put(5, new Road(5, new LinkedList<Vehicle>(), 360, occupiedLength, 68.06, 0.811));
        roadMap.put(6, new Road(6, new LinkedList<Vehicle>(), 123, occupiedLength, 10000, -1.000 ));
        */

/*
       // roadMap.put(1, new Road(1, new LinkedList<Vehicle>(), 10000, occupiedLength, ));
        roadMap.put(2, new Road(2, new LinkedList<Vehicle>(), 540, occupiedLength,  4.309));
        roadMap.put(3, new Road(3, new LinkedList<Vehicle>(), 478, occupiedLength, 46.25));
        roadMap.put(4, new Road(4, new LinkedList<Vehicle>(), 426, occupiedLength, 94.65));
        roadMap.put(5, new Road(5, new LinkedList<Vehicle>(), 360, occupiedLength, 58.8));
        roadMap.put(6, new Road(6, new LinkedList<Vehicle>(), 123, occupiedLength, 10000));
*/
        return roadMap;
    }
    public double getOccupiedLength() {
        return occupiedLength;
    }

    public void setOccupiedLength(double vehicleLength, boolean isEntering) {
        if(isEntering){
            this.occupiedLength = this.occupiedLength + vehicleLength;
        }else{
            this.occupiedLength = this.occupiedLength - vehicleLength;
        }

    }

    public static boolean isRoadFull(Vehicle vehicle, int nextSection){
       if( Engine.roadMap.get(nextSection).length - Engine.roadMap.get(nextSection).occupiedLength > vehicle.len){
           return false;
       }else{
           return true;
       }
    }
}
