package main.test.Utilities;

import main.java.Engine;
import main.java.FileOperations.InputProcessor;
import main.java.Signal;
import org.junit.Before;
import org.junit.Test;

import static org.junit.Assert.*;

public class SignalTest {
    @Before
    public void setUp() throws Exception {
        Engine.signalMap = InputProcessor.readSignalData("../resources/noYellowSignal.csv");
    }

    @Test
    public void getColor() throws Exception {
        int color = Signal.getColor(2, 100, 2, 1);
        assertEquals(0, color);
        color = Signal.getColor(3, 80, 2, 1);
        assertEquals(2, color );
    }

    @Test
    public void getTimeForGreenSignal() throws Exception {
        double futureTS = Signal.getTimeForGreenSignal(2, 50, 2, 1);
        assertEquals(96.9, futureTS, 0.4);

        futureTS = Signal.getTimeForGreenSignal(5, 60, 2, 1);
        assertEquals(80.7, futureTS, 0.4);

    }

}