import numpy as np
import math
import matplotlib.pyplot as plt

'''
Want x values to be decending
'''
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
    #push bottom point to list
    stack.push(bottom_point)
    #remove bottom point
    x = x[:index] + x[index+1:]
    y = y[:index] + y[index+1:]
    #sort by polar cords
    x, y = sort_polar(x, y, bottom_point)
    stack.push((x[0], y[0]))
    stack.push((x[1], y[1]))
    for i in range(2, n-1):
        print('comparing point ', x[i-1], y[i-1], '\n with ', x[i], y[i])
        top = len(stack.items) - 1
        angle_1 = get_polar_angle(stack.items[top][0], stack.items[top][1], stack.items[top-1])
        angle_2 = get_polar_angle(x[i], y[i], stack.items[top])
        print(angle_1, angle_2)
        if(angle_1 > angle_2):
            stack.pop()
        stack.push((x[i], y[i]))
    return


'''
Sort points by polar angle with respect to given base point
'''
def sort_polar(x, y, base_point):
    angle_index = []
    new_order = []
    for i in range(len(x)):
        angle_index.append((i, get_polar_angle(x[i], y[i], base_point)))
    angle_index = sorted(angle_index, key=lambda p: p[1])
    for j in range(len(angle_index)):
        new_order.append(angle_index[j][0])

    return [x[k] for k in new_order], [y[l] for l in new_order]

'''
Compute polar angle in radians
'''
def get_polar_angle(x, y, base_point):
    angle = math.degrees(math.atan2(y-base_point[1], x-base_point[0]))
    if angle < 0:
        angle += 360
    return angle

'''
Generate set of size n points of uniform distribution centered about the origin
'''
def generate_points_uniform(n):
    return np.random.uniform(-5, 5, n).tolist(), np.random.uniform(-5, 5, n).tolist()

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
    x, y = generate_points_uniform(10)
    graham_scan(x, y, stack)

    plt.scatter(x, y, marker='.')
    convex_x = []
    convex_y = []
    for i in range(len(stack.items)):
        convex_x.append(stack.items[i][0])
        convex_y.append(stack.items[i][1])
    print(convex_x[0:2], convex_y[0:2])
    plt.scatter(convex_x, convex_y, marker='>')

    plt.show()

