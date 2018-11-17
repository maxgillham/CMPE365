
import numpy as np
import itertools
import matplotlib.pyplot as plt

def wait_times_n_drivers(n, network, requests):
    
    #init wait count for all drivers to be zero
    total_wait_time = 0
    #create a list of instances of driver class
    drivers = []
    #create n instances of drivers
    for i in range(n):
        drivers.append(Driver(network_map=network))

    #loop through all requests
    for i in range(requests.shape[0]):
        
        #set request variables for ease of use
        request_time = requests[i,0]
        pickup_location = int(requests[i,1])-1
        dropoff_location = int(requests[i,2])-1

        #update time to request time for all drivers
        for i in range(n): drivers[i].update_time(request_time)
        
        #create a empty array of zeros
        eta = np.zeros(n)
        #update driver eta to pickup for each driver
        for i in range(n): eta[i] = drivers[i].get_eta(pickup_location)

        #find driver with earliest eta
        driver_index = np.argmin(eta)

        #get driver with earliest eta to pickup and dropoff
        drivers[driver_index].pickup(pickup_location=pickup_location, request_time=request_time)
        drivers[driver_index].dropoff(dropoff_location=dropoff_location)

    #count late times for each driver in request
    for i in range(n): total_wait_time += drivers[i].late_count
    #return total wait time
    return total_wait_time

def wait_times_2_drivers(network, requests):
    #init 2 drivers starting at location 0 at time of first request
    driver_1 = Driver(network_map=network)
    driver_2 = Driver(network_map=network)

    #loop through requests
    for i in range(requests.shape[0]):

        #set variables for ease of use
        request_time = requests[i,0]
        pickup_location = int(requests[i,1])-1
        dropoff_location = int(requests[i,2])-1

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

    #return sum of driver 1 and driver 2 late counts
    return driver_1.late_count + driver_2.late_count

def wait_times_1_driver(network, requests):
    
    #create instance of driver class
    driver = Driver(network_map=network)

    #iterate through all requests
    for i in range(requests.shape[0]):

        #set variables for ease of use
        request_time = requests[i,0]
        pickup_location = int(requests[i,1])-1
        dropoff_location = int(requests[i,2])-1

        #update driver time to request time
        driver.update_time(request_time)

        #pickup requestor
        driver.pickup(pickup_location, request_time)
        #dropoff requestor
        driver.dropoff(dropoff_location)
    
    #return late count for single driver
    return driver.late_count


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

#plotting method
def plot_wait_times(city_graph, requests, range_of_drivers):
    wait_times = []
    for i in range(1,range_of_drivers):
        wait_times.append(wait_times_n_drivers(i, city_graph, requests))
    plt.scatter(np.arange(1,range_of_drivers), wait_times, marker='o', c='c')
    plt.xlabel('Number of Drivers')
    plt.ylabel('Total Time Spent Waiting')
    plt.title('Time Spent Waiting for 100 Given Drivers')
    plt.show()
    return

#just a csv open to numpy
def load_csv(fname):
    return np.loadtxt(open(fname, 'rb'), delimiter=',')



if __name__ == '__main__':
    #load request data and city_graph
    requests = load_csv('requests.csv')
    city_graph = load_csv('network.csv')

    #optimize city graph
    city_graph = floyd_warshall(city_graph)

    #plot_wait_times(city_graph, requests, 100)
    late_count = wait_times_n_drivers(10,city_graph, requests)
    print(late_count)
