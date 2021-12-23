# a1-forrelease
#**Part 1: The 2021 Puzzle**

##**Initial State:** The input board that is passed in a file format.

##**Successor State:** All the combinations where you can move any of the rows or columns towards left or right. These would constitute to 20 moves. Apart from these we have 4 more possible moves that outer and inner ring of tiles clockwise and anti-clockwise. Totally, there are 24 possible moves. We make a visited list to keep a track of already visited nodes so that we don't revisit it again. 

##**Cost Function:** Each movement has a cost of 1.

##**Heuristic Function:** The number of steps(manhattan) from current state to goal state for each cell. Additionally, to manage edge cases such as corners, we are converting 4 steps to 1 step and 3 steps to 2 steps.

##**Functions defined:**
Left - Based on the number of row we want to move left, we move all the elements by 1 step, hence 5th element of nth row becomes 1st element in the same row.
Right - Based on the number of row we want to move right, we move all the elements by 1 step, hence 1st element of nth row becomes 5th element in the same row.
Up - Based on the number of column, we want to move upwards, we move all the elements by 1 step, hence 1st element becomes the 5th element in the same row.
Down - Based on the number of column, we want to move downwards, we move all the elements by 1 step, hence 5th element becomes the 1st element in the same column.
Outer (Clockwise & Counterclockwise): The outer elements move clockwise/counter clockwise by one step each. 
Inner (Clockwise & Counterclockwise): The inner elements move clockwise/counter clockwise by one step each.

##**Goal State:**
The board with numbers in a sequence such as below for a 5X5 board.

1 |2 |3 |4 |5 |

6 |7 |8 |9 |10|

11|12|13|14|15|

16|17|18|19|20|

21|22|23|24|25|

##**Implementation:** We implemented A* search algorithm. Used heap fringe to pop the value that has lowest sum of heuristic value and cost function. This will inturn return the number of moves we took to reach the goal.

##**Challenges:** We took time to come up with an admissable heuristic function. We tried difference of goal position to present position, number of misplaced tiles, and manhattan distance. After discussing with team and brainstorming, we figured out that a combination of manhattan distance with slight modification to manage edge cases as mentioned above gave us the optimal solution.

##**Questions asked**

1.In this problem, what is the branching factor of the search tree?
The branching factor of the search tree is 24 since we have 5 rows and 5 columns with movements up,down,left,right - that consitutes to 20. Rest 4 are the inner and outer tiles moving clockwise and counter clockwise. Together, it constitutes to 24.


2.If  the  solution  can  be  reached  in  7  moves,  about  how  many  states  would  we  need  to  explore  before  we found it if we used BFS instead of A* search?  A rough answer is fine.
Considering the depth of the tree is "d while implementing BFS. The number of states would be 24^d which is not optimal.


#**Part 2: Road Trip!**

##**Initial State:** The city where one is starting from (specified in the first argument).

##**Goal State:** The city where one wants to reach (specified in the second argument).

##**State Space**
The state space is the set of all locations given in the data set.

##**Succesor Function**
The succesor function works by taking the current city and outputing all possible places that are directly connected to this city along with the length speed limit and the segment name for all segments.

