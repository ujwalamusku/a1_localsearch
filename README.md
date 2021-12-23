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
