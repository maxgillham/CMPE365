
'''
Method for question 1.  Pass this method a list and the left and right indicies you want to check for and it will
return the maximum segment sum and corresponding segment.
'''
def question_1(list, left_index, right_index):
    #set initial sum to be the sum of the entire list
    initial_sum = sum(list[left_index:right_index+1])
    #set initial sub list to be entire list
    initial_sub_list = list[left_index:right_index+1]
    max_sum, max_seg = recurse_by_endpoints(list, left_index, right_index, initial_sum, initial_sub_list)
    return max_sum, max_seg

'''
This method accepts a list, left and right indicies, a current greatest (greatest sum value), current_sub_list (the sub
list corresponding to the current greatest sum.  The method then returns the greatest segment sum and the corresponding
segment
'''
def recurse_by_endpoints(list, left_index, right_index, current_greatest, current_sub_list):
    if right_index > left_index:
        for i in range(len(list[left_index:right_index+1])):
            temp_sum = sum(list[left_index+i:right_index+1])
            if temp_sum > current_greatest:
                current_greatest = temp_sum
                current_sub_list = list[left_index+i:right_index+1]
            i += 1
        return recurse_by_endpoints(list, left_index, right_index - 1, current_greatest, current_sub_list)
    else:
        return current_greatest, current_sub_list


if __name__ == '__main__':
    test_list = [-12, -2, 1, -3, 4, -1, 2, 1, -5, 4, -10]
    max_sum, max_seg = question_1(test_list, left_index=1, right_index=10)
    print('maximum value', max_sum, 'corresponding segment', max_seg)

