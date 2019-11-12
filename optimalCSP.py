class CSP():
    def __init__(self, vars, domains, constraints):
        self.vars = []
        self.domains = {}
        for var in vars:
            self.vars.append(var)
        for var in domains.keys():
            self.domains[var] = domains[var]
        self.constraints = {}
        for var in constraints:
            self.constraints[var] = []
            for c in constraints[var]:
                self.constraints[var].append(c)

    def backtrack_search(self, assignment, num_check):
        if len(assignment) == len(self.vars):
            return assignment, num_check
        unassigned_var = None
        for var in self.vars:
            if var not in assignment:
                unassigned_var = var
                break

        for value in self.domains[unassigned_var]:
            local_assignment = assignment.copy()
            local_assignment[var] = value
            num_check += 1
            if self.consistency_check(local_assignment):
                result, num_check = self.backtrack_search(local_assignment, num_check)
                if result is not None:
                    return result, num_check
        return None, num_check
               

    def consistency_check(self, assignment):
        for var in self.constraints.keys():
            constraints_on_var = self.constraints[var]
            constraints_var_satisfied = False
            # looping through each constraint dictionary
            # if one of constraint dictionary is T for current var
            # var is considered satisfied
            for c_dict in constraints_on_var:
                constraint_var_satisfied = True
                # looping through to each constraint value for var nbrs and var itself
                # need all condition to be true for this particular constraint
                for var_key in c_dict.keys():
                    constrainted_value = c_dict[var_key]
                    if var_key in assignment:
                        if assignment[var_key] != constrainted_value:
                            constraint_var_satisfied = False
                if constraint_var_satisfied:
                    # one of constraint within OR(constraints) for var is T
                    # thus, var is satisifed, break
                    constraints_var_satisfied = True
                    break
            if not constraints_var_satisfied:
                # none of constraints for var is satisfied
                # no need to check further
                return False
        return True

      

class OptimalCSP(CSP):
    def __init__(self, vars, domains, constraints, decision_vars, reward_f):
        super().__init__(vars, domains, constraints)
        self.decision_vars = []
        for var in decision_vars:
            self.decision_vars.append(var)
        self.reward_f = reward_f

    
