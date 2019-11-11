# -*- coding: utf-8 -*-
"""
Created on Tue Nov  5 20:39:32 2019

@author: Sydney
"""
import numpy as np
from optimalCSP import *

def check_full_assignment(assignment):
    # check if all decision variables has been assigned to some values
    for var in decision_vars:
        if var not in assignment:
            return False, var
    return True, None

def split_on_var(assignment, non_assigned_var, csp):
    # search tree split on variables, 
    # in other words, choose successor state by picking one of unassigned var
    # and try all of its domain
    
    queue = []
    for value in csp.domains[non_assigned_var]:
        local_assignment = assignment.copy()
        local_assignment[non_assigned_var] = value
        queue.append(local_assignment)
    #print ("split", queue)
    return queue

#def sort_priority(queue, optimal_csp):
#    # sort queue from largest to smallest log probability
#    priority_queue = []
#    for assignment in queue:
#        score = optimal_csp.reward_f(assignment)
#        priority_queue.append((score, assignment))
#    
#    priority_queue = sorted(priority_queue, key=lambda x: x[0], reverse=True)
#    #print ("priority queue", priority_queue)
#
#    new_queue = []
#    for s, assign in priority_queue:
#        new_queue.append(assign)
#    return new_queue







def cda(optimal_csp,output):
    queue = [{}]
    conflicts = []
    expanded = []
    while len(queue) > 0:
        assign = queue.pop(0)
        expanded.append(assign)
        is_full_assign, non_assigned_var = check_full_assignment(assign)
        if is_full_assign:
            is_consistent, conflict = optimal_csp.backtrack_search_conflict(assign, {})
            
            print('\n\tConsistent: {} \n\tIT FOUND A FULL ASSIGNMNET {} with conflict {}'.format(is_consistent, assign,conflict))
            if is_consistent:
                print('\tIt found a full assignment that was consistent')
                return assign
            else:
                conflicts.append(conflict)
                queue,conflicts = remove_conflict(conflict, queue,output,conflicts)
#                print('Output queue at this point {}'.format(queue))
        else:
            is_resolved, unresolved_conflict = resolved_conflicts(conflicts, assign, optimal_csp)
            if is_resolved:
#                print('The intial pass that it goes through as it builds up the assignment {}'.format(assign))
                nbrs = split_on_var(assign, non_assigned_var, optimal_csp)
#                print('The neighbors are {}'.format(nbrs))
            else:
                nbrs = split_on_conflict(assign, unresolved_conflict, optimal_csp)
                print('The neighbors it found through split on conflict are {}'.format(nbrs))
            for nbr in nbrs:
                if nbr not in expanded:
                    queue.append(nbr)
#            for each in queue:  
#                print('THe current queue status  {}'.format(each))
#        print('-----------------------------------------------------')

#        queue = sort_priority(queue, optimal_csp)
    return None





def remove_conflict(conflict, queue,output,conflict_list):
    ## output needs to be true or False 
    # remove any states in Q that manifest conflict
    ### find conflict order first 
    issue=[]
    temp_issue=[]
    final_issue={}
#    print('\n----------------------------------------------------------')
#    print('remind me again what is in conflict {}'.format(conflict))
#    print('remind me again of what the prior conflcits were {}'.format(conflict_list))
    
    
    while len(issue)==0:
        for var in range(4,0,-1):
            temp_issue=[]
            str_var=str(var)
            num_var=var
            if conflict[str_var] !=output:
                while num_var>0:
                    temp_issue.append(num_var)
                    num_var=num_var-2
                if temp_issue not in conflict_list:
                    issue=temp_issue
                    break
    
#    print('the conflict it found for this case was {}'.format(issue))
#    print('the total list of conflcits at this point is {}'.format(conflict_list))
    for each in issue:
        each_string=str(each)
        final_issue[each_string]=conflict[each_string]
        
    print('FINALIZED the conflict it found for this case was {}'.format(final_issue))
#    print('the total list of conflcits at this point is {}'.format(conflict_list))    
        
    conflict_list.append(final_issue)
    
    

    
    
    new_queue = []
    for assignment in queue:
#        print('Initial assignment {}'.format(assignment))
        is_conflicted =0
        for var in assignment:
#            print('Current Var is {}'.format(var))
            if assignment[var] !=output and var in final_issue:
