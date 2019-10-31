import numpy as np 
from optimalCSP import *

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
constraints["A"] = [{"A": True}]
constraints["B"] = [{"B":True, "1":True, "A":True}, {"B":False, "1":False}, {"B": False, "A": False}]
constraints["C"] = [{"C":False, "2":True}, {"C":True, "2":False, "A":True}]
# constraints["D"] = [{"D":True,"3":True,"B":True}, {"D":False,"3":False}, {"D":False, "B":False}]
# constraints["E"] = [{"E":False,"4":True}, {"E":True, "4":False, "C":True}]
# constraints["F"] = [{"F":True, "D":True}, {"F":True, "E":True}, {"F":False, "D":False, "E":False}]
# set output of toy example to be False to test 
constraints["D"] = [{"D":False,"3":False}, {"D":False, "B":False}]
constraints["E"] = [{"E":False,"4":True}]
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

def check_full_assignment(assignment):
    for var in decision_vars:
        if var not in assignment:
            return False, var
    return True, None

def cba(optimal_csp):
    queue = [{}]
    expanded = []
    while len(queue) > 0:
        assign = queue.pop(0)
        #print ("current", assign)
        expanded.append(assign)
        is_full_assign, non_assigned_var = check_full_assignment(assign)
        if is_full_assign:
            #if optimal_csp.consistency_check(assign):
            csp_assignment = optimal_csp.backtrack_search(assign)
            if csp_assignment is not None:
                return assign
        else:
            assert(non_assigned_var is not None)
            nbrs = split_on_var(assign, non_assigned_var, optimal_csp)
            for nbr in nbrs:
                if nbr not in expanded:
                    queue.append(nbr)

        queue = sort_priority(queue, optimal_csp)
    return None

def split_on_var(assignment, non_assigned_var, csp):
    queue = []
    for value in csp.domains[non_assigned_var]:
        local_assignment = assignment.copy()
        local_assignment[non_assigned_var] = value
        queue.append(local_assignment)
    #print ("split", queue)
    return queue

def sort_priority(queue, optimal_csp):
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


def interpret_assignment(assign):
    new_assignment = {}
    for var in assign.keys():
        is_normal = assign[var]
        is_open = states[var]
        if is_normal:
            new_assignment[var] = "Norminal"
        else:
            if is_open:
                new_assignment[var] = "Stuck Closed"
            else:
                new_assignment[var] = "Stuck Open"
    return new_assignment

result = cba(optimal_csp)
print (interpret_assignment(result))

def cda(optimal_csp):
    queue = [{}]
    conflicts = []
    expanded = []
    while len(queue) > 0:
        assign = queue.pop(0)
        expanded.append(assign)
        is_full_assign, non_assigned_var = check_full_assignment(assign)
        if is_full_assign:
            is_consistent, conflict = optimal_csp.backtrack_search_conflict(assign, {})
            if is_consistent:
                return assign
            else:
                conflicts.append(conflict)
                queue = remove_conflict(conflict, queue)
        else:
            is_resolved, unresolved_conflict = resolved_conflicts(conflicts, assign, optimal_csp)
            if is_resolved:
                nbrs = split_on_var(assign, non_assigned_var, optimal_csp)
            else:
                nbrs = split_on_conflict(assign, unresolved_conflict, optimal_csp)

            for nbr in nbrs:
                if nbr not in expanded:
                    queue.append(nbr)

        queue = sort_priority(queue, optimal_csp)
    return None


def remove_conflict(conflict, queue):
    new_queue = []
    for assignment in queue:
        is_conflicted = True
        for var in conflict.keys():
            if not var in assignment:
                # at least one var is not assigned in assignement
                # cannot become a conflict
                is_conflicted = False
                break
        if not is_conflicted:
            # check all conflict variable, does not conflict with assignment
            new_queue.append(assignment)
    return new_queue

            
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

# result_cda = cda(optimal_csp)
# print (result_cda)

    



        








