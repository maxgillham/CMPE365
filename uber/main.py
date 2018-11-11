import os
import numpy as np


'''
Max Gillham - CMPE 365
UBER Final Project
14mfg2@queensu.ca - 10183941
'''

'''
This method gets the wait times for two uber drivers at once.  It gets all the shortest
paths at the start because I am asssuming all of nodes will need to be computed when
comparing distances to requests for each driver.  Driver 1 starts at request 0 and driver 2
begins at request 1.  At each iteration in the loop, we consider the ith request and the i+1th
request.  If driver 1 ends their previous trip closer to the starting location of request i,
in comparison to driver 2's ending location, driver 1 takes the ith request and driver 2 takes
the ith+1 trip.  This following for the opposite situation.
'''
def count_wait_times_two_drivers(city_graph, requests):
    #first and seccond don't have to wait
    wait_times = [0,0]
    #driver one starts are request 0 time
    driver_one_time = requests[0,0]
    #driver two strarts at request 1 time
    driver_two_time = requests[1,0]
    #cast to int and sub 1 for 0 indexing
    one_start_location = int(requests[0,1]) -1
    one_end_location = int(requests[0,2]) -1
    #same but for driver 2
    two_start_location = int(requests[1,1]) -1
    two_end_location = int(requests[1,2]) -1
    #just get all the shortest paths from every node to every other node at once
    computed_paths = get_all_shortest_paths(city_graph)
    #increment driver one and driver two time
    driver_one_time += computed_paths[one_start_location][one_end_location]
    driver_two_time += computed_paths[two_start_location][two_end_location]
    #set previous ending locations for each driver
    one_prev_end = one_end_location
    two_prev_end = two_end_location
    #iterate through requests by 2.  i.e. 2,4,6,8...
    for requestor in range(2, requests.shape[0]-2, 2):
        #start and end nodes for requestor i
        one_request_time = requests[requestor,0]
        one_start_location = int(requests[requestor,1]) - 1
        one_end_location = int(requests[requestor, 2]) - 1
        #start and end nodes for requestor i + 1
        two_request_time = requests[requestor+1, 0]
        two_start_location = int(requests[requestor+1,1]) - 1
        two_end_location = int(requests[requestor+1,2]) - 1
        #find who is closer to first request
        driver_one_distance = computed_paths[one_prev_end][one_start_location]
        driver_two_distance = computed_paths[two_prev_end][one_start_location]
        if driver_one_distance < driver_two_distance:
            #driver 1 takes request 1 and driver 2 takes request 2
            #increment driver 1 time and driver 2 time
            driver_one_time += driver_one_distance
            driver_two_time += computed_paths[two_prev_end][two_start_location]
            #if driver 1 late, add to wait time, else, add 0
            if driver_one_time > one_request_time:
                wait_times.append(driver_one_time - one_request_time)
            else:
                wait_times.append(0)
                #driver waits for requestor to be ready
                driver_one_time = one_request_time
            #if driver 2 is late, add to wait time, else, add 0
            if driver_two_time > two_request_time:
                wait_times.append(driver_two_time - two_request_time)
            else:
                wait_times.append(0)
                #wait for requstor
                driver_two_time = two_request_time
            #add drop off time for each driver
            driver_one_time += computed_paths[one_start_location][one_end_location]
            driver_two_time += computed_paths[two_start_location][two_end_location]
            #set previous end location_node
            one_prev_end = one_end_location
            two_prev_end = two_end_location
        else:
            #driver 2 takes request 1 and driver 1 takes request 2
            #increment driver 1 time and driver 2 time
            driver_one_time += computed_paths[one_prev_end][two_start_location]
            driver_two_time += driver_two_distance
            #if driver 1 late, add wait time, else, add 0
            if driver_one_time > two_request_time:
                wait_times.append(driver_one_time - two_request_time)
            else:
                wait_times.append(0)
                #wait for requesotr
                driver_one_time = two_request_time
            #if driver 2 late, add wait time, else, add 0
            if driver_two_time > one_request_time:
                wait_times.append(driver_two_time - one_request_time)
            else:
                wait_times.append(0)
                driver_two_time = one_request_time
            #add drop off tiems
            driver_one_time += computed_paths[two_start_location][two_end_location]
            driver_two_time += computed_paths[one_start_location][one_end_location]
            #set previous end nodes
            one_prev_end = two_end_location
            two_prev_end = one_end_location
    return wait_times

