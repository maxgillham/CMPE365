import math
import itertools

'''
Method for question 1.  Pass this method a list and the left and right indicies you want to check for and it will
return the maximum segment sum and corresponding segment.
'''
def question_1(list, left_index, right_index):
    max_sum, max_seg = divide_conq(list, left_index, right_index, (0, 0))
    return max_sum, max_seg

'''
Method for question 2
'''
def question_2(list, left_index, right_index):
    #first get the maximal sum as before
    max_sum_1, boundry_1 = divide_conq(list, left_index, right_index, (0, 0))
    #now we have max value and the left and right boundrys
    #next, remove this sublist from the list
    list = replace_sublist(list, boundry_1)
    #now we can repeat
    max_sum_2, boundry_2 = divide_conq(list, left_index, right_index, (0, 0))
    return max_sum_1, boundry_1, max_sum_2, boundry_2


def divide_conq(list, left_index, right_index, mss_bounds):
    while left_index != right_index:
        median = math.floor((left_index + right_index)/2)
        left_child_sum, mss_bounds = divide_conq(list, left_index, median, (left_index, median))
        right_child_sum, mss_bounds = divide_conq(list, median+1, right_index, (median+1, right_index))

        left_sum = list[median - 1]
        right_sum = list[median]

        #initialize left and right sums to be individual values
        max_left = left_sum
        max_right = right_sum

        #left_bound = (left_index, right_index)
        #right_bound = (left_index, right_index)
        right_bound = mss_bounds

        range_1 = range(median - left_index - 1)
        range_2 = range(right_index - median - 1)
        for l in range_1:
            left_sum += list[l]
            if(left_sum > max_left):
                max_left = left_sum
        for r in range_2:
            right_sum += list[median + r + 1]
            if(right_sum > max_right):
                max_right = right_sum
                right_bound = (median-1, median + r + 1)
        max_sum = max(max_left + max_right, left_child_sum, right_child_sum)
        if max_left + max_right > left_child_sum and right_child_sum:
            mss_bounds = right_bound
        else:
            if right_child_sum > left_child_sum:
                mss_bounds = (median+1, right_bound[1])
            else:
                mss_bounds = (left_index, right_bound[0])
        return max_sum, mss_bounds
    return list[left_index], (left_index, right_index)

def replace_sublist(list, boundry):
    minimum_value = min(list)
    list = list[0:boundry[0]] + [minimum_value]*(boundry[1]-boundry[0]) + list[boundry[1]:]
    return list

if __name__ == '__main__':
    #test_list = [-2, 1, -3, 4, -1, 2, 1, -5, 4]
    test_list = [2, 4, 5, -7, 3, -6, 1, 4]
    #test_list = [-1, -2, -3, -4, -5, 6, -7, -8, -9]

    result, mss_bounds = question_1(test_list, 0, len(test_list) -1)
    print(result)
    print(mss_bounds)

    max_1, boundry_1, max_2, boundry_2 = question_2(test_list, left_index=1, right_index=len(test_list) -1)
    print(max_1, boundry_1,'\n',max_2, boundry_2)