
'''
This method accepts a list, left and right indicies, a current greatest (greatest sum value), current_sub_list (the sub
list corresponding to the current greatest sum.  The method then returns the greatest segment sum and the corresponding
segment
'''
def recurse_by_endpoints(list, left_index, right_index, current_greatest, current_sub_list):
    if right_index >= left_index:
        i = 0
        while i < len(list) - right_index:
            temp_sum = get_sum(list[i:right_index+i+1])
            if temp_sum > current_greatest:
                current_greatest = temp_sum
                current_sub_list = list[i:right_index+i+1]
                print('new greatest is: ', current_greatest, 'for sublist: ', list[i:right_index+i+1])
            i += 1
        recurse_by_endpoints(list, left_index, right_index - 1, current_greatest, current_sub_list)
    else:
        return current_greatest, current_sub_list

def get_sum(list):
    return sum(list)

if __name__ == '__main__':
    test_list = [2, -4, 5, -1, 3, -6, -1, 4]
    recurse_by_endpoints(list=test_list, left_index=0, right_index=len(test_list), current_greatest=get_sum(test_list), current_sub_list=test_list)




#first attempt.  Didn't check for middle cases.  Saving for later.
'''
import math

def question_1(list, left, right):
    sub_list = list[left:right+1]
    sum_left, sum_right = recurse(sub_list, [], [])
    return sum_left, sum_right

def recurse(list, sum_left, sum_right):
    if list:
        divide_index = math.floor(len(list) / 2)
        sum_left.append(get_sum(list[0:divide_index]))
        sum_right.append(get_sum(list[divide_index:]))
        if divide_index != 0:
            print('left', list[:divide_index])
            print('right', list[divide_index:])
            recurse(list[:divide_index], sum_left, sum_right)
            recurse(list[divide_index:], sum_left, sum_right)
    return sum_left, sum_right
'''