# CSE6730-TrafficSimulation

## Event-Oriented Simulation
Change directory to the 'event_simulation' folder: cd event_simulation

Compile classes: find . -name "*.java" | xargs javac

Run Command: java -cp src main.java.Engine args1
    
where args1 = Number of seconds in event time that the simulation should run. Eg. 200


## Process-Oriented Simulation - Adithya

Change directory to the 'process_simulation' folder: cd process_simulation

Run Command: python ProcessOrientedSimulator.py

Output Format: (Car, Timestamp, Event) for each event occuring

    START and FINISH remarks in Event string indicate each car process starting and completing the stretch of road the simulator focuses on for the checkpoint


## Cellular Automata Simulation
Change directory into the 'cellular_automata' folder

Run command: python CellularAutomataSimulation.py
