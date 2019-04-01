package main.java.Utilities;

import main.java.Event;
import java.util.Comparator;

public class TimestampComparator implements Comparator<Event> {
    public int compare(Event e1, Event e2) {
        if (e1.getTimestamp() > e2.getTimestamp())
            return 1;
        else if (e1.getTimestamp() < e2.getTimestamp())
            return -1;
        return 0;
    }
}
