import numpy as np 
class CSP:
    def __init__(self, variables, domains):
        self.vars = []
        self.domains = {}
        self.constraints = []
        for var in variables:
            self.vars.append(var)

        for var in domains.keys():
            self.domains[var] = domains[var]


    def add_constraint(self, constraint):
        self.constraints.append(constraint)


    def backtrack_search(self, assignment):
        if len(assignment) == len(self.vars):
            return assignment
        
        unassigned = []
        for var in self.vars:
            if var not in assignment:
                unassigned.append(var)
        
        one_unassigned = unassigned.pop()

        for value in self.domains[one_unassigned]:
            local_assignment = assignment.copy()
            local_assignment[one_unassigned] = value

            # check consistency
            if self.consistent(local_assignment):
                result = self.backtrack_search(local_assignment)
                if result is not None:
                    return result
        return None

    def consistent(self, assignment):
        for c in self.constraints:
            if not c.satisfied(assignment):
                return False

        return True

    def consistent_conflict(self, assignment):
        for c in self.constraints:
            is_satisfied, conflict = c.satisfied_conflict(assignment)
            if not is_satisfied:
                return False, conflict
        return True, {}
        

class Constraint:
    def __init__(self, vars):
        self.vars = vars

    def satisfied(self, assignment):
        return None

    def satisfied_conflict(self, assignment):
        return None, {}

class OrConstraint(Constraint):
    def __init__(self, vars):
        super().__init__(vars)
    
    def satisfied(self, assignment):
        # constraint would be a set of () or () or ()
        # only ONE need to true
        for var in assignment.keys():
            if var.satisfied(assignment):
                return True
        return False

    def satisfied_conflict(self, assignment):
        conflicts = {}
        for var in assignment.keys():
            is_satisfied, conflict = var.satisfied_conflict(assignment)
            if is_satisfied:
                return True, conflicts
            if not is_satisfied:
                if conflict is not None:
                    conflicts.update(conflict)
                conflicts[var] = assignment[var]
        return False, conflicts

class AndConstraint(Constraint):
    def __init__(self, vars):
        super().__init__(vars)
    
    def satisfied(self, assignment):
        # All need to be True
        for var in self.vars:
            if not var.satisfied(assignment):
                return False
        return True

    def satisfied_conflict(self, assignment):
        conflicts = {}
        for var in self.vars:
            is_satisfied, conflict = var.satisfied_conflict(assignment)
            if not is_satisfied:
                if conflict is not None:
                    conflicts.update(conflict)
                if var in assignment:
                    conflicts[var] = assignment[var]
                return False, conflicts
        return True, conflicts

class NotConstraint(Constraint):
    def __init__(self, vars):
        super().__init__(vars)
        self.var = vars[0]

    def satisfied(self, assignment):
        return not self.var.satisfied(assignment)

    def satisfied_conflict(self, assignment):
        is_satisfied, conflicts = var.satisfied_conflict(assignment)
        return not is_satisfied, conflicts

class SingleSelfConstraint(Constraint):
    def __init__(self, vars):
        super().__init__(vars)
        self.var = vars[0]

    def satisfied(self, assignment):
        if self.var in assignment:
            return assignment[self.var]
        return True

    def satisfied_conflict(self, assignment):
        if self.var in assignment:
            return assignment[self.var], None
        return True, {}



