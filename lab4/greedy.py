import numpy as np
import os

path = os.getcwd()


def question_1():
    #load data
    time1, time2 = load_data()
    #sort each set by departure time
    time_set_1 = sort_by_departure(time1)
    time_set_2 = sort_by_departure(time2)
    #compute minimum number of terminals needed
    set_1_min = greedy_terminal_count(time_set_1)
    set_2_min = greedy_terminal_count(time_set_2)
    print('Set 1: ', set_1_min, 'terminals required for 0 delays of up to 0.0 Minutes')
    print('Set 2: ', set_2_min, 'terminals required for 0 delays of up to 0.0 Minutes')
    return

def question_2(max_delay):
    #load data
    time1, time2 = load_data()
    #randomly select some flights to be late
    time_set_1, num_delays_1 = delay_flights(times=time1, max_delay=max_delay)
    time_set_2, num_delays_2 = delay_flights(times=time2, max_delay=max_delay)
    #sort by departure time
    time_set_1 = sort_by_departure(time_set_1)
    time_set_2 = sort_by_departure(time_set_2)
    #compute minimum number of terminals needed
    set_1_min = greedy_terminal_count(time_set_1)
    set_2_min = greedy_terminal_count(time_set_2)
    print('Set 1: ', set_1_min, 'terminals required for', num_delays_1, 'delays of up to', max_delay*60, 'Minutes')
    print('Set 2: ', set_2_min, 'terminals required for', num_delays_2, 'delays of up to', max_delay*60, 'Minutes')
    return set_1_min, num_delays_1, set_2_min, num_delays_2
'''
Find the minimum number of terminals needed to suit all planes arrival and departure times
'''
def greedy_terminal_count(times):
    #minimum of 1 terminal needed
    A = [1]
    #set overlap count to 0
    overlap_count = 0
    #initial flight
    k = 0
    for i in range(1, len(times)):
        #if plane i arrives after plane k departs
        if times[i, 0] >= times[k, 1]:
            #append number of terminals needed
            #this is equal to number of time intersections + 1
            A.append(overlap_count + 1)
            k = i
            overlap_count = 0
        #if plane i and plane k are at airport together
        else:
            overlap_count += 1
    A.append(overlap_count + 1)
    #the maximum of A is the minimum number of terminals required
    return max(A)

'''
Adds delays to randomly selected flights.  Delay for arrivals and departures must depend on one another because the 
amount of time between depatures and arrivals cannot increase (ie, delaying an arrival by 4 minutes and delaying a 
depature by 2 minutes means the amount of time at the airport has decreased).  Therefore arrival delay can be range from
(0, max_delay) but departure delay has to be from (arrival_delay, max_delay) 
'''
def delay_flights(times, max_delay):
    #randomly select flights to encounter a delay
    flight_status = generate_late_flights(len(times))
    for i in range(len(times)):
        #if i'th flight is delayed
        if flight_status[i]:
            arrival_delay = uniform_delay(0, max_delay)
            departure_delay = uniform_delay(arrival_delay, max_delay)
            #delay arrival and departure
            times[i, 0] += arrival_delay
            times[i, 1] += departure_delay
    return times, len(np.where(flight_status)[0])

'''
Just loads csv files into 2 np arrays for (start1,finish1) and (start2,finish2),
formated as (arrival(i), departure(i)) where i is an element of {0,1,2,...,length(start1,finish1)}
'''
def load_data():
    #go to path with data
    os.chdir(path + '/data')
    #merge into 2 arrays, each index is (start, finish) for each row in start1,start2,finish1,finsh2
    times_1 = np.dstack((np.genfromtxt('start1.csv', delimiter=','), np.genfromtxt('finish1.csv', delimiter=',')))[0]
    times_2 = np.dstack((np.genfromtxt('start2.csv', delimiter=','), np.genfromtxt('finish2.csv', delimiter=',')))[0]
    return times_1, times_2

#Sort time set by departure time, the second column
def sort_by_departure(times):
    return np.array(sorted(times, key=lambda p: p[1]))

#returns a value between min delay and max delay
def uniform_delay(min_delay, max_delay):
    return np.random.uniform(min_delay, max_delay)

#returns a list of size num_of_flights, where list[i]=True indicates flight[i] is late.
def generate_late_flights(num_of_flights):
    return np.random.choice(a=[False, True], size=num_of_flights)

if __name__ == '__main__':
    question_1()
    question_2(.25)
    question_2(.5)
    question_2(.75)
    question_2(1)




