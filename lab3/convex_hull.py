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
    merge_sort_polar(x, y, bottom_point)
    stack.push((x[0], y[0]))
    stack.push((x[1], y[1]))
    for i in range(3, n-2):
        top = len(stack.items)
        angle_1 = get_polar_angle(stack.items[top-1][0], stack.items[top-1][1], stack.items[top-2])
        angle_2 = get_polar_angle(x[i], y[i], stack.items[top-1])
        if(angle_1 > angle_2):
            stack.pop()
        stack.push((x[i], y[i]))
    return stack

'''
Sort by polar angle of points with respect to the base point
'''
def merge_sort_polar(x, y, base_point):
    if len(x) > 1:

        middle = len(x)//2
        left_x = x[:middle]
        right_x = x[middle:]
        left_y = y[:middle]
        right_y = y[middle:]

        merge_sort_polar(right_x, right_y, base_point)
        merge_sort_polar(left_x, left_y, base_point)

        i = 0
        j = 0
        k = 0

        while i < len(left_x) and j < len(right_x):
            left_angle = get_polar_angle(left_x[i], left_y[i], base_point)
            right_angle = get_polar_angle(right_x[i], right_y[i], base_point)
            if left_angle < right_angle:
                x[k] = left_x[i]
                y[k] = left_y[i]
                i += 1
            else:
                x[k] = right_x[j]
                y[k] = right_y[j]
                j += 1
            k += 1
        while j < len(right_x):
            x[k] = right_x[j]
            y[k] = right_y[j]
            j += 1
            k += 1
        while i < len(left_x):
            x[k] = left_x[i]
            y[k] = left_y[i]
            i += 1
            k += 1
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
    #merge_sort_polar(x, y, (0,-6))
    #print(x)
    #plt.scatter(x, y)
    #plt.scatter(0,-6, marker='>')
    #plt.show()

    graham_scan(x, y, stack)
    #print(stack.items)
    plt.scatter(x, y, marker='.')
    convex_x = []
    convex_y = []
    for i in range(len(stack.items)):
        convex_x.append(stack.items[i][0])
        convex_y.append(stack.items[i][1])
    #print(convex_x[0:2], convex_y[0:2])
    plt.scatter(convex_x, convex_y, marker='>')

    plt.show()
