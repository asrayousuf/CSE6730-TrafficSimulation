package main.java;

import java.util.HashMap;

public class Signal {
    public Signal(int color) {
        this.color = color;
    }

    int color; // 0-Green, 1-Yellow, 2-Red

    public static int getColor(int section, float currentTime, int direction, int movement, HashMap<Integer, float[][]> signalMap) {
        int signalLoc =0;
        int color;
        float totalTime;
        //1-through (TH), 2 - left-turn (LT), 3 - right-turn (RT)
        //1 - east-bound (EB), 2 -north-bound (NB), 3 - west-bound (WB)
        //0-Green, 1-Yellow, 2-Red
        if(movement==1){
            signalLoc = 3;

            totalTime = signalMap.get(section)[direction-1][7];
        }else{
            totalTime = signalMap.get(section)[direction-1][6];
        }
        if(totalTime == 0){
            return 0;
        }
        //float totalTime = signalMap.get(intersection)[(direction-1)][7]; //[TODO] change signalMap to add total time
        float modTime = currentTime % totalTime;

        if(modTime <  signalMap.get(section)[(direction - 1)][signalLoc]){ //Assume 2 signals red and green
            color = 0;
        }else{
            color=2;
        }
        return color;
    }

    public static float getTimeForGreenSignal(int section, float currentTime, int direction, int movement, HashMap<Integer, float[][]> signalMap) {

        int color;
        float totalTime;
        if(movement==1){
             totalTime = signalMap.get(section)[direction-1][7];
        }else{
             totalTime = signalMap.get(section)[direction-1][6];
        }
        if(totalTime == 0){
            return currentTime;
        }
        float timeMod = currentTime % totalTime;
        float future_ts = currentTime + (totalTime-timeMod);
        return future_ts;
    }

}
