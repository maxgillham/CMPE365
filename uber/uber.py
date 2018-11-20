
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
        #initialize each to random location node
        drivers.append(Driver(starting_location=np.random.choice(50), network_map=network))

    #create a empty array of zeros to initialize eta to next request
    eta = np.zeros(n)

    #loop through all requests
    for i in range(requests.shape[0]):

        #set request variables for ease of use
        request_time = requests[i,0]
        pickup_location = int(requests[i,1])-1
        dropoff_location = int(requests[i,2])-1

        #increment request to pickup_location counter
        #hotspot[pickup_location] += 1

        #update time to request time for all drivers
        for i in range(n): drivers[i].update_time(request_time)

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
    driver_1 = Driver(starting_location=0, network_map=network)
    driver_2 = Driver(starting_location=0, network_map=network)

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
    driver = Driver(starting_location=0, network_map=network)

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
    #driver has variables location, time, late_count
    def __init__(self, starting_location, network_map):
        self.location = starting_location
        self.time = 0
        self.late_count = 0
        self.map = network_map

    #this method updates driver time, location and increments late_count if late
    def pickup(self, pickup_location, request_time):
        self.time += self.map[self.location][pickup_location]
        self.location = pickup_location
        if self.time > request_time: self.late_count += (self.time - request_time)
        else: self.time = request_time

    #this method increments time and location for a dropoff
    def dropoff(self, dropoff_location):
        self.time += self.map[self.location][dropoff_location]
        self.location = dropoff_location

    #this method gets time of arrival if driver goes to location
    def get_eta(self, check_location):
        return self.map[self.location][check_location] + self.time

    #this method updates time of driver to time of request unless driver currently
    #on trip
    def update_time(self, time):
        if self.time > time: return
        else: self.time = time

    #if a driver isn't chosen to pickup a requestor and not currently on a trip
    #update time and location to some given wait location
    def wait(self, time, wait_location):
        if self.time > time: return
        else:
            self.time += self.map[self.location][wait_location]
            self.location = wait_location


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
    plt.title('Time Spent Waiting for 100 Given Drivers Initilized Randomly')
    plt.show()
    return

#just a csv open to numpy
def load_csv(fname):
    return np.genfromtxt(fname, delimiter=',')

#sort locations by sum of distances to all other locations
def sort_by_centrality(city_graph):
    locations = range(50)
    return sorted(locations, key=lambda x: sum(city_graph[x]))


if __name__ == '__main__':
    #load request data and city_graph
    #requests = load_csv('supplementpickups.csv')
    requests = load_csv('requests.csv')
    city_graph = load_csv('network.csv')

    #optimize city graph
    city_graph = floyd_warshall(city_graph)

    print(sort_by_centrality(city_graph))
    #plot_wait_times(city_graph, requests, 100)
    #print('late_count for 1 driver', wait_times_1_driver(city_graph, requests))
    #print('late count for 2 drivers', wait_times_2_drivers(city_graph, requests))
    #print('late count for 10 drivers', wait_times_n_drivers(50,city_graph, requests))
