package main.java;

import java.util.HashMap;

public class Signal {
    public Signal(int color) {
        this.color = color;
    }

    int color; // 0-Green, 1-Yellow, 2-Red

    public static int getColor(int section, double currentTime, int direction, int movement) {
        int signalLoc =0;
        int color;
        double totalTime;
        //1-through (TH), 2 - left-turn (LT), 3 - right-turn (RT)
        //1 - east-bound (EB), 2 -north-bound (NB), 3 - west-bound (WB)
        //0-Green, 1-Yellow, 2-Red
        if(movement==1){
            signalLoc = 3;

            totalTime = Engine.signalMap.get(section)[direction-1][7];
        }else{
            totalTime = Engine.signalMap.get(section)[direction-1][6];
        }
        if(totalTime == 0){
            return 0;
        }
        double modTime = currentTime % totalTime;

        if(modTime <  Engine.signalMap.get(section)[(direction - 1)][signalLoc]){ //Assume 2 signals red and green
            color = 0;
        }else{
            color=2;
        }
        return color;
    }

    public static double getTimeForGreenSignal(int section, double currentTime, int direction, int movement) {
        int color;
        double totalTime;
        if(movement==1){
             totalTime = Engine.signalMap.get(section)[direction-1][7];
        }else{
             totalTime = Engine.signalMap.get(section)[direction-1][6];
        }
        if(totalTime == 0){
            return currentTime;
        }
        double timeMod = currentTime % totalTime;
        double future_ts = currentTime + Math.ceil(totalTime-timeMod);
        return future_ts;
    }

}
