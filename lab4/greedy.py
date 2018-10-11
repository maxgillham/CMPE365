import numpy as np
import os
import random
import itertools
import matplotlib.pyplot as plt

from mpl_toolkits.mplot3d import Axes3D

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
    #randomly select fraction of flights to be late
    late_fraction = np.random.uniform(0, 1)
    time_set_1, num_delays_1 = delay_flights(times=time1, max_delay=max_delay, late_fraction=late_fraction)
    time_set_2, num_delays_2 = delay_flights(times=time2, max_delay=max_delay, late_fraction=late_fraction)
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
def greedy_overlap_count(times):
    k = 0
    A = []
    for i in range(1, len(times)):
        if times[i][0] > times[k][1]:
            k = i
        else:
            A.append(times[i])
    return A

def greedy_terminal_count(times):
    gate = 0
    A = greedy_overlap_count(times)
    while(len(A) > 2):
        A  = greedy_overlap_count(A)
        gate += 1
    return gate

'''
Adds delays to randomly selected flights.  Delay for arrivals and departures must depend on one another because the 
amount of time between depatures and arrivals cannot increase (ie, delaying an arrival by 4 minutes and delaying a 
depature by 2 minutes means the amount of time at the airport has decreased).  Therefore arrival delay can be range from
(0, max_delay) but departure delay has to be from (arrival_delay, max_delay) 
'''
def delay_flights(times, max_delay, late_fraction):
    flight_status = generate_late_flights(late_fraction, len(times))
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
def generate_late_flights(fraction, num_of_flights):
    selected_indicies = random.sample(range(0, num_of_flights), int(fraction*num_of_flights))
    return np.isin(range(0, num_of_flights), selected_indicies)

def make_plots():

    num_gate_3d = []
    delay_3d = []
    fraction_3d = []

    allowable_delay = [.1, .2, .3, .4, .5, .6, .7, .8, .9, 1]
    late_fraction = [.1, .2, .3, .4, .5, .6, .7, .8, .9, 1]

    #for 3d plot
    for j, i in itertools.product(allowable_delay, late_fraction):
        time1, time2 = load_data()
        time1, num_delay = delay_flights(time1, max_delay=j, late_fraction=i)
        time1 = sort_by_departure(time1)
        num_gate_3d.append(greedy_terminal_count(time1))
        delay_3d.append(j)
        fraction_3d.append(i)

    fig = plt.figure()
    ax = fig.add_subplot(121, projection='3d')
    ax.scatter(delay_3d, fraction_3d, num_gate_3d, marker='o')
    ax.set_xlabel('Allowable Delay')
    ax.set_ylabel('Fraction of Late Flights')
    ax.set_zlabel('Number of Gates Required')

    plt.show()

    num_gate_delay = []

    #keeping late fraction to be 50 percent
    for j in allowable_delay:
        time1, time2 = load_data()
        time1, num_delay = delay_flights(time1, max_delay=j, late_fraction=.5)
        time1 = sort_by_departure(time1)
        num_gate_delay.append(greedy_terminal_count(time1))

    plt.scatter(allowable_delay, num_gate_delay, marker='o')
    plt.xlabel('Allowable Delay')
    plt.ylabel('Number of Gates Required')
    plt.title('Number of Gates for Allowable Delay, Late Fraction Constant (0.5)')
    plt.show()

    num_gate_fraction = []

    return

if __name__ == '__main__':
    question_1()
    #question_2(.25)
    #question_2(.5)
    #question_2(.75)
    #question_2(1)

    #make_plots()

    #check_for_noah = np.array([[0, 3], [2, 4], [3, 4.5], [2.5, 6]])
    #check_for_noah = sort_by_departure(check_for_noah)
    #minimum_noah = greedy_terminal_count(check_for_noah)
    #print(minimum_noah)




