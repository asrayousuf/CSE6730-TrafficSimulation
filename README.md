# CSE6730-TrafficSimulation

## Event-Oriented Simulation
Change directory to the 'event_simulation' folder: cd event_simulation

Compile classes: find . -name "*.java" | xargs javac

Run Command: java -cp src main.java.Engine args1
    
where args1 = Number of seconds in event time that the simulation should run. Eg. 200


## Process-Oriented Simulation - Adithya

Change directory to the 'process_simulation' folder: cd process_simulation

Run Command: python ProcessOrientedSimulator.py

Output: Warm-up time and Mean Travel Time


## Cellular Automata Simulation
Change directory into the 'cellular_automata' folder

Run command: python CellularAutomataSimulation.py

Simualation is initially populated with cars and none added afterwards

Simulation runs until all cars have exited

Output format: A histogram showing how many cars exit at each simulation step
