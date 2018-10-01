import numpy as np
import matplotlib.pyplot as plt


def graham_scan(x, y, stack):
    #number of points
    n = len(x)
    #get bottom most point
    bottom_point = (x[0], y[0])
    index = 0
    for i in range(n):
        if y[i] < bottom_point[1]:
            bottom_point = (x[i], y[i])
            index = i
    #delete bottom point from list
    x = np.delete(x, index)
    y = np.delete(y, index)
    stack.push(bottom_point)
    stack.push((x[0], y[0]))
    stack.push((x[1], y[1]))
    for i in range(n-1):
        while 


    #print(stack.items)
    return bottom_point

'''
Generate points of uniform distribution centered about the origin
'''
def generate_points_uniform():
    return np.random.uniform(-5, 5, 10), np.random.uniform(-5, 5, 10)

'''
Plot points
'''
def plot_points(x, y):
    plt.scatter(x, y, marker='.', c='g')
    plt.show()
    return

'''
Just a class for stack object
'''
class Stack:
    def __init__(self):
        self.items = []

    def is_empty(self):
        return self.items == []

    def push(self, item):
        return self.items.append(item)

    def pop(self):
        return self.items.pop()

if __name__ == '__main__':
    stack = Stack()
    x, y = generate_points_uniform()
    graham_scan(x, y, stack)
    #plot_points(x, y)

