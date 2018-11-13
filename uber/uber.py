
import numpy as np
from main import *


def wait_times(network, requests):
    #init 2 drivers starting at location 0 at time of first request
    driver_1 = Driver(start_location=0, start_time=10, network_map=network)
    driver_2 = Driver(start_location=0, start_time=10, network_map=network)

    for i in range(requests.shape[0]):

        request_time = requests[i,0]
        pickup_location = int(requests[i,1])-1
        dropoff_location = int(requests[i,2])-1

        print('\nRequest at time', request_time)
        print('~~~')
        print('Driver 1 Time', driver_1.time, 'At Location', driver_1.location)
        print('With ETA', driver_1.get_arival_time(pickup_location))
        print('\nDriver 2 Time', driver_2.time, 'At Location', driver_2.location)
        print('With ETA', driver_2.get_arival_time(pickup_location),'\n')

        #if driver 1 can arrive at pickup location before driver 2
        if driver_1.get_arival_time(pickup_location) < driver_2.get_arival_time(pickup_location):
            driver_1.pickup(pickup_location=pickup_location, request_time=request_time)
            driver_1.dropoff(dropoff_location=dropoff_location)
        #if driver 2 can arrive at pickup_location before driver 1
        else:
            driver_2.pickup(pickup_location=pickup_location, request_time=request_time)
            driver_2.dropoff(dropoff_location=dropoff_location)


    return driver_1.late_count + driver_2.late_count

#driver class
class Driver:
    def __init__(self, start_location, start_time, network_map):
        self.location = start_location
        self.time = start_time
        self.late_count = 0
        self.map = network_map

    def dropoff(self, dropoff_location):
        self.time += self.map[self.location][dropoff_location]
        self.location = dropoff_location

    def get_arival_time(self, check_location):
        return (self.map[self.location][check_location] + self.time)

    def pickup(self, pickup_location, request_time):
        self.time += self.map[self.location][pickup_location]
        self.location = pickup_location
        if self.time > request_time: self.late_count += (self.time - request_time)
        else: self.time = request_time

if __name__ == '__main__':
    requests = load_csv('requests.csv')
    city_graph = load_csv('network.csv')

    network = get_all_shortest_paths(city_graph)

    late_count = wait_times(network, requests)
    print(late_count)
