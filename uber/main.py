import os
import numpy as np


def load_csv(fname):
    return np.loadtxt(open(fname, 'rb'), delimiter=',', skiprows=1)

def find_path(city_graph, start, end, path):

    #check if start and end nodes are in the city graph
    if not start in range(0, city_graph.shape[0]):
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
        if i not in path:
            if city_graph[start, i] != 0:
                #print(path)
                new_path = find_path(city_graph, i, end, path)
                if not new_path: return new_path
    return None

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

if __name__ == '__main__':
    #column 0: time stamp, #column 1: start location, #column 2: finish location
    request = load_csv('requests.csv')
    city_graph = load_csv('network.csv')

    path = []
    find_path(city_graph, 0, 5, path)

    print(path)

    #print('\n node 0', city_graph[0])
    #print('\n node 2', city_graph[2])
    #print('\n node 4', city_graph[4])
    #print('\n node 6', city_graph[6])

    distance = get_path_length(city_graph, path)
    print(distance)
