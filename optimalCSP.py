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

    def backtrack_search(self, assignment):
        if len(assignment) == len(self.vars):
            return assignment
        unassigned_var = None
        for var in self.vars:
            if var not in assignment:
                unassigned_var = var
                break

        for value in self.domains[unassigned_var]:
            local_assignment = assignment.copy()
            local_assignment[var] = value
            if self.consistency_check(local_assignment):
                result = self.backtrack_search(local_assignment)
                if result is not None:
                    return result
        return None
               

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



    # def conflict_directed_backjumping(self, assignment, conflicts):
    #     if len(assignment) == len(self.vars):
    #         return assignment, conflicts
    #     unassigned_var = None
    #     for var in self.vars:
    #         if var not in assignment:
    #             unassigned_var = var
    #             break
        
    #     for value in self.domains[unassigned_var]:
    #         local_assignment = assignment.copy()
    #         local_assignment[unassigned_var] = value


    def backtrack_search_conflict(self, assignment, conflicts):
        if len(assignment) == len(self.vars):
            return assignment, None
        unassigned_var = None
        for var in self.vars:
            if var not in assignment:
                unassigned_var = var
                break

        for value in self.domains[unassigned_var]:
            local_assignment = assignment.copy()
            local_assignment[var] = value
            is_consistent, conflict = self.consistency_conflict_check(local_assignment)
            if is_consistent:
                assign_result, conflict_result = self.backtrack_search_conflict(local_assignment, conflicts)
                if assign_result is not None:
                    return assign_result, None
            else:
                for var_conflict in conflict.keys():
                    if var_conflict in self.decision_vars:
                        conflicts[var_conflict] = conflict[var_conflict]
        
        # if is not consistent, means there is conflict
        assert(conflicts is not None)
        return None, conflicts

    def consistency_conflict_check(self, assignment):
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
                return False, assignment
        return True, None
    
