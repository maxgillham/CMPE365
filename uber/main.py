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
    if not end in range(0, city_graph.shape[0]+1):
        print('fuckj',end)
        return None
    elif not start in range(0, city_graph.shape[0]+1):
        print(start, end)
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
I need to use dijkstra's shortest path algo
'''
def shortest_path(city_graph, reference_node):
    #location nodes connected to the reference_node
    location_nodes = [i for i in range(city_graph.shape[0]) if city_graph[reference_node, i] != 0]
    # assign neighbor nodes to be of distance None. Represents infinity.
    unvisited = {location: None for location in location_nodes}
    #dictionary for neighbors that have been visited
    visited = {}
    current_distance = 0
    unvisited[reference_node] = current_distance

    while unvisited:
        for neighbor in location_nodes:
            if neighbor not in unvisited: continue
            #if neighbor is accesable from the starting location
            if city_graph[reference_node, neighbor] != 0:
                if neighbor in unvisited:
                    temp_distance = current_distance + city_graph[reference_node, neighbor]
                #if first time reaching node or new distance is shorter than current distance
                if unvisited[neighbor] is None or unvisited[neighbor] > temp_distance:
                    #update unvisited table
                    unvisited[neighbor] = temp_distance
        visited[reference_node] = current_distance
        del unvisited[reference_node]
        if not unvisited: break
        candidates = [node for node in unvisited.items() if node[1]]
        reference_node, current_distance = sorted(candidates, key = lambda x: x[1])[0]


    print(visited)


    return visited

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
    return np.loadtxt(open(fname, 'rb'), delimiter=',')

if __name__ == '__main__':
    #column 0: time stamp, #column 1: start location, #column 2: finish location
    requests = load_csv('requests.csv')
    city_graph = load_csv('network.csv')
    #print('requests shape', requests.shape)
    #print('city graph shape', city_graph.shape)

    shortest_path(city_graph, 0)
    #print(shortest_path(city_graph, 0)[4])
    #wait_times = count_wait_times(city_graph, requests)
