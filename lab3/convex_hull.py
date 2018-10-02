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
    top = 2
    for i in range(2, n-1):
        while(get_polar_angle(stack.items[top][0], stack.items[top][1], stack.items[top-1]) > get_polar_angle(x[i], y[i], stack.items[top])):
            stack.pop()
            top -= 1
        stack.push((x[i], y[i]))
        top += 1
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

def hull_area(cords):
    n = len(cords)
    area = 0
    for i in range(len(cords)):
        j = (i + 1) % n
        area += cords[i][0]*cords[j][1]
        area -= cords[j][0]*cords[i][1]
    area = abs(area) / 2
    return area
'''
Generate set of size n points of uniform distribution centered about the origin
'''
def generate_points_uniform(n):
    return np.random.uniform(-5, 5, n).tolist(), np.random.uniform(-5, 5, n).tolist()

'''
Plot points and convex hull around it
'''
def plot_points(x, y):
    top =len(stack.items)
    plt.scatter(x, y, marker='.', c='g')
    convex_x = []
    convex_y = []
    for i in range(top):
        convex_x.append(stack.items[i][0])
        convex_y.append(stack.items[i][1])
    plt.plot(convex_x, convex_y, linestyle='-', marker='o', c='b')
    end_point_x = []
    end_point_y =[]
    end_point_x.append(convex_x[top-1])
    end_point_x.append(convex_x[0])
    end_point_y.append(convex_y[top-1])
    end_point_y.append(convex_y[0])
    plt.plot(end_point_x, end_point_y, linestyle='-', marker='o', c='b')
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
    x, y = generate_points_uniform(5)
    graham_scan(x, y, stack)
    points = stack.items
    area = hull_area(points)
    print(area)
    plot_points(x, y)

