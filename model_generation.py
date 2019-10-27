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

class model_generation():
    
    # CONSTRAINT Decision Variables
    # will be used to define the conditions for a state to be a solution [i.e. passes a given needed voltage]
    

    # Variable 
    # what variables will be used to define each of the work stations
    
    # Domains
    # possible assignments/values of each variable
    
    def __init__(self):
        self.variables = []
        self.domains = []
#        self.parents = parents # used to track parents for mode propagation
        self.constraints = {}
        self.variable_names={}
#        for var in variables:
#            if var in constraints:
#                self.constraints[var] = constraints[var]
#            else:
#                self.constraints[var] = []
    
#    def assign(self, var,val,assignment):
#        ## add {var:val} to assignmnet, override the old value if there was one
#        assingment{var}=val
#
#    
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
    def add_valve(self, name, domain=None):
        var = Valve(name, domain=domain)
        self.variables.append(var)
        self.variable_names[name] = var
        return var
    
    
class Valve():
    def __init__(self, name, domain=['True', 'False', 'False']):
        self.name = str(name)
        self.domain = frozenset(domain)
        self.assignments = {}
        # Initialize assignments

#    def set_probabilities(self, prob_desc):
        # Do some sanity checking
