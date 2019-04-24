
import random
import numpy as np


def initialize(cells, max_vel):
 
    tt = ([0]*cells,[0]*cells) 
    travel_distribution = {} 
    
    return (cells, max_vel, tt,travel_distribution) 
    
Lights = np.array([39, 76, 151])    
lambdas = { 102: 0.024334016393442622, 101: 0.11157156518967166,
            112: 0.01042287075640262, 123: 0.027154494783478634,
            111: 0.01273705066515709, 103: 0.01001401962747847,
            120: 0.00564652738565782, 121: 0.0061462814996926865 }

def get_occupied(lane, lanes_data):
    ''' get indices where cars are to avoid needless computations for empty indices  '''  
    occupied = [x for x in range(len(lanes_data[lane])) if lanes_data[lane][x] != 0]             
    return occupied


def get_gap(i,lane, lanes_data):
    '''get distance between car and predecessor in current lane.
       Returns 0 if there is a vehicle on the bordering patch '''    
    try:
        gap = lanes_data[lane][i+1:].index(1)       
    except:
        gap = None     #no car ahead       
    return gap


def get_gap_o(i,lane, lanes_data):
    '''get distance between car and predecessor in other lane
    Returns -1 if there is a car on the adjacent patch in the other lane '''  
    try:
        gap = lanes_data[lane-1][i:].index(1) - 1      
    except:
        gap = None #no car ahead in other lane      
    return gap


def get_gap_o_back(i,lane, lanes_data):
    ''' get distance between car and car behind in other lane.
    Returns -1 if there is a car on the adjacent patch and 0
    if there is a car immediately behind '''

    rev_o = lanes_data[lane-1][:i+1]    #get list of cars behind in other lane
    rev_o.reverse()
    
    try:
        gap = rev_o.index(1) -1      
    except:
        gap = None     
    return gap


def swap_data(data, lane, pos):
    data[lane-1][pos] = 1
    data[lane][pos] = 0
    return(data)

def swap_data_raw(data, lane, pos):
    data[lane -1][pos] = data[lane][pos]
    data[lane][pos] = 0
    return(data)


def switch_lanes(i,lane, lan_data, vel_data, ttd_data, org_data):
    
    gap_o = get_gap_o(i, lane, lan_data)    #gap to successor
    gap = get_gap(i, lane, lan_data)

    if gap_o != None: 

        # room ahead
        if gap_o > gap: 
            gap_o_back = get_gap_o_back(i,lane, lan_data)

            if gap_o_back != None:             #car ahead and car behind     
                look_back = gap_o_back + 1     # diff. between car and car behind
                lbvel = vel_data[lane-1][i-look_back] 

                #room ahead and behind
                if gap_o_back > lbvel: 
                    # swap lane, velocity and time data
                    lan_data = swap_data(lan_data, lane, i)
                    vel_data = swap_data(vel_data, lane, i)
                    ttd_data = swap_data_raw(ttd_data, lane,i)
                    org_data = swap_data_raw(org_data, lane, i)

                #room ahead but none behind, abort switch    
                else: 
                    vel_data[lane][i] = get_gap(i,lane, lan_data)                     

            #car ahead and none behind. Room ahead for switch though
            else:           
                #swap lane, velocity, and time data
                lan_data = swap_data(lan_data, lane, i) 
                vel_data = swap_data(vel_data, lane, i)
                ttd_data = swap_data_raw(ttd_data, lane, i)
                org_data = swap_data_raw(org_data, lane, i)

        #car ahead and not enough room to move forward abort switch
        else:
            vel_data[lane][i] = get_gap(i,lane, lan_data)

    # no car ahead. check if car behind
    else:       
        gap_o_back = get_gap_o_back(i,lane, lan_data)

        #car ahead and car behind
        if gap_o_back != None:        
            look_back = gap_o_back + 1       # diff. between car and car behind
            lbvel = vel_data[lane-1][i-look_back] 

            #room ahead and behind
            if gap_o_back > lbvel: 
                # swap lane, velocity and time data
                lan_data = swap_data(lan_data, lane, i)
                vel_data = swap_data(vel_data, lane, i)
                ttd_data = swap_data_raw(ttd_data, lane, i) 
                org_data = swap_data_raw(org_data, lane, i)

            #room ahead but none form behind, abort switch    
            else: 
                vel_data[lane][i] = get_gap(i,lane, lan_data)            

        #car ahead but none behind. Room ahead for switch though        
        else: 
            # swap lane, velocity and time data
            lan_data = swap_data(lan_data, lane, i)
            vel_data = swap_data(vel_data, lane, i)
            ttd_data = swap_data_raw(ttd_data, lane, i)
            org_data = swap_data_raw(org_data, lane, i)

    return (lan_data, vel_data, ttd_data, org_data)


