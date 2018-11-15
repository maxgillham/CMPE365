
import numpy as np
import itertools



def wait_times(network, requests):
    #init 2 drivers starting at location 0 at time of first request
    driver_1 = Driver(network_map=network)
    driver_2 = Driver(network_map=network)

    for i in range(requests.shape[0]):

        request_time = requests[i,0]
        pickup_location = int(requests[i,1])-1
        dropoff_location = int(requests[i,2])-1

        print('\nRequest at time', request_time)
        print('~~~')
        print('Driver 1 Time', driver_1.time, 'At Location', driver_1.location)
        print('With ETA', driver_1.get_eta(pickup_location))
        print('\nDriver 2 Time', driver_2.time, 'At Location', driver_2.location)
        print('With ETA', driver_2.get_eta(pickup_location),'\n')

        #update drivers to time of request if they at prev time
        #if they are seeing request after its been made, ignore
        driver_1.update_time(request_time)
        driver_2.update_time(request_time)

        #if driver 1 can arrive at pickup location before driver 2
        if driver_1.get_eta(pickup_location) < driver_2.get_eta(pickup_location):
            driver_1.pickup(pickup_location=pickup_location, request_time=request_time)
            driver_1.dropoff(dropoff_location=dropoff_location)
        #if driver 2 can arrive at pickup_location before driver 1
        else:
            driver_2.pickup(pickup_location=pickup_location, request_time=request_time)
            driver_2.dropoff(dropoff_location=dropoff_location)

        print('\ndriver 1 late count', driver_1.late_count)
        print('driver 2 late count', driver_2.late_count)
    return driver_1.late_count + driver_2.late_count

#driver class
class Driver:
    def __init__(self, network_map):
        self.location = 0
        self.time = 0
        self.late_count = 0
        self.map = network_map

    def pickup(self, pickup_location, request_time):
        self.time += self.map[self.location][pickup_location]
        self.location = pickup_location
        if self.time > request_time: self.late_count += (self.time - request_time)
        else: self.time = request_time

    def dropoff(self, dropoff_location):
        self.time += self.map[self.location][dropoff_location]
        self.location = dropoff_location

    def get_eta(self, check_location):
        return self.map[self.location][check_location] + self.time
    
    def update_time(self, time):
        if self.time > time: return
        else: self.time = time


#floyd warshall aglorithm to optimize city network
def floyd_warshall(city_graph):
    V = range(city_graph.shape[0])
    #initialize table so nodes that are unreachable in single step are infinity, others left
    #to default weights and (i,i) entries are left at zero with a nested loop
    for row, col in itertools.product(V,V):
        if city_graph[row, col] == 0 and row != col: city_graph[row, col] = float('inf')
    #3 nested loops to find shorter paths from node to node
    for k, i, j in itertools.product(V,V,V):
        if city_graph[i,j] > city_graph[i,k] + city_graph[k,j]: city_graph[i,j] = city_graph[i,k] + city_graph[k,j]
    return city_graph

#just a csv open to numpy
def load_csv(fname):
    return np.loadtxt(open(fname, 'rb'), delimiter=',')



if __name__ == '__main__':
    #load request data and city_graph
    requests = load_csv('requests.csv')
    city_graph = load_csv('network.csv')

    #optimize city graph
    city_graph = floyd_warshall(city_graph)

    late_count = wait_times(city_graph, requests)
    print(late_count)
