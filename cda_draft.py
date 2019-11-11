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
    return queue

def sort_priority(queue, optimal_csp):
    # sort queue from largest to smallest log probability
    priority_queue = []
    for assignment in queue:
        score = optimal_csp.reward_f(assignment)
        priority_queue.append((score, assignment))
    
    priority_queue = sorted(priority_queue, key=lambda x: x[0], reverse=True)
    #print ("priority queue", priority_queue)

    new_queue = []
    for s, assign in priority_queue:
        new_queue.append(assign)
    return new_queue


def cda(optimal_csp,output, states):
    queue = [{}]
    conflicts = []
    expanded = []
    while len(queue) > 0:
        assign = queue.pop(0)
        expanded.append(assign)
        is_full_assign, non_assigned_var = check_full_assignment(assign)
        if is_full_assign:
            csp_assignment = optimal_csp.backtrack_search(assign)
            
            if csp_assignment is not None:
                print('\tIt found a full assignment that was consistent')
                return assign
            else:
                queue,conflicts = remove_conflict(assign, queue,output,conflicts, states)
##                print('Inconsistent, Output queue at this point {} with conflicts {}'.format(queue, conflicts))
        else:
            is_resolved, unresolved_conflict = resolved_conflicts(conflicts, assign, optimal_csp)
            if is_resolved:
                nbrs = split_on_var(assign, non_assigned_var, optimal_csp)
                #print('Conflict resolved with assign {}, The neighbors are {}'.format(assign, nbrs))
            else:
                nbrs = split_on_conflict(assign, unresolved_conflict, optimal_csp)
##                print ("Conflict not resolved: {}, with assign: {}".format(unresolved_conflict, assign))
##                print('The neighbors it found through split on conflict are {}'.format(nbrs))
            for nbr in nbrs:
                if nbr not in expanded:
                    queue.append(nbr)

        queue = sort_priority(queue, optimal_csp)
    return None





def remove_conflict(conflict, queue,output,conflict_list, states):
    ## output needs to be true or False 
    # remove any states in Q that manifest conflict
    ### find conflict order first 
    issue=[]
    temp_issue=[]
    final_issue={}
    
    # need to update this, right now hard coded
    while len(issue)==0:
        for var in range(4,0,-1):
            temp_issue=[]
            str_var=str(var)
            num_var=var
            is_normal = conflict[str_var]
            is_open = states[str_var]
            # valve is open, and nominal: has flow
            if is_normal and is_open:
                expected = 1
            elif is_normal and not is_open:
                # no flow
                expected = 0
            elif not is_normal and is_open:
                # stuck close
                expected = 0
            else:
                # broken, and state is close
                # stuck open
                expected = 1
            
            if expected !=output:
                while num_var>0:
                    temp_issue.append(num_var)
                    num_var=num_var-2
                if temp_issue not in conflict_list:
                    issue=temp_issue
                    break
    
    for each in issue:
        each_string=str(each)
        final_issue[each_string]=conflict[each_string]
        
##    print('FINALIZED the conflict it found for this case was {}'.format(final_issue))   
        
    conflict_list.append(final_issue)
    

    new_queue = []
    for assignment in queue:
        if not final_issue.items() <= assignment.items():
            new_queue.append(assignment)
    return new_queue,conflict_list

            

def build_conflict_kernel(conflict, csp):
    kernel = {}
    # conflict: not ("1"=True and "2"=True)
    # resolve t ("1" = False) or ("2"=False)
    for var in conflict.keys():
        value = conflict[var]
        # since we only have either True or False
        kernel[var] = not value
    return kernel
    

def resolved_conflicts(conflicts, assignment, csp):
    kernels = []
    for conflict in conflicts:
        # build a kernel for each conflict
        kernel = build_conflict_kernel(conflict, csp)
        kernels.append(kernel)
        
    for i in range(len(kernels)):
        k = kernels[i]
        is_resolved = False
        # check if any one of variable is resolved for each kernel
        # resolved means: kernel value of var is same as our assignment of var
        for var in k:
            if var in assignment:
                # check resolvable
                if k[var] == assignment[var]:
                    is_resolved = True
                    break
            
        if not is_resolved:
            # ith kernel not resolvable, so conflict i is returned
            return False, conflicts[i]
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
# reward function f = g(x) + h(x)
def score_f(assignment):
    score = 0
    for var in decision_vars:
        valve_type = types[var]
        prob_dist = probs_table[valve_type]
        state = states[var]
        if var in assignment:
            is_normal = assignment[var]
            if is_normal:
                #print ("var: ", var, "is normal", "prob", prob_dist[0])
                score += np.log(prob_dist[0])
            else:
                if state == 1:
                    #print ("var: ", var, "not normal, prob", prob_dist[1])
                    # suppose to be open, but detect not normal, thus stuck close
                    score += np.log(prob_dist[1])
                else:
                    #print ("var: ", var, "not normal, prob", prob_dist[2])
                    # suppose to be close, but detect not normal, thus stuck open
                    score += np.log(prob_dist[2])

        else:
            #print("var: ", var, "estimate: ", np.max(prob_dist))
            # estimate heuristic
            # overestimate 
            score += np.max(np.log(prob_dist))
    #print ("score: ", score)
    return score


optimal_csp = OptimalCSP(variables, domains, constraints, decision_vars, score_f)
output=False
result_cda = cda(optimal_csp,output, states)
print (result_cda)
