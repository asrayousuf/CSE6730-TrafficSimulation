package main.java;

import java.util.HashMap;
import java.util.LinkedList;
import java.util.Queue;

public class Road {
    int id;
    Queue<Vehicle> vehiclesOnRoad;
    float length;
    float occupiedLength;
    Signal signalTR;
    Signal signalLT;


    public Road(int id, Queue<Vehicle> vehiclesOnRoad, float length, float occupiedLength) {
        this.id = id;
        this.vehiclesOnRoad = vehiclesOnRoad;
        this.length = length;
        this.occupiedLength = occupiedLength;
        this.signalTR = signalTR;
        this.signalLT = signalLT;
    }

    public  static HashMap<Integer, Road> initialiseRoadMap(){
        HashMap<Integer, Road> roadMap = new HashMap<Integer, Road>();
        float length = 100; //0.1 mile = 528ft
        float occupiedLength = 0; // no cars on road initially

        roadMap.put(1, new Road(1, new LinkedList<Vehicle>(), length, occupiedLength));
        roadMap.put(2, new Road(2, new LinkedList<Vehicle>(), length, occupiedLength ));
        roadMap.put(3, new Road(3, new LinkedList<Vehicle>(), length, occupiedLength));
        roadMap.put(4, new Road(4, new LinkedList<Vehicle>(), length, occupiedLength));
        roadMap.put(5, new Road(5, new LinkedList<Vehicle>(), length, occupiedLength));
        roadMap.put(6, new Road(6, new LinkedList<Vehicle>(), length, occupiedLength));
        return roadMap;
    }
    public float getOccupiedLength() {
        return occupiedLength;
    }

    public void setOccupiedLength(float vehicleLength, boolean isEntering) {
        if(isEntering){
            this.occupiedLength = this.occupiedLength + vehicleLength;
        }else{
            this.occupiedLength = this.occupiedLength - vehicleLength;
        }

    }

    public static boolean isRoadFull(HashMap<Integer, Road> roadMap, int section){
       if( roadMap.get(section).length > roadMap.get(section).occupiedLength){
           return true;
       }else{
           return false;
       }
    }
}