def update_velocities(pos, lane, lanes_data, velocity_data ,ttd_data, org_data):
    
    if get_gap(pos,lane, lanes_data) != None:
            
        #accelerate if velocity less than max velocity
        if velocity_data[lane][pos] < max_vel:
            velocity_data[lane][pos] += 1
             
        #switch lanes if possible, else decelerate
        if velocity_data[lane][pos] > get_gap(pos,lane, lanes_data):
            lanes_data, velocity_data, ttd_data, org_data = switch_lanes(pos,lane, lanes_data, velocity_data, ttd_data, org_data)

        # randomly slowing down     
        if velocity_data[lane][pos] > 0 and random.random() < 0.3:
            velocity_data[lane][pos] -= 1
                
    # no car ahead       
    else:
        #accelerate if traveling at less than max velocity
        if velocity_data[lane][pos] < max_vel:
            velocity_data[lane][pos] += 1
    return (lanes_data,velocity_data, ttd_data, org_data)


def update(lanes_data, velocity_data, max_vel, ttd_data, TDd,t, org_data):
    ''' Rules for updating vehicle positions. Essentially the engine of the simulation '''  
    for lane in [0,1]:
        occupied = get_occupied(lane, lanes_data)
        for pos in reversed(occupied):
            ttd_data[lane][pos] += 1
            lanes_data, velocity_data, ttd_data, org_data = update_velocities(pos, lane, lanes_data, velocity_data, ttd_data, org_data)

    for lane in [0,1]:
        occ = get_occupied(lane, lanes_data)  
        for i in reversed(occ):
            lights, = np.where((Lights > i) & (Lights < i + velocity_data[lane][i]))
            if lights.size > 0:
                light = Lights[lights[0]]
                if NB_TR_signals(t,light) == 'red':
                    step = Lights[lights[0]] - i - 1
                else:
                    step = velocity_data[lane][i]
            else:
                step = velocity_data[lane][i]

            if step > 0:
                if (i + step < len(velocity_data[lane])):
                    lanes_data[lane][i + step] = 1
                    velocity_data[lane][i + step] = step
                    org_data[lane][i+step] = org_data[lane][i]
                    org_data[lane][i] = 0
                    ttd_data[lane][i + step] = ttd_data[lane][i]
                    ttd_data[lane][i] = 0

                else:
                    time = ttd_data[lane][i] 
                    if TDd.get(time) != None:
                        if org[lane][i] == 1:
                            TDd[time] += 1
                    else:
                        if org[lane][i] == 1:
                            TDd[time] = 1
                    ttd_data[lane][i] = 0

                lanes_data[lane][i] = 0
            velocity_data[lane][i] = 0 
   
    return(lanes_data,velocity_data,ttd_data,TDd, org_data)


def entrance_at_10th(time):
    ''' 0 is for EB traffic moving onto north; org zone 223
        1 is for NB traffic; org zone 101
        2 is for WB traffic that turns north; org zone '''  
    val = 0 if time % 71 < 8 else 1 if 8 < time % 71 < 43 else 2   
    return(val)

def NB_TL_signals(t):
    '''Signals for cars to turn left onto the corridor
        Reasoning is, if we subtract time for cars to go north at a signal
        subtract time for cars to move east and west off the corridor,
        Then half the remaining time is what is available for cars to move onto the 
        corridor by making a left turn
        No need to model left turn onto corridor at 14th'''
    green = []
#     if 42 < t % 100 < 62:
#         green.append(30)
    if 61 < t % 100 < 73:
        green.append(76)
    return(green) 


def WB_TR_signals(t):
    '''Signal turns for vehicles that need a right turn to enter corridor
    Add period need to
    Removed 80 because there were no entrances from that originating zone'''
    green = []
    if 62 < t % 100 < 82:
        green.append(39)
    return (green)


def NB_TR_signals(time,pos):
    '''Northbound TR signals
        pos == 40 is for signal at 11th
        pos == 80 is for signal at 12th
        pas == 160 is for signal at 14th
        There is no signal at 14th.
        should put in real values in the future
        '''
    if pos == 39:
        val = 'green' if time % 100 < 42 else 'red'
        return val
    if pos == 76:
        val = 'green' if time % 100 < 61 else 'red'
        return val
    if pos == 151:
        val = 'green' if time % 84 < 35 else 'red'
        return val    

    
