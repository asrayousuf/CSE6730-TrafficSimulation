package main.java.FileOperations;

import java.io.BufferedReader;
import java.io.File;
import java.io.FileReader;
import java.io.IOException;
import java.util.*;

public class InputProcessor {

    public static  HashMap<Integer, double[][]> readSignalData(String filePath) throws IOException{
        File file = new File(filePath);
        BufferedReader br = new BufferedReader(new FileReader(file));
        String line_str;
        String line[] = new String[20];
        int intersection_num =0;
        HashMap<Integer, double[][]> signalMap = new HashMap<Integer, double[][]>();
        /*
        * 1,[[8	1.8	1.8	30	3.8	55], [5	3.6	4.2	28	3.8	55], []]
        * 2, [[][][]]
         */
        while ((line_str = br.readLine()) != null) {

            String intervals[] = line_str.split(",");

            if(line_str.startsWith(","))
                continue;
            if(intervals[0].startsWith("Peachtree")){
                intersection_num++;
                if(intersection_num==3){ // 13th st. data not given
                    signalMap.put(intersection_num, new double[3][8]);
                    intersection_num++;
                }
                signalMap.put(intersection_num, new double[3][8]);
            }else if(intervals[0].equals("Eastbound") || intervals[0].equals("Westbound") || intervals[0].equals("Northbound")){
                double[][] lights = signalMap.get(intersection_num);
                int direction;
                double totalTurnTime=0.00;
                double totalTRTime =0.00;
                if(intervals[0].equals("Eastbound"))direction=0;
                else if(intervals[0].equals("Northbound")) direction=1;
                else direction=2;
                for(int i=0; i<3;i++){
                    if(intervals[i+1].isEmpty())
                        intervals[i+1]="0";
                    lights[direction][i] = Double.parseDouble(intervals[i+1]);
                    totalTurnTime+=lights[direction][i];
                }
                for(int i=3; i<6;i++){
                    if(intervals[i+1].isEmpty())
                        intervals[i+1]="0";
                    lights[direction][i] = Double.parseDouble(intervals[i+1]);
                    totalTRTime+=lights[direction][i];
                }
                lights[direction][6]=totalTurnTime;
                lights[direction][7]=totalTRTime;
                signalMap.put(intersection_num,lights);
            }
            else{
                continue;
            }
        }
        return  signalMap;
    }
}