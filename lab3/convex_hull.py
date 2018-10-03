import numpy as np
import math
import matplotlib.pyplot as plt

from statistics import mean

'''
This method produces the neccesary computation for question 1
'''
def question_1():
    number_of_points = []
    size_of_hull = []
    ratio = []
    for i in range(3, 50):
        number_of_points.append(i)
        stack = Stack()
        x, y = generate_points_uniform(i, 5)
        graham_scan(x, y, stack)
        hull_verticies = stack.items
        size_of_hull.append(len(hull_verticies))
        ratio.append((len(hull_verticies))/i)
    plt.subplot(121)
    plt.scatter(number_of_points, size_of_hull, marker='.')
    title = 'Size of Convex Hull for Uniform Points'
    plt.title(title)
    plt.xlabel('Number of Points')
    plt.ylabel('Size of Convex Hull')
    return

'''
This method performs the necessary computation for question 2
'''
def question_2():
    number_of_points = []
    size_of_hull = []
    ratio = []
    for i in range(3, 50):
        number_of_points.append(i)
        stack = Stack()
        x, y = generate_points_normal(i, 5)
        graham_scan(x, y, stack)
        hull_verticies = stack.items
        size_of_hull.append(len(hull_verticies))
        ratio.append((len(hull_verticies))/i)
    plt.subplot(122)
    plt.scatter(number_of_points, size_of_hull, marker='.')
    title = 'Size of Convex Hull for Normal Points'
    plt.title(title)
    plt.xlabel('Number of Points')
    plt.ylabel('Size of Convex Hull')
    plt.show()
    return

'''
This method performs necessary computation for question 3
'''
def question_3():
    '''
    #for first set of points
    stack = Stack()
    x, y = generate_points_uniform(10, 100)
    plt.scatter(x, y)
    graham_scan(x, y, stack)
    hull_verticies = stack.items
    #unziping, turning list of points into x list and y list
    hull_x_1, hull_y_1 = zip(*hull_verticies)
    #get center of circle
    x_center_1, y_center_1 = mean(hull_x_1), mean(hull_y_1)
    r_1 = max(np.sqrt((np.array(hull_x_1) - x_center_1)**2 + (np.array(hull_y_1) - y_center_1)**2))

    #for seccond set of points
    stack = Stack()
    x, y = generate_points_uniform(5, 10)
    plt.scatter(x, y)
    graham_scan(x, y, stack)
    hull_verticies = stack.items
    #unzip and turn into lists of x and y cords
    hull_x_2, hull_y_2 = zip(*hull_verticies)
    #get center of circle
    x_center_2, y_center_2 = mean(hull_x_2), mean(hull_y_2)
    r_2 = max(np.sqrt((np.array(hull_x_2) - x_center_2)**2 + (np.array(hull_y_2) - y_center_2)**2))
    '''

    r_1 = 2
    r_2 = 10

    x_center_1 = 1
    y_center_1 = -1

    x_center_2 = 1
    y_center_2 = 5

    fig = plt.figure()
    ax = fig.add_subplot(1,1,1)

    c_1 = plt.Circle((x_center_1, y_center_1), radius=r_1, fill=False)


    c_2 = plt.Circle((x_center_2, y_center_2), radius=r_2, fill=False)
    ax.add_patch(c_1)
    ax.add_patch(c_2)

    plt.axis('scaled')
    #now check if they intersect

    #if (r_2 - r_1)**2 <= (x_center_2 - x_center_1)**2 + (y_center_2 - y_center_1)**2 <= (r_2 + r_1)**2:
        #print('they intersect u cuck')

    if abs(r_2 + r_1) <= ((x_center_2 - x_center_1)**2 + (y_center_2 - y_center_1)**2):
        print('they intsect u pleb')

    plt.show()
    #plot_points(x, y, stack)
    return

'''
Performs Graham Scan to caluclate the convex hull, after running
the verticies of the hull are in the stack.
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

'''
Generate set of size n points of uniform distribution or guassian centered about the origin
'''
def generate_points_uniform(n, bound):
    return np.random.uniform(-bound, bound, n).tolist(), np.random.uniform(-bound, bound, n).tolist()

def generate_points_normal(n, bound):
    return np.random.normal(0, ((2*bound)^2)/4, n).tolist(), np.random.normal(0, ((2*bound)^2)/12, n).tolist()

'''
Plot points and convex hull around it
'''
def plot_points(x, y, stack):
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
    #question_1()
    #question_2()
    question_3()
