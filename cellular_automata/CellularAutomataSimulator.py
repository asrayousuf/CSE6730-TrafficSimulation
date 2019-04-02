import random
import matplotlib.pyplot as plt

def initialize(segments, max_vel, l, l_o, l_o_back):
    '''
    Segments is the number of grid points to simulate in a lane
    l is the number of grid positions to look ahead in a vehicle's lane.
    Essentially, it is a decision-making window.
    Normally, l is set to max velocity.
    l_o is a decision-making decision concerning cars ahead in the other
    lane. Again, this can be set to max velocity.
    l_o_back is decision-making window concerning cars coming from behind 
    prior to switching lanes. It can either be kept as a constant or
    varied according to both the distance and the velocity of the car behind.
    '''
    
    #initial car positions
    lane1 = [random.randint(0,1) for x in range(segments)]
    lane2 = [random.randint(0,1) for s in range(segments)]
    
    #initial velocity for cars
    vel_lane1 = [random.randint(0,max_vel) if (x !=0) else 0 for x in lane1]
    vel_lane2 = [random.randint(0,max_vel) if (x != 0) else 0 for x in lane2]
    
    #track simulation time for each car
    tt = ([0]*segments,[0]*segments) 
    travel_distribution = {} 
    
    return ((lane1, lane2),(vel_lane1, vel_lane2), max_vel, l , l_o, l_o_back, tt,travel_distribution)



def get_occupied(i):
    '''
    get indices where cars are to avoid needless computations for empty indices
    '''
    
    if i == 0:
        occupied = [x   for x in range(len(lanes[0])) if lanes[0][x] != 0]
        
    else:
        occupied = [x  for x in range(len(lanes[1])) if lanes[1][x] != 0 ]
        
    return occupied


def get_gap(i,lane):
    '''
    get distance between car and predecessor in current lane.
    Returns 0 if there is a vehicle on the bordering patch
    '''
    
    try:
        gap = lanes[lane][i+1:].index(1)
        
    except:
        gap = None     #no car ahead
        
    return gap


def get_gap_o(i,lane):
    '''
    get distance between car and predecessor in other lane
    Returns -1 if there is a car on the adjacent patch in the other lane
    '''
    
    try:
        gap = lanes[lane-1][i:].index(1) - 1
        
    except:
        gap = None #no car ahead in other lane
        
    return gap


def get_gap_o_back(i,lane):
    '''
    get distance between car and car behind in other lane.
    Returns -1 if there is a car on the adjacent patch and 0
    if there is a car immediately behind
    '''
    
    #get list of cars behind in other lane
    rev_o = lanes[lane-1][:i+1]
    rev_o.reverse()
    
    try:
        gap = rev_o.index(1) -1
        
    except:
        gap = None
        
    return gap


