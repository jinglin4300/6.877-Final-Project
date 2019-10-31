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
    def __init__(self, name, status, domain=['Nominal', 'Sc', 'So'], is_pyro=False, valve_in=1):
        self.name = str(name)
        self.domain = domain # made it not frozen so we can prune later
        self.assignments = {}
        self.mode = 'Nominal'
        self.is_pyro = is_pyro
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
        self.output = self.value[self.input]


    def set_mode(val):
        self.mode = val

    def set_input(val):
        self.input=val
    def get_corresponding_link(self,links):
        for each in links:
            if each.in_valve_name==self.name:
                return each
        return None
        
        
        
class Link():
    def __init__(self,name,vn,pl, ins1, outs1):
        self.name=name
        self.in_valve_name=vn
        self.prior_link=pl
        self.ins=ins1
        self.outs=outs1
        self.value=None
        
    def assign_value(self,node,prior_link_value):
        if node.status == 'open' and prior_link_value!=None:
            self.value=prior_link_value
        elif node.status== 'close':
            self.value=0
        elif node.status == 'open':
            self.value=node.input
    
        
