import matplotlib.pyplot as plt
'''
This method is the collartz problem with an additional if statement that checks if the value of x has been executed
previosly and halted.  It accepts the initial value x and a list of numbers that have already been checked.
'''
def collartz(x, checked_num):
    count = 0
    while x != 1:
        if x in checked_num:
            break
        count += 1
        if x % 2 == 0:
            x = x/2
        else:
            x = 3*x + 1
    return count

'''
This method is an additional loop to the collartz problem, however, as i is incremented, it appends the initial value 
given to collartz previosly given to indicate it halts at whenever it is inputted.
'''
def outer_loop_with_checking(n):
    checked = []
    checked_count = []
    total_count = 0
    for i in range(n):
        count = collartz(i+1, checked)
        total_count += count
        checked.append(i)
        checked_count.append(total_count)
    return total_count

'''
This method is simaler to the outer loop with checking, but it does not append values that have previosly halted so the
if statement is never satisfied.
'''
def outer_loop_without_checking(n):
    checked = []
    total_count = 0
    for i in range(n):
        count = collartz(i+1, checked)
        total_count += count
    return total_count


if __name__ == '__main__':

    #count_checked = outer_loop_with_checking(1000)
    #print('with checking', count_checked)

    #count_not_checked = outer_loop_without_checking(10000)
    #print('without checking', count_not_checked)
    empty_list = []
    count_list = []
    init_value_list = []
    for i in range(100):
        count = collartz(i+1, empty_list)
        init_value_list.append(i+1)
        count_list.append(count)
    plt.scatter(init_value_list, count_list)
    plt.show()