def update(lanes_data, velocity_data, max_vel, ttd, TDd):
    '''
    Rules for updating vehicle positions. Essentially the engine of the simulation
    '''  
    
    #get occupied cells in both lanes
    lane0_occupied = get_occupied(0)
    lane1_occupied = get_occupied(1)
    
    #copy velocity and lane data into temporary lists
    temp_vel = (velocity_data[0][:], velocity_data[1][:])
    temp_lanes = (lanes_data[:])


    def switch_lanes(i,lane):
        '''
        Rules on which cars can switch lanes.
        A car plans switching if it has to slow down in current lane
        It tries to avoid getting in other cars way in the other lane
        It also avoids bumping into its successor in the next lane
        Only switches if it can accomplish both tasks simulataneously
        Otherwise, it stays in its lane and slows down
        '''
        
        #gap to successot
        gap_o = get_gap_o(i,lane) 
        
        if gap_o != None: 
            
            # room ahead
            if gap_o > l_o: 
                gap_o_back = get_gap_o_back(i,lane)
                
                if gap_o_back != None: #car ahead and car behind
                    
                    #room behind as well
                    if gap_o_back > l_o_back: 
                        
                        #swap lane data  
                        temp_lanes[lane -1][i] = 1
                        temp_lanes[lane][i] = 0
                        
                        #swap velocity data
                        temp_vel[lane -1][i] =  temp_vel[lane][i]
                        temp_vel[lane][i] = 0
                        
                        # swap time data
                        ttd[lane - 1][i] = ttd[lane][i]
                        ttd[lane][i] = 0
                        
                    #room ahead but none behind, abort switch    
                    else: 
                        temp_vel[lane][i] = get_gap(i,lane)                     
                  
                #car ahead and none behind. Room ahead for switch though
                else: 
                    
                    #swap lane data
                    temp_lanes[lane -1][i] = 1
                    temp_lanes[lane][i] = 0
                    
                    #swap velocity data
                    temp_vel[lane -1][i] =  temp_vel[lane][i]
                    temp_vel[lane][i] = 0 
                    
                    #swap time data
                    ttd[lane - 1][i] = ttd[lane][i]
                    ttd[lane][i] = 0
            
            #car ahead and not enough room to move forward abort switch
            else:
                temp_vel[lane][i] = get_gap(i,lane)
                
         
        # no car ahead. check if car behind
        else:
            
            gap_o_back = get_gap_o_back(i,lane)
            
            #car ahead and car behind
            if gap_o_back != None: 
                
                #room ahead and behind
                if gap_o_back > l_o_back: 
                    
                    #swap lane data  
                    temp_lanes[lane -1][i] = 1
                    temp_lanes[lane][i] = 0
                    
                    #swap velocity data
                    temp_vel[lane -1][i] =  temp_vel[lane][i]
                    temp_vel[lane][i] = 0
                    
                    #swap time data
                    ttd[lane - 1][i] = ttd[lane][i]
                    ttd[lane][i] = 0
                    
                #room ahead but none form behind, abort switch    
                else: 
                    temp_vel[lane][i] = get_gap(i,lane)            

            #car ahead but none behind. Room ahead for switch though        
            else: 
                #swap lane data 
                temp_lanes[lane -1][i] = 1
                temp_lanes[lane][i] = 0
                
                #swap velocity data
                temp_vel[lane -1][i] =  temp_vel[lane][i]
                temp_vel[lane][i] = 0
                
                #swap time data
                ttd[lane - 1][i] = ttd[lane][i]
                ttd[lane][i] = 0
                
                
    
    # run updates for cars in lane 0
    for pos in lane0_occupied:
        
        #increase time spent in simulation by one
        ttd[0][pos] += 1  
        
        #rules for car ahead
        if get_gap(pos,0) != None:
            
            #accelerate if velocity less than max velocity
            if velocity_data[0][pos] < max_vel:
                temp_vel[0][pos] += 1 if temp_vel[0][pos] < max_vel else True
             
            #switch lanes if possible, else decelerate
            if temp_vel[0][pos] > get_gap(pos,0):
                switch_lanes(pos,0)

            # randomly slowing down     
            if temp_vel[0][pos] > 0 and random.random() < 0.3:
                temp_vel[0][pos] -= 1
                
        # no car ahead       
        else:
            
            #accelerate if traveling at less than max velocity
            if velocity_data[0][pos] < max_vel:
                temp_vel[0][pos] += 1
               

    #run updates for cars in lane 1
    for pos in lane1_occupied:
        
        #increment time spent in simulation for each car by 1
        ttd[1][pos] += 1
        
        # rules for car ahead
        if get_gap(pos,1) != None:
            
            #accelerate initially
            if velocity_data[1][pos] < max_vel:
                temp_vel[1][pos] += 1 if temp_vel[1][pos] < max_vel else True
               
            #switch lanes or slow down if switch impossible
            if temp_vel[1][pos] > get_gap(pos,1):
                 switch_lanes(pos,1)

            #randomly slow down vehicles        
            if temp_vel[1][pos] > 0 and random.random() < 0.3:
                temp_vel[1][pos] -= 1
                
        #rules for unobstructed lane        
        else:
            
            #accelerate if driving under speed limit
            if velocity_data[1][pos] < max_vel:
                temp_vel[1][pos] += 1
      
    
    #update velocity and vehicle position data            
    velocities = temp_vel[:]
    lanes = temp_lanes[:]
    
    #get current cell occupation data
    occupied0 = [x for x in range(len(lanes[0])) if lanes[0][x] != 0]
    occupied1 = [x for x in range(len(lanes[1])) if lanes[1][x] != 0]
    
    #position update code for cars in lane 1
    #should write this as a function going forward
    for i in occupied0:
        step = velocities[0][i]

        #rules for non-stationary cars
        if step > 0:
            
            # car remains on stretch after update
            if (i + step < len(velocities[0])):
                
                lanes[0][i + step] = 1
                velocities[0][i + step] = step
                
                ttd[0][i + step] = ttd[0][i]
                ttd[0][i] = 0
            
            #car leaves road segment after update
            else:
                
                #update exit times with velocity
                time = ttd[0][i]
                if TDd.get(time) != None:
                    TDd[time] += 1
                else:
                    TDd[time] = 1
                ttd[0][i] = 0
             
            #indicate vacation of cell by cars
            lanes[0][i] = 0
            velocities[0][i] = 0

                   
    #same comments as update for lane 0   
    for i in occupied1:
        step = velocities[1][i]
        
        if step > 0:
            
            if (i + step < len(velocities[1])):
                lanes[1][i + step] = 1
                velocities[1][i + step] = step
                
                ttd[1][i + step] = ttd[1][i]
                ttd[1][i] = 0
                
            else:
                time = ttd[1][i] 
                if TDd.get(time) != None:
                    TDd[time] += 1
                else:
                    TDd[time] = 1
                ttd[1][i] = 0
                
            lanes[1][i] = 0
            velocities[1][i] = 0
                    
        
    return(lanes,velocities,ttd,TDd)
  
if __name__ == '__main__':    
#initialize model and run simulations
    lanes, velocities, max_vel, l, l_o, l_o_back, ttd, TDd = initialize(100, 5, 5, 2, 2)

    while (get_occupied(0) or get_occupied(1)):
          lanes,velocities, ttd, TDd = update(lanes, velocities, max_vel, ttd,TDd)

    plt.figure('Distribution of exits per simulation time')
    plt.bar(TDd.keys(), TDd.values())
    plt.ylabel('cars')
    plt.xlabel('simulation time')
    plt.show()
