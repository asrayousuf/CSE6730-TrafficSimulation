package main.java.Utilities;

import java.util.Random;

public class RandomGenerator {
    public static int getPoisson(double lambda) {
        Random r = new Random();
        double L = Math.exp(-lambda);
        int k = 0;
        double p = 1.0;
        do {
            p = p * r.nextDouble();
            k++;
        } while (p > L);
        return k - 1;
    }
}
