import math


'''
Method for question 1.  Pass this method a list and the left and right indicies you want to check for and it will
return the maximum segment sum and corresponding segment.
'''
def question_1(list, left_index, right_index):
    result = divide_conq(list, left_index, right_index)
    return result

'''
Method for question 2
'''
def question_2(list, left_index, right_index):
    #first get the maximal sum as before
    #set initial sum to be the sum of the entire list
    initial_sum = sum(list[left_index:right_index+1])
    #set initial boundries to be entire list
    initial_boundry = (left_index, right_index)
    max_sum, boundry = divide_conq(list, left_index, right_index, initial_sum, initial_boundry)
    #now we have max value and the left and right boundrys
    #next, remove this sublist from the list
    list = replace_sublist(list, boundry)
    #now we can repeat
    return


def divide_conq(list, left_index, right_index):
    if left_index == right_index:
        return list[left_index]
    median = math.floor((left_index + right_index)/2)
    left_child = divide_conq(list, left_index, median)
    right_child = divide_conq(list, median+1, right_index)

    left_sum = list[median - 1]
    right_sum = list[median]

    #initialize left and right sums to be individual values
    max_left = left_sum
    max_right = right_sum
    for i in range(median - left_index - 1):
        left_sum += list[i]
        if(left_sum > max_left):
            max_left = left_sum
    for i in range(right_index - median - 1):
        #print('RIGHT SIDE: median ', median, 'right ind ', right_index)
        right_sum += list[median + i + 1]
        if(right_sum > max_right):
            max_right = right_sum
    sum_middle = max_left + max_right
    return max(sum_middle, left_child, right_child)


def replace_sublist(list, boundry):
    minimum_value = min(list)
    list = list[0:boundry[0]] + [minimum_value]*(boundry[1]-boundry[0]) + list[boundry[1]:]
    return list

if __name__ == '__main__':
    #test_list = [-2, 1, -3, 4, -1, 2, 1, -5, 4]
    test_list = [2, 4, 5, -7, 3, -6, 1, 2]
    #test_list = [1, 2, 3, 4, 5, 6, 7, 8, 9]
    #max_sum, max_seg = question_1(test_list, left_index=1, right_index=9)
    #print('maximum value: ', max_sum, '\ncorresponding segment: ', max_seg)

    #question_2(test_list, left_index=1, right_index=9)

    #recur = [2,3,4,5,6,7,8,9]

    result = divide_conq(test_list, 0, len(test_list)-1)
    print(result)