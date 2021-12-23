#!/usr/local/bin/python3
# assign.py : Assign people to teams
#
# Code by: Ujwala Musku
#
# Based on skeleton code by D. Crandall and B551 Staff, September 2021
#

#Importing libraries
import sys
import pandas as pd
import numpy as np
import math
import itertools
import json
import random

def solver(input_file):
    """
    1. This function should take the name of a .txt input file in the format indicated in the assignment.
    2. It should return a dictionary with the following keys:
        - "assigned-groups" : a list of groups assigned by the program, each consisting of usernames separated by hyphens
        - "total-cost" : total cost (time spent by instructors in minutes) in the group assignment
    3. Do not add any extra parameters to the solver() function, or it will break our grading and testing code.
    4. Please do not use any global variables, as it may cause the testing code to fail.
    5. To handle the fact that some problems may take longer than others, and you don't know ahead of time how
       much time it will take to find the best solution, you can compute a series of solutions and then
       call "yield" to return that preliminary solution. Your program can continue yielding multiple times;
       our test program will take the last answer you 'yielded' once time expired.
    """
    #Parsing the input survey file
    def parse_survey(input_file):
        #input_file = str(sys.argv[0]).split("/rough")[0] + "/test1.txt"
        data = pd.read_csv(input_file, sep=" ", header=None)
        data.columns = ['student_name', 'sugg_group', 'exclude']
        data['sugg_group_count'] = data['sugg_group'].str.split("-").str.len()
        return data

    # Initializing each student's choice as an initializer to start the fringe with
    def initializer(data, i):
        initialized_list = data["sugg_group"][i].split("-")
        rev_initialized_list = []
        for element in initialized_list:
            if element not in ("xxx","zzz"):
                rev_initialized_list.append(element)
        for person in rev_initialized_list:
            for excl_per in data.loc[data['student_name'] == person]['exclude'].str.split(",").to_list()[0]:
                # print(excl_per)
                if excl_per in rev_initialized_list:
                    # print("yes")
                    rev_initialized_list.remove(person)
        return rev_initialized_list
    #Goal state - Checking the number of people assigned in teams is equal to the total number of students
    def count_people(list_f):
        person_count = 0
        for group in list_f:
            for person in group:
                person_count += 1
        return person_count
    # Calculating the cost as per the four condition given in the question
    def heuristic(groups, input_file):
        data = parse_survey(input_file)

        result = pd.DataFrame(groups)
        result.columns = ['assigned_group']
        result['assigned_group_count'] = result['assigned_group'].str.split("-").str.len()
        result['student_name'] = result['assigned_group'].str.split("-")
        result = result.explode('student_name')

        condition1 = len(groups)

        cond2 = result[['student_name', 'assigned_group_count']].merge(data[['student_name', 'sugg_group_count']],
                                                                       on='student_name', how='left')

        condition2 = (~(cond2['assigned_group_count'] == cond2["sugg_group_count"])).values.sum()

        result2 = result[['student_name', 'assigned_group']].merge(
            (data.loc[data['exclude'] != '_'][['exclude', 'student_name']]), on='student_name', how='inner')

        count_val = 0
        for student_grp in result2['exclude']:
            for student in student_grp.split(","):
                for exc_student_grp in result2.loc[result2['exclude'] == student_grp]['assigned_group']:
                    for exc_student in exc_student_grp.split('-'):
                        if student == exc_student:
                            count_val += 1
        condition4 = count_val

        result3 = result[['student_name', 'assigned_group']].merge(data[['student_name', 'sugg_group']],
                                                                   on='student_name',
                                                                   how="inner")
        count_3 = 0
        for sugg_grp in result3['sugg_group']:
            for sugg_per in sugg_grp.split('-'):
                if sugg_per not in ("xxx","zzz") and sugg_per not in \
                        ((result3.loc[result3['sugg_group'] == sugg_grp]['assigned_group'].str.split("-")).to_list())[
                            0]:
                    count_3 += 1

        condition3 = count_3
        # print(condition1,condition2,condition3,condition4)
        heuristic_val = condition1 * 5 + condition2 * 2 + condition3 * 3 + condition4 * 10
        # print(heuristic_val)
        # print(data)
        # print(groups_dict)
        return heuristic_val
    # Defining the successor in such a way that it adds a new person to the existing two or one member team or add the new person in a new team
    def successor(new_list, student, input_file,student_list):
        fringe = []
        for group in new_list:
            if len(group) < 3:
                index_val = new_list.index(group)
                succ = new_list.copy()
                added_list = group.copy()

                added_list.append(student)
                succ.remove(group)

                succ.insert(index_val, added_list)
                fringe.append(succ)
        add_succ = new_list.copy()
        add_succ.append([student])
        fringe.append(add_succ)
        # print(fringe)
        new_fringe = []
        for group in fringe:
            group_list = []
            for team in group:
                join_str = "-".join(team)
                # print(join_str)
                group_list.append(join_str)
            new_fringe.append(group_list)
        # print(new_fringe)
        heu_list = []
        for team in new_fringe:
            heu_list.append(heuristic(team,input_file))
        # print(heu_list)

        new_fringe = new_fringe[np.argmin(heu_list)]
        student_list.remove(student)


        list1 = []
        for i in range(len(new_fringe)):
            list1.append(new_fringe[i].split('-'))
        # print(list1)
        return list1, min(heu_list)