'''
Counting wait times for a single uber driver going through list.  This method checks
for shortest path calculations to avoid copmuting shortest paths for nodes that are
not reached.
'''
def count_wait_times_single_driver(city_graph, requests):
    #first person doesnt have to wait
    wait_times = [0]
    #drivers time, assume starts at first request time
    driver_time = requests[0,0]
    #cast to int and subtract 1 because indexing from 0
    start_location = int(requests[0,1])-1
    end_location = int(requests[0,2])-1
    #dictionary of shortest paths to every node from a given reference node
    computed_paths = {}
    #get shortest path from initial starting location and add to dictionary
    #so we don't have to compute it twice
    computed_paths[start_location] = shortest_path(city_graph, start_location)
    driver_time += computed_paths[start_location][end_location]
    #previous ending location to get time to arrive at next requestors start
    prev_end_location = end_location
    computed_paths[prev_end_location] = shortest_path(city_graph, start_location)
    #iterate through requests
    for requestor in range(1, requests.shape[0]):
        #start and end nodes for requestor i
        request_time = requests[requestor, 0]
        start_location = int(requests[requestor,1]) - 1
        end_location = int(requests[requestor, 2]) - 1
        #add time to get to requestor
        driver_time += computed_paths[prev_end_location][start_location]
        #if driver was late add lateness to wait_times
        if driver_time > request_time: wait_times.append(driver_time - request_time)
        #if driver was early or exactly on time
        else:
            #wait time of 0
            wait_times.append(0)
            #asssuming driver has to wait for requestor to be ready, then leave
            #at request time, so driver time is updated to request time
            driver_time = request_time

        #if we haven't computed shortest paths for this reference_node
        if start_location not in computed_paths:
            #compute and add to the dictionary
            computed_paths[start_location] = shortest_path(city_graph, start_location)
        #add time to drop off ith requestor to end location
        driver_time += computed_paths[start_location][end_location]
        #end location becomes prev_end_location
        prev_end_location = end_location
        #if we haven't used this node as reference
        if prev_end_location not in computed_paths:
            #compute and add to our dict
            computed_paths[prev_end_location] = shortest_path(city_graph, prev_end_location)
    return wait_times

'''
This method just gets the shortest path to all other nodes, for each node in the location matrix
'''
def get_all_shortest_paths(city_graph):
    #dict structure where key is start node
    computed_paths = {}
    for i in range(city_graph.shape[0]):
        computed_paths[i] = shortest_path(city_graph, i)
    return computed_paths

'''
Uses Dijkstra's algorithm to find the shortest distance to each location node, given
and initial reference node.
'''
def shortest_path(city_graph, reference_node):
    #location nodes are indexed as 0,1,2,...,49
    location_nodes = range(city_graph.shape[0])
    # assign neighbor nodes to be of distance None to represent infinity.
    unvisited = {location: float('inf') for location in location_nodes}
    #dictionary for neighbors that have been visited
    visited = {}
    #init current distance and unvisited for starting node, always 0
    current_distance = 0
    unvisited[reference_node] = 0
    #while there exists unvisited nodes
    while unvisited:
        for neighbor in location_nodes:
            #skip over neighbors that have been completely visited
            if neighbor not in unvisited: continue
            #check to make sure reference_node to neighbor is accesable
            if city_graph[reference_node, neighbor] != 0:
                #assign temp distance to current distance plus reference to neighbor dist
                temp_distance = current_distance + city_graph[reference_node, neighbor]
                #if first time reaching node or new distance is shorter than current distance
                if unvisited[neighbor] > temp_distance:
                    #update unvisited table
                    unvisited[neighbor] = temp_distance
        #move to visited
        visited[reference_node] = current_distance
        #remove from unvistied nodes
        del unvisited[reference_node]
        #end case
        if unvisited:
            #get the next reference node and distance
            reference_node, current_distance = get_next_reference_and_dist(unvisited)
    return visited

'''
Get the next reference node from all unvisited nodes that has been visited at least
once and has the smallest current weight
'''
def get_next_reference_and_dist(unvisited):
    return sorted([next_ref for next_ref in unvisited.items() if next_ref[1] != float('inf')], key = lambda x: x[1])[0]


#just a csv open to numpy
def load_csv(fname):
    return np.loadtxt(open(fname, 'rb'), delimiter=',')

if __name__ == '__main__':
    #column 0: time stamp, #column 1: start location, #column 2: finish location
    requests = load_csv('requests.csv')
    city_graph = load_csv('network.csv')
    #print('requests shape', requests.shape)
    #print('city graph shape', city_graph.shape)

    #print(shortest_path(city_graph, 0))

    wait_times = count_wait_times_single_driver(city_graph, requests)
    print(sum(wait_times))

    less_wait_times = count_wait_times_two_drivers(city_graph, requests)
    print(sum(less_wait_times))