##**Heuristic Function:**
Distance - Shortest distance from start to destination city. We are using Haversine distance(great-circle distance) to calculate the shortest distance between two co-ordinates on earth(sphere like structure). If coordinate for some intermediate point does not exist, then, we are considering the optimistic situation and subtracting the length of the segment from the previous city's hueristic. This heuristic is admissible because the haversine distance between two coordinates will always be shorter than the distance of the path taken to reach the goal.
Time - Quickest(lower time) from start to destination city. We are using the same haversine distance and dividing it by the maximum speed limit possible in the entire given dataset to calculate the time.If coordinate for some intermediate point does not exist, then we are considering an optimistic situation and subtracting the minimum possible time (ie (length of current segment/Max Speed) from the previous city's heuristic. This heuristic is admissible because we are always considering the max speed possible in the dataset to calculate the time heuristic, therefore the heuristic value will be less than the time taken to travel the actual path taken to the goal.
Segments - Lowest number of segments(edges of the graph) from start city to destination city. We calculate the lowest possible number of segments by dividing the haversine distance between the two points by the max distance from the data set. If coordinate for some intermediate point does not exist, then we are considering an optimistic situation and subtracting the length of the segment from the haversine distance and then dividing the result by the max distance. This heuristic is admissible because we are considering the maximum distance from the data set to estimate the number of segments required to reach the goal in this heuristic and therefore the actual number of segments will always be more than the heuristic value.
Delivery - same as time heuristic. The time heuristic is admissible for the delivery cost because the delivery cost according to its definition is always higher or equal to the time cost therefore, since the time heuristic is admissible for the time cost it is also admissible for the delivery cost.

##**Cost Function (Edge Weights)**
Distance-It is calculated as sum of length of each segment in the current path
Time- It is calculated as sum of time taken to travel each segment in the current path. Time is calculated by distance/Speed limit of the segment
segments-It is the length of the route
delivery-It is calculated as t_road + p.2.()t_road + t_trip, where t_road is the time it takes to drive the length of the segment and t_trip is the time it takes to reach the current segment from the start city and p=tanh(l/1000) where l is the length of the currrent segment if speed limit of the current limit is more than or equal to 50, otherwise p=0.

##**Implementation:** 
We are using A * search algorithm and using heapq to pop the highest priority node having the lowest cost f(s) = g(s) + h(s), where g(s) is equal to path cost till the current node and h(s) is the heuristic from the current node to the goal. We have coded seperate functions that calculates the heuristic for each of the given conditions - distance, time, segments and we used the time heuristic for delivery as well. The algorithm starts with the heapqueue having the starting node along with its current cost (f). We run the algorithm until the heapqueue is empty or till we encounter the goal node popped from the heapqueue. We pop the highest priority node from the heapqueue, then the algorithm finds the list of all the successors to the node. If the successor is not visited, it is added to the heapqueue along with its cost f. On reaching the goal node, we calculate all the costs for the resultant path and return them in a dictionary.

##**Prolem faced**
The most difficult problem faced was there were no test cases to check the validity of the code. We had to make our own test cases and we tried optimising the cost on our test cases as best as possible.



#**Part 3: Choosing teams**

##**Initial State:** 

All combinations of student teams with one, two and, three students each.
Let's say there are 3 students say abc,def,ghi. The initial state is going be all combinations one till three students - [[abc],[def],[ghi],[abc,def],[abc,ghi],[def,ghi],[abc,def,ghi]]

##**Successor State:**

The possible combinations of students from present state which has lower cost(# of hours) when compared to previous state.

##**Cost Function:**

1. Time spent to grade each assignment for each team : Total number of teams * 5 minutes
2. Time taken to read complaints of students who were assigned to different group count instead of what they asked for: Total number of students who were assigned to other group count * 2 minutes  
3. Time taken to include the possible academic integrity cases between students who were not assigned to teams they requested for: Total number of students who were assigned to different people than they requested for * (0.05*60) minutes
4. Time taken to deal with complaints who were assigned to someone they requested not to work with : Total number of students who were assigned to someone they requested not to work with * 10 minutes

Final cost is sum of condition 1, Condition 2, Condition 3, and Condition 4

##**Goal State:**

The successor state with least cost function and all the team members in the final assigned group.

##**Implementation:**

##**Local Search Algorithm**

1. With the initial state as all possible 1 to 3 student combinations of all the students in the survey.
2. Then I created a cost function that calculates the time spent of a particular assigned teams.
3. Created a successor function in such a way that it adds new student in all possible locations (add a student if it is a team of 1 or 2 and add a student in another group).
4. For each combination in the initial state, we are calculating the cost function and adding the next student as per the successor function. Then I'm passing that list to cost function to return the lowest cost groups. We run this recursively till all the students are added to the group of teams.
5. We yield this result only if it is lower than the previous result cost.
6. Similarly, after we run for one combination in initial state, we keep running for all combinations and yield the group of teams with lowest cost.

##**Difficulties Faced:**

Initially I used initial state as all the suggestions from each user. But the initial state has too less groups to return a possible optimal cost. Later, I brainstormed, discussed and finalized that all possible combinations with a minimum limit of atleast one student and maximum limit of three students would increase our initial state. I implemented that and it started giving me better solutions.