# This is a recursive function that picks the team with lowest heuristic and returns the final goal state with all members irrespective of cost value.
# Returning the low cost value team is handled later in the code.
    def final_result(list_f, data, stud_list_count, cost1, student_list):
        if count_people(list_f) == len(data):
            return list_f, cost1
        else:
            list_result, cost = successor(list_f, student_list[stud_list_count], input_file, student_list)
            return final_result(list_result, data, stud_list_count - 1, cost, student_list)

    cost1 = math.inf

    data = parse_survey(input_file)
    student_list_1 = [x for x in data['student_name'].to_list()]
    random.shuffle(student_list_1)
# All possible combinations of the students act as a starting point.
    combin = []
    for i in range(1, 4):
        combinations = [list(item) for item in itertools.combinations(student_list_1, i)]
        combin.extend(combinations)
# This loop will basically start with each combination and then keeps adding a new person to return the lowest cost team.
# We yield the present result whenever present team's cost is lower than previous team's cost. Otherwise, we dont.
# We yield result in a dictionary format.

    #for student_list3 in student_list_of_lists:
    for i in range(len(parse_survey(input_file))):
        data = parse_survey(input_file)
        combin.append(initializer(data, i))
        for new_list in combin:
            #new_list = initializer(data, i)
            #new_list = [data['student_name'][i]]
            #student_list = [x for x in student_list3 if x not in new_list]
            student_list = [x for x in data['student_name'].to_list() if x not in new_list]
            random.shuffle(student_list)
            new_list = [new_list]
            stud_list_count = len(student_list) - 1
            yielded_result, yielded_cost = final_result(new_list, data, stud_list_count, cost1,student_list)
            if yielded_cost < cost1:
                cost1 = yielded_cost
                group_list = []
                for group in yielded_result:
                    #print(group)
                    join_str = "-".join(str(x) for x in group)
                    group_list.append(join_str)
                #print(json.dumps(group_list))
                result = {"assigned-groups" : group_list, "total-cost" : int(yielded_cost)}
                yield result

# Main function which takes input into solver function and yield the output.
if __name__ == "__main__":
    if(len(sys.argv) != 2):
       raise(Exception("Error: expected an input filename"))

    #input_file = str(sys.argv[0]).split("/assign")[0] + "/test3.txt"
    #for result in solver(input_file):
    for result in solver(sys.argv[1]):
        print("----- Latest solution:\n" + "\n".join(result["assigned-groups"]))
        print("\nAssignment cost: %d \n" % result["total-cost"])