def populate_lanes_from_10th(i, queue, lanes_data, org_data):
    
    for j in [0,1]:
        if lanes_data[j][0] == 0 and queue[i] > 0:
            lanes_data[j][0] = 1 
            org_data[j][0] = 1
            queue[i] -= 1
    return (queue,lanes_data, org_data) 


def populate_by_left_at_light(pos, queue, lanes_data, org_data):
    '''
    Cars that make a left turn at a signal to enter the system.
    Left turns are made at traffic signals at 11th and 12th street
    11th street is 122
    12th street is 121
    Nothing from 122 so we shall ignore that
    '''
#     i = 0 if pos == 30 else 1 if pos == 59 else None
    for j in [0,1]:
        if lanes_data[j][76] == 0 and queue > 0:
            lanes_data[j][76] =1
            org_data[j][76] = 2
            queue -= 1
    return (queue, lanes_data, org_data)


def populate_by_right_at_light(pos, queue, lanes_data, org_data):
    '''
    * Entrance for cars that need to make a right turn onto the corridor
    * No such entrances on 12th street so removed from the dataset
    * position 0 are entrances from 11th street
    * position 1 are entrances from 13th street
    '''
    if pos == 39:
        i = 0
            
    for j in [0,1]:
        if lanes_data[j][pos] == 0 and queue[i] > 0:
            lanes_data[j][pos] =1
            org_data[j][pos] = 2
            queue[i] -= 1
    return (queue, lanes_data, org_data)

def populate_from_others(pos,queue, lanes_data, org_data):
    '''
    * Use first queue element for entrance 111 which is at cell 85
    * Use second queue element for entrance 120 which is at cell 80
    '''
    i = 0 if pos == 109 else 1 if pos == 102 else 2
    for j in [0,1]:
        if lanes_data[j][pos] == 0 and queue[i] > 0:
            lanes_data[j][pos] =1
            org_data[j][pos] = 2
            queue[i] -= 1
    return (queue, lanes_data, org_data)



if __name__ == '__main__':    
#initialize model and run simulations
#initialize model and run simulations
    level = 1
    
    cells, max_vel, ttd, TDd = initialize(151, 3)

    lanes = ([0 for i in range(cells)], [0 for i in range(cells)])
    velocities = ([0 for i in range(cells)], [0 for i in range(cells)])
    org = ([0 for i in range(cells)], [0 for i in range(cells)])

    queue_main = np.zeros(3)
    queue_left = np.zeros(1)
    queue_right = np.zeros(1)
    queue_others = np.zeros(3)

    Arrivals_main = np.random.poisson((level*lambdas[123],level*lambdas[101],level*lambdas[102]), (900,3))
    Arrivals_LT = np.random.poisson(level*lambdas[121], 900)
    Arrivals_RT = np.random.poisson((level*lambdas[103]), 900)
    Arrivals_oth = np.random.poisson((level*lambdas[111], level*lambdas[112], level*lambdas[120]), (900,3))


    for times in range(1100):
        if times < 900:
            queue_main += Arrivals_main[times]
            queue_left += Arrivals_LT[times]
            queue_right += Arrivals_RT[times]
            queue_others += Arrivals_oth[times]
        turn = entrance_at_10th(times)

        queue_main, lanes, org = populate_lanes_from_10th(turn,queue_main,lanes, org)

        lefts = NB_TL_signals(times)
        if len(lefts) > 0:
            for left in lefts:
                queue_left, lanes, org = populate_by_left_at_light(left, queue_left,lanes, org)

        rights = WB_TR_signals(times)
        if len(rights) > 0:
            for right in rights:
                queue_right, lanes, org = populate_by_right_at_light(right, queue_right, lanes, org)

        others = [109,102,114]
        for other in others:
            queue_others, lanes, org = populate_from_others(other, queue_others, lanes, org) 
        lanes,velocities, ttd, TDd, org = update(lanes, velocities, max_vel, ttd,TDd,times, org)

    summ = 0
    num = sum(list(TDd.values()))
    for key in TDd.keys():
        summ += key*TDd[key]
    mean = summ / num
    print('number of cars that traversed the corridor are %d \n'%(num))

    print('mean travel time is %d \n'%(mean))

    print('The distribution of travel times is: ')
    for key in sorted(TDd.keys()):
        n = TDd[key]
        print('%d:'%(key)+n*'*')

    print('\n')
    for key in sorted(TDd.keys()):
        print('%s cars traversed the corridor in %d seconds'%(TDd[key], key))
