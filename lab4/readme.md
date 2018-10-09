# CMPE 365 Lab 4
## Max Gillham - 10183941 - 14mfg2@queensu.ca

### Question 1 - Number of Gates
Given two test files, we compute the smallest number of gates required so that all the planes can arrive and depart on scheduled time.  Assuming no plane is late, I processed the csv files into two lists of 2-tuples.  Each list corresponds to either `start1.csv` and `finish1.csv` or  `start2.csv` and `finish2.csv`. For example, consider `start1.csv` and `finish1.csv`, they are now in a list:  
`(start(i),finish(i)) where i is an element of {0,1,2,...len(start1.csv)}`  
The algorithm to detect the number of gates required is as follows.
```
sort planes by arrival
A = [1]
overlap_count = 0
index = 0

for i from 1 to # of entries in csv file
    if plane i arrives after plane k leaves
        A.append(overlap_count + 1)
        index = i
        overlap_count = 0
    else
        overlap_count = overlap_count + 1
A.append(overlap_count + 1)

return maximum(A)
```

Performing such algorithm on the data provoided on Onq, I yeilded the following results.  
```
Set 1: 11 Gates required
Set 2: 12 Gates required
```

### Question 2 - Expecting Delays
The previous algorithm can be used to evaluate how the number of gates required changes with respect to delays.  To model arrival and departure delays I assumed the following:
* The amount of time between arrival and departure cannot decrease when a delay occurs
* If the arrival is delayed by `x`, then the departure must be delayed by atleast `x`
* A delay in a flight results in a delay on arrival and departure

To model potential delays in a series of flights and the effect on their arrival and departure times, I used the following idea.
```
n = maximum allowable delay
flight delays = Make a True/False list of length(# of flights)
for i=0 to # of flights
    if flight delays == True
        Flight i is delayed
        arrival delay = random number from (0 to n)
        departure delay = random number from (arrival delay to n)
```
Doing so, for any flight, the arrival time is always before the departure time and the amount of time between arrival and departure is either constant or increased when a delay occurs.  
Loading in the testing data and introducing this notion of flight delays, I yeilded the following results.

```
Set 1:  17 terminals required for 64 delays of up to 15.0 Minutes
Set 1:  16 terminals required for 62 delays of up to 30.0 Minutes
Set 1:  16 terminals required for 72 delays of up to 45.0 Minutes
Set 1:  13 terminals required for 66 delays of up to 60 Minutes

Set 2:  15 terminals required for 80 delays of up to 15.0 Minutes
Set 2:  15 terminals required for 59 delays of up to 30.0 Minutes
Set 2:  22 terminals required for 71 delays of up to 45.0 Minutes
Set 2:  12 terminals required for 67 delays of up to 60 Minutes
```
Naturally, the number of gates required increases when delays are intruduced.  Lets see what happens when we look at the plot of average number of gates with respect to allowable delay.
