## Lab 2 - Maximum Segment Sum

### Question 1  

The implimentation of the proposed stategy is found by running question_1 in the attached python file.   Using this strategy,
the division portion of the algorithm provides a complexity of O(logn), and the non-nested for loop within the recursive function
indicates an additional complexity of n.  Therefore, in combination, this implementation of the maximum segment sum provides a 
completexy of O(nlogn).  
### Question 2  
A basic way to find the top 2 maximum non-overlapping segments is by first running the algorithm as normal, then replacing the 
sublist values with a lower number such that when passed back to the algorithm for the seccond computaion, the 2nd largest
segment does not contain any of the 1st largest segment, or replaced values.   This can be achieved by solving for the first segment
sum and then replacing each segment value with x, where x is the smallest number in the entire list.   This method is 2 calls of the 
algorithm which is O(nlogn), plus the replacing method where you much loop through the existing list and replace values which is O(n), making
the entire process O(2n^2logn).  
Another way this could be implemented is by insteading of replacing the list with sufficiently small values, you can remove the sublist 
from the original list, making the seccond call of the algorithm O(n-mlog(n-m)), where m is the size of the removed sublist.
