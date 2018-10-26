import os
import numpy as np

def count_wait_times(city_graph, requests):
    #first person doesnt have to wait
    wait_times = [0]
    #drivers time, assume starts at first request time
    driver_time = requests[0,0]
    path = []
    find_path(city_graph, int(requests[0,1])-1, int(requests[0,2])-1, path)
    #if path exists, increment time by the amount taken to drop off requestor
    if path: driver_time += get_path_length(city_graph, path)

    #iterate though the rest of requests after dropping off requestor 0
    for i in range(1, requests.shape[0]):
        #find time to get to starting location from previous drop off location
        path = []
        find_path(city_graph, int(requests[i-1,2])-1, int(requests[i,1])-1, path)
        #if the path exists
        if path:
            driver_time += get_path_length(city_graph, path)
            wait_times.append(driver_time - requests[i,0])
        print('\n request at time ', requests[i,0], 'driver arrived at ', driver_time)
        #add time to drop off ith request to driver wait_time
        path = []
        find_path(city_graph, int(requests[i,1])-1, int(requests[i,2])-1, path)
        if path:
            driver_time += get_path_length(city_graph, path)

    return wait_times

'''
This method finds a path , if one exists , from the starting point to the
ending point.  Note that it currenly finds a path, not necessarily the fastest
path
'''
def find_path(city_graph, start, end, path):
    #check if start and end nodes are in the city graph
    if not end in range(0, city_graph.shape[0]):
        return None
    elif not start in range(0, city_graph.shape[0]):
        return None

    path.append(start)
    #if starting node is ending node and has a loop in graph, return path
    if start == end and city_graph[start, end] != 0:
        return path

    #if we can get to the end from start
    if city_graph[start,end] != 0:
        return path.append(end)

    #need to try finding end from a node connected to start
    for i in range(city_graph.shape[0]):
        #if we can access node i from start and haven't accessed this node yet
        if i not in path and city_graph[start, i] != 0:
            new_path = find_path(city_graph, i, end, path)
            if not new_path: return new_path
    return None

'''
This method gets the length of a given path in the city graph data
'''
def get_path_length(city_graph, path):
    #if a single loop path
    if len(path) == 1:
        return city_graph[path[0], path[0]]
    #initilize distance to zero
    distance = 0
    #first node in path
    prev_node = path[0]
    #iterate through nodes in the path
    for node in path[1:]:
        #increment with distance from previous node to next node in path
        distance += city_graph[prev_node, node]
        #assign previous node to current node for next increment
        prev_node = node
    return distance

#just a csv open to numpy
def load_csv(fname):
    return np.loadtxt(open(fname, 'rb'), delimiter=',', skiprows=1)

if __name__ == '__main__':
    #column 0: time stamp, #column 1: start location, #column 2: finish location
    requests = load_csv('requests.csv')
    city_graph = load_csv('network.csv')
    wait_times = count_wait_times(city_graph, requests)


    #print('\n node 0', city_graph[0])
    #print('\n node 2', city_graph[2])
    #print('\n node 4', city_graph[4])
    #print('\n node 6', city_graph[6])