#                print('went here {} {}'.format(assignment[var],output))
                is_conflicted=is_conflicted+1
            elif is_conflicted>0 and var in final_issue:
                is_conflicted=is_conflicted+1
#        print('For assignment {} \n\tthe resultant estimation was {}'.format(assignment,is_conflicted))    
        if is_conflicted == len(final_issue):
#            print('The Assingments that get assigned to queue {}'.format(assignment))
            # check all conflict variable, does not conflict with assignment
            new_queue.append(assignment)
    return new_queue,conflict_list

            
def build_conflict_kernel(conflict, csp):
    kernels = {}
    # conflict: not ("1"= True and "2"=True)
    # resolve to ("1"=False) or ("2"=False)
    for var in conflict.keys():
        value = conflict[var]
        kernels[var] = []
        for other_value in csp.domains[var]:
            if other_value != value:
                # same as constraint
                # reduced down domain range
                # OR relationship, either one of value is True
                kernels[var].append({var: other_value})
    return kernels

def resolved_conflicts(conflicts, assignment, csp):
    all_constraints = []
    for conflict in conflicts:
        kernel = build_conflict_kernel(conflict, csp)
        all_constraints.append(kernel)
    
    # resolve in the sense of consistent with all_constraints
    # since we rewrite kernel into constraint

    # all satisfied: And relationship
    all_satisfied = True
    for c in all_constraints:
        # c satisfied: Or relationship
        c_satisfied = False
        for var in c.keys():
            desired_value = c[var]
            if var in assignment:
                actual_value = assignment[var]
                if desired_value == actual_value:
                    c_satisfied = True
                    break
        if not c_satisfied:
            return False, c
            
    return True, None


def split_on_conflict(assignment, unresolved_conflict, csp):
    kernel = build_conflict_kernel(unresolved_conflict, csp)
    new_queue = []
    for var in kernel.keys():
        value = kernel[var]
        local_assignment = assignment.copy()
        # self-consistent
        if var not in local_assignment:
            local_assignment[var] = value
            new_queue.append(local_assignment)
    return new_queue

# state and decision varibles as described above
state_vars = ["A", "B", "C", "D", "E", "F"]
decision_vars = ["1", "2", "3", "4"]
variables = decision_vars + state_vars

# decision variables = [True, False] represents [Normal, Stuck]
# state variables = [True, False] represents [has flow, no flow]
domains = {}
for var in variables:
    domains[var] = [True, False]
    
constraints = {}
# each state variable has constraints

# A always has flow
constraints["A"] = [{"A": True}]

# B's value is dependent on whether valve 1 is acting normal or the presence of input flow from A
constraints["B"] = [{"B":True, "1":True, "A":True}, {"B":False, "1":False}, {"B": False, "A": False}]

# C's value is dependent on whether valve 2 is acting normal or the presence of input flow from A
constraints["C"] = [{"C":False, "2":True}, {"C":True, "2":False, "A":True}]
# constraints["D"] = [{"D":True,"3":True,"B":True}, {"D":False,"3":False}, {"D":False, "B":False}]
# constraints["E"] = [{"E":False,"4":True}, {"E":True, "4":False, "C":True}]
# constraints["F"] = [{"F":True, "D":True}, {"F":True, "E":True}, {"F":False, "D":False, "E":False}]

# set output of toy example to be False to test 
# D's value is dependent on whether valve 3 is acting normal, or the presence of input flow from B
constraints["D"] = [{"D":False,"3":False}, {"D":False, "B":False}]
# E's value is dependent on whether valve 4 is acting normal, or the presence of input flow from C
constraints["E"] = [{"E":False,"4":True}]
# F has no flow, thus no flow from D and E
constraints["F"] = [{"F":False, "D":False, "E":False}]

# denote valve being open or close
states = {"1": 1, "2": 0, "3":1, "4": 0}
# denote type of valves: 0 being valve, 1 being pyro
types = {"1": 0, "2": 0, "3": 1, "4": 1}
# probility distribution table
valve_prob = [0.8, 0.1, 0.1]
pyro_prob = [0.95, 0.03, 0.02]
probs_table = [valve_prob, pyro_prob]
score_f=0; ## JUST TO INITIALIZE


optimal_csp = OptimalCSP(variables, domains, constraints, decision_vars, score_f)
output=False
result_cda = cda(optimal_csp,output)
print (result_cda)
