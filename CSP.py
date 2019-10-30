# -*- coding: utf-8 -*-
"""
Created on Sun Oct 27 13:53:54 2019

@author: Sydney
"""

# -*- coding: utf-8 -*-
"""
Created on Thu Oct 24 11:01:33 2019

@author: Sydney
"""

import constraint

class CSP():
    """
    Our CSP is specified by the following inputs:
        variables   A list of valves;
        domains     A dict of {var:[Nominal, Sc, So]} 
        neighbors   A dict of {var:[var,...]} that for each variable lists
                    the other variables that participate in constraints.
        constraints List of boolean statements
    """
    
    def __init__(self, variables, domains, neighbors, constraints):
        self.variables = []
        self.domains = []
#        self.parents = parents # used to track parents for mode propagation
        self.constraints = []
        self.nassigns = 0 #number of decision variables assigned
        self.curr_domains = None #domain of variables if pruned
#        self.variable_names = 
#        for var in variables:
#            if var in constraints:
#                self.constraints[var] = constraints[var]
#            else:
#                self.constraints[var] = []
    
    """ This function keeps track of the number of decision variables assigned
    def assign(self, var,val):
#        add {var:val} to assignmnet, override the old value if there was one
        assingment{var}=val
        self.nassigns +=1
    """    
#    def add_constraint(self, constraint):
#        # add a constraint
#        pass
#    
#    def consistent(self, variables, assignments):
#        # given list of variables and their assignments
#        # check if they are consistant with all constraints
#        pass
#    
#    def search_assigment_brute_force(self, assignments):
#        # Given an empty or paritial assignement
#        # try every possible assignment for each variable that does not violate constraints
#        # stop when we find one possible solution to the question 
#        #     in such case, len(assigment) == len(self.variable)
#        # Or we searches through all combinations of assignments but no solution can be found, return None
#        
#        pass
#    
#
#    def satisfied(self, assignment):
#        # check if given assignment satisfies the question and is consistent with the constraint
#        # in other words, all variables are assigned to a value that not violate constraint
#        pass
#    
#    def full_assignment(self, assignment):
#        # check if given assignment is full assignment to variables 
#        pass
#        
#    def find_nonassigned_variables(self):
#        # find decision variables not yet assigned
#        pass
    def add_valve(self, Valve):
        var = Valve
        self.variables.append(var)
        self.variable_names[var.name] = var
        return var
    
    
class Valve():
    def __init__(self, name, status, domain=['Nominal', 'Sc', 'So'], is_pyro=False, parent=None, valve_in=1):
        self.name = str(name)
        self.domain = domain # made it not frozen so we can prune later
        self.assignments = {}
        self.mode = 'Nominal'
        self.is_pyro = is_pyro
        self.parent = parent #let's not do parent for now
        self.status = status
        self.input = valve_in
        if self.mode == 'Nominal' and status == 'open' :
            self.value = {0:0,1:1}
        if self.mode == 'Nominal' and status == 'close':
            self.value = {0:0,1:0}
        if self.mode == 'Sc':
            self.value = {0:0,1:0}
        if self.mode == 'So':
            self.value = {0:0,1:1}

    def set_mode(val):
        self.mode = val
        
    def get_output():
        return self.value[self.input]
    
    def set_input(val):
        self.input=val
    