if __name__ == "__main__":
    variables = ["v1", "v2", "v3", "v4", "v5", "v6", "v7", "v8", 
    "v9", "v10", "v11", "v12", "v13", "v14", "v15", "v16"]

    domain = [True, False]

    domains = {}
    for var in variables:
        domains[var] = domain[:]

    csp = CSP(variables, domains)

    # add constraints:
    singleCs = {}
    for i in range(len(variables)):
        var = variables[i]
        singleCs[var] = SingleSelfConstraint([var])

    # # v1 or v2 or v3 or v4
    # csp.add_constraint(OrConstraint([singleCs["v1"], singleCs["v2"], singleCs["v3"], singleCs["v4"]]))
    # # v5 or v6 or v7 or v8 or v9 or v10 or v11
    # csp.add_constraint(OrConstraint([
    #     singleCs["v5"], singleCs["v6"], singleCs["v7"], singleCs["v8"],
    #     singleCs["v9"], singleCs["v10"], singleCs["v11"], singleCs["v12"]
    # ]))
    # # v13 or v14 or v15 or v16
    # csp.add_constraint(OrConstraint([singleCs["v13"], singleCs["v14"], singleCs["v15"], singleCs["v16"]]))
    # # (v1 and v5) or (v1 and v6) or (not v1)
    # csp.add_constraint(OrConstraint([
    #     AndConstraint([singleCs["v1"], singleCs["v5"]]), 
    #     AndConstraint([singleCs["v1"], singleCs["v6"]]),
    #     NotConstraint([singleCs["v1"]])
    # ]))

    # # (v2 and v7) or (v2 and v8) or (not v2)
    # csp.add_constraint(OrConstraint([
    #     AndConstraint([singleCs["v2"], singleCs["v7"]]), 
    #     AndConstraint([singleCs["v2"], singleCs["v8"]]),
    #     NotConstraint([singleCs["v2"]])
    # ]))

    # # (v3 and v9) or (v3 and v10) or (not v3)
    # csp.add_constraint(OrConstraint([
    #     AndConstraint([singleCs["v3"], singleCs["v9"]]), 
    #     AndConstraint([singleCs["v3"], singleCs["v10"]]),
    #     NotConstraint([singleCs["v3"]])
    # ]))

    # # (v4 and v11) or (v4 and v12) or (not v4)
    # csp.add_constraint(OrConstraint([
    #     AndConstraint([singleCs["v4"], singleCs["v11"]]), 
    #     AndConstraint([singleCs["v4"], singleCs["v12"]]),
    #     NotConstraint([singleCs["v4"]])
    # ]))

    # # (v5 and v13) or (v6 and v13) or (not v5 and not v6)
    # csp.add_constraint(OrConstraint([
    #     AndConstraint([singleCs["v5"], singleCs["v13"]]),
    #     AndConstraint([singleCs["v6"], singleCs["v13"]]),
    #     AndConstraint([NotConstraint([singleCs["v5"]]), NotConstraint([singleCs["v6"]])])
    # ]))

    # # (v7 and v14) or (v8 and v14) or (not v7 and not v8)
    # csp.add_constraint(OrConstraint([
    #     AndConstraint([singleCs["v7"], singleCs["v14"]]),
    #     AndConstraint([singleCs["v8"], singleCs["v14"]]),
    #     AndConstraint([NotConstraint([singleCs["v7"]]), NotConstraint([singleCs["v8"]])])
    # ]))

    # # (v9 and v15) or (v10 and v15) or (not v9 and not v10)
    # csp.add_constraint(OrConstraint([
    #     AndConstraint([singleCs["v9"], singleCs["v15"]]),
    #     AndConstraint([singleCs["v10"], singleCs["v15"]]),
    #     AndConstraint([NotConstraint([singleCs["v9"]]), NotConstraint([singleCs["v10"]])])
    # ]))

    # # (v11 and v16) or (v12 and v16) or (not v11 and not v12)
    # csp.add_constraint(OrConstraint([
    #     AndConstraint([singleCs["v11"], singleCs["v16"]]),
    #     AndConstraint([singleCs["v12"], singleCs["v16"]]),
    #     AndConstraint([NotConstraint([singleCs["v11"]]), NotConstraint([singleCs["v16"]])])
    # ]))

    # assignment = csp.backtrack_search({})
    # print (assignment)



    # testing:
    csp.add_constraint(OrConstraint([
        singleCs["v5"], singleCs["v6"], singleCs["v7"], singleCs["v8"],
        singleCs["v9"], singleCs["v10"], singleCs["v11"], singleCs["v12"]
    ]))

    is_consistent, conflict = csp.consistent_conflict({'v12': False, 'v11': False, 'v10': False, 'v9': False, 'v8': False, 'v7': False, 'v6': False, 'v5': False})
    print ("here", is_consistent, conflict)
    # True for open valve, False for close valve
    states = {
        "v1": False, "v2": False, "v3": False, "v4": False,
        "v5": False, "v6": False, "v7": False, "v8": False, "v9": False, "v10":False, "v11": False, "v12":False,
        "v13": True, "v14": True, "v15": False, "v16": False
    }

    # 1 for regular valve, 0 for pyro valve
    types = {
        "v1": 1, "v2": 1, "v3": 1, "v4": 1,
        "v5": 0, "v6": 1, "v7": 0, "v8": 1, "v9": 0, "v10":1, "v11": 0, "v12":1,
        "v13": 0, "v14": 0, "v15": 0, "v16": 0
    }

    # norminal, stuck closed, stuck open
    valve_prob = [0.8, 0.1, 0.1]
    pyro_valve_prob = [0.95, 0.03, 0.02]
    probs = {1: valve_prob, 0: pyro_valve_prob}

    def find_prob(assignment, states, types):
        prob = 1
        for var in assignment:
            has_flow = assignment[var]
            is_open = states[var]
            if (has_flow and is_open) or (not has_flow and not is_open):
                # acting normally
                prob *= probs[types[var]][0]
            elif has_flow and not is_open:
                # stuck open
                prob *= probs[types[var]][2]
            elif not has_flow and is_open:
                # stuck closed
                prob *= probs[types[var]][1]
        return prob

    # print ("with current assignment, its prob: ", find_prob(assignment, states, types))


    def constraint_based_astar(csp):
        queue = [{}]
        expanded = []
        while len(queue) > 0:
            assign = queue.pop()
            expanded.append(assign)
            if len(assign) == len(csp.vars):
                if csp.consistent(assign):
                    return assign
            else:
                for var in csp.vars:
                    if var not in assign:
                        nbrs = split_on_var(assign, var, csp)
                        for nbr in nbrs:
                            if nbr not in expanded:
                                queue.append(nbr)

            queue = sort_queue(queue, csp)
            print (len(queue))
                        
        return None

    def compute_score(assign, states, types, csp):
        score = 0
        for var in csp.vars:
            if var in assign:
                has_flow = assign[var]
                is_open = states[var]
                if (has_flow and is_open) or (not has_flow and not is_open):
                    # acting normally
                    score += -np.log(probs[types[var]][0])
                elif has_flow and not is_open:
                    # stuck open
                    score += -np.log(probs[types[var]][2])
                elif not has_flow and is_open:
                    # stuck closed
                    score += -np.log(probs[types[var]][1])
            else:
                score += -np.log(np.max(probs[types[var]]))
        return score 
                


    def sort_queue(queue, csp):
        priority_queue = []
        for assign in queue:
            prob = compute_score(assign, states, types, csp)
            priority_queue.append((prob, assign))
        
        priority_queue = sorted(priority_queue, key=lambda x: x[0], reverse=True)
        print (priority_queue)
        new_queue = []
        for p, assign in priority_queue:
            new_queue.append(assign)
        return new_queue
            

    def split_on_var(assign, var, csp):
        next_queues = []
        for value in csp.domains[var]:
            assign_copy = assign.copy()
            assign_copy[var] = value
            next_queues.append(assign_copy)
        return next_queues

    # cba_assignment = constraint_based_astar(csp)
    # print ("CBA assignment: ", cba_assignment)


    def conflict_directed_astar(csp):
        queue = [{}]
        conflicts = []
        expanded = []
        while len(queue) > 0:
            assign = queue.pop()
            expanded.append(assign)
            print ("assign", assign)
            if len(assign) == len(csp.vars):
                is_consistent, conflict = csp.consistent_conflict(assign)
                print ("conflict: ", conflict)
                print ("is consistent", is_consistent)
                if is_consistent:
                    return assign
                else:
                    conflicts.append(conflict)
                    queue = remove_conflict(queue, conflict)
            else:
                nbrs = []
                is_resolved, non_resolved_conflict = resolve_conflict(assign, conflicts)
                if is_resolved:
                    for var in csp.vars:
                        if var not in assign:
                            nbrs = split_on_var(assign, var, csp)
                else:
                    nbrs = split_on_conflict(assign, non_resolved_conflict, csp)
                
                for nbr in nbrs:
                    if nbr not in expanded:
                        queue.append(nbr)

            queue = sort_queue(queue, csp)
            print (len(queue))
        return None


    def remove_conflict(queue, conflict):
        if len(conflict) > 0:
            new_queue = []
            for assign in queue:
                # check if conflict is subset of assignment
                # remove if so, no need to check further for that assign
                if not conflict.items() <= assign.items():
                    new_queue.append(assign)
        else:
            new_queue = queue[:]
        return new_queue

    def resolve_conflict(assign, conflicts):
        for conflict in conflicts:
            if conflict.items() <= assign.items(): 
                return False, conflict

        return True, None


    def cons_kernel(conflict, csp):
        possible_assigns = ()
        for var in conflict.keys():
            conflict[var] = value
            csp.domains[var] = domains 
            for v in domains:
                if v != value:
                    possible_assigns.add((var, v))
        return possible_assigns
        


    def split_on_conflict(assign, conflict, csp):
        next_queues = []
        possible_assigns = cons_kernel(conflict, csp)
        for possible_assign in possible_assigns:
            assign_copy = assign.copy()
            var, v = possible_assign
            if var not in assign_copy:
                assign_copy[var] = v
                next_queues.append(assign_copy)
        return next_queues
            

    # cda_assignment = conflict_directed_astar(csp)
    # print ("cda assignment: ", cda_assignment)






