
'''
Method for question 1.  Pass this method a list and the left and right indicies you want to check for and it will
return the maximum segment sum and corresponding segment.
'''
def question_1(list, left_index, right_index):
    #set initial sum to be the sum of the entire list
    initial_sum = sum(list[left_index:right_index+1])
    #set initial sub list to be entire list
    boundry = (left_index, right_index)
    max_sum, boundry = recurse_by_endpoints(list, left_index, right_index, initial_sum, boundry)
    return max_sum, list[boundry[0]:boundry[1]]

'''
Method for question 2
'''
def question_2(list, left_index, right_index):
    #first get the maximal sum as before
    #set initial sum to be the sum of the entire list
    initial_sum = sum(list[left_index:right_index+1])
    #set initial boundries to be entire list
    initial_boundry = (left_index, right_index)
    max_sum, boundry = recurse_by_endpoints(list, left_index, right_index, initial_sum, initial_boundry)
    #now we have max value and the left and right boundrys
    #next, remove this sublist from the list
    list = replace_sublist(list, boundry)
    #now we can repeat
    return
'''
This method is very simaler to the one above.  Only difference is it returns the left and right endpoints for when 
removing the sublist in question 2
'''
def recurse_by_endpoints(list, left_index, right_index, current_greatest, boundary):
    if right_index > left_index:
        for i in range(len(list[left_index:right_index+1])):
            temp_sum = sum(list[left_index+i:right_index+1])
            if temp_sum > current_greatest:
                current_greatest = temp_sum
                boundary = (left_index+i, right_index+1)
            i += 1
        return recurse_by_endpoints(list, left_index, right_index - 1, current_greatest, boundary)
    else:
        return current_greatest, boundary


def replace_sublist(list, boundry):
    minimum_value = min(list)
    list = list[0:boundry[0]] + [minimum_value]*(boundry[1]-boundry[0]) + list[boundry[1]:]
    return list

if __name__ == '__main__':
    test_list = [-12, -2, 1, -3, 4, -1, 2, 1, -5, 4, -10]
    #max_sum, max_seg = question_1(test_list, left_index=1, right_index=9)
    #print('maximum value: ', max_sum, '\ncorresponding segment: ', max_seg)

    #question_2(test_list, left_index=1, right_index=9)

