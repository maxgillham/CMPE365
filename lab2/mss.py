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
            recurse(list[:divide_index], sum_left, sum_right)
            recurse(list[divide_index:], sum_left, sum_right)
    return sum_left, sum_right

def get_sum(list):
    return sum(list)

if __name__ == '__main__':
    test_list = [2, 4, 5, -1, 3, -6, 1, 4]
    sum_left, sum_right = question_1(test_list, 0, 8)
    print(sum_left, sum_left)