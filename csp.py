import time
import functools

class Variable: 

    #
    #set up and info methods
    #
    def __init__(self, name, domain=[]):
        '''Create a variable object, specifying its name (a
        string). Optionally specify the initial domain.
        '''
        self.name = name                #text name for variable
        self.dom = list(domain)         #Make a copy of passed domain
        self.curdom = [True] * len(domain)      #using list
        #for bt_search
        self.assignedValue = None

    def add_domain_values(self, values):
        '''Add additional domain values to the domain
           Removals not supported removals'''
        for val in values: 
            self.dom.append(val)
            self.curdom.append(True)

    def domain_size(self):
        '''Return the size of the (permanent) domain'''
        return(len(self.dom))

    def domain(self):
        '''return the variable's (permanent) domain'''
        return(list(self.dom))

    #
    #methods for current domain (pruning and unpruning)
    #

    def prune_value(self, value):
        '''Remove value from CURRENT domain'''
        self.curdom[self.value_index(value)] = False

    def unprune_value(self, value):
        '''Restore value to CURRENT domain'''
        self.curdom[self.value_index(value)] = True

    def cur_domain(self):
        '''return list of values in CURRENT domain (if assigned 
           only assigned value is viewed as being in current domain)'''
        vals = []
        if self.is_assigned():
            vals.append(self.get_assigned_value())
        else:
            for i, val in enumerate(self.dom):
                if self.curdom[i]:
                    vals.append(val)
        return vals

    def in_cur_domain(self, value):
        '''check if value is in CURRENT domain (without constructing list)
           if assigned only assigned value is viewed as being in current 
           domain'''
        if not value in self.dom:
            return False
        if self.is_assigned():
            return value == self.get_assigned_value()
        else:
            return self.curdom[self.value_index(value)]

    def cur_domain_size(self):
        '''Return the size of the variables domain (without construcing list)'''
        if self.is_assigned():
            return 1
        else:
            return(sum(1 for v in self.curdom if v))

    def restore_curdom(self):
        '''return all values back into CURRENT domain'''
        for i in range(len(self.curdom)):
            self.curdom[i] = True

    #
    #methods for assigning and unassigning
    #

    def is_assigned(self):
        return self.assignedValue != None
    
    def assign(self, value):
        '''Used by bt_search. When we assign we remove all other values
           values from curdom. We save this information so that we can
           reverse it on unassign'''

        if self.is_assigned() or not self.in_cur_domain(value):
            print("ERROR: trying to assign variable", self, 
                  "that is already assigned or illegal value (not in curdom)")
            return

        self.assignedValue = value

    def unassign(self):
        '''Used by bt_search. Unassign and restore old curdom'''
        if not self.is_assigned():
            print("ERROR: trying to unassign variable", self, " not yet assigned")
            return
        self.assignedValue = None

    def get_assigned_value(self):
        '''return assigned value...returns None if is unassigned'''
        return self.assignedValue

    #
    #internal methods
    #

    def value_index(self, value):
        '''Domain values need not be numbers, so return the index
           in the domain list of a variable value'''
        return self.dom.index(value)

    def __repr__(self):
        return("Var-{}".format(self.name))

    def __str__(self):
        return("Var--{}".format(self.name))

    def print_all(self):
        '''Also print the variable domain and current domain'''
        print("Var--\"{}\": Dom = {}, CurDom = {}".format(self.name, 
                                                             self.dom, 
                                                             self.curdom))
class Constraint: 
    '''Class for defining constraints variable objects specifes an
       ordering over variables.  This ordering is used when calling
       the satisfied function which tests if an assignment to the
       variables in the constraint's scope satisfies the constraint'''

    def __init__(self, name, scope): 
        '''create a constraint object, specify the constraint name (a
        string) and its scope (an ORDERED list of variable objects).
        The order of the variables in the scope is critical to the
        functioning of the constraint.

        Consraints are implemented as storing a set of satisfying
        tuples (i.e., each tuple specifies a value for each variable
        in the scope such that this sequence of values satisfies the
        constraints).

        NOTE: This is a very space expensive representation...a proper
        constraint object would allow for representing the constraint
        with a function.  
        '''

        self.scope = list(scope)
        self.name = name
        self.sat_tuples = dict()

        #The next object data item 'sup_tuples' will be used to help
        #support GAC propgation. It allows access to a list of 
        #satisfying tuples that contain a particular variable/value
        #pair.
        self.sup_tuples = dict()

    def add_satisfying_tuples(self, tuples):
        '''We specify the constraint by adding its complete list of satisfying tuples.'''
        for x in tuples:
            t = tuple(x)  #ensure we have an immutable tuple
            if not t in self.sat_tuples:
                self.sat_tuples[t] = True

            #now put t in as a support for all of the variable values in it
            for i, val in enumerate(t):
                var = self.scope[i]
                if not (var,val) in self.sup_tuples:
                    self.sup_tuples[(var,val)] = []
                self.sup_tuples[(var,val)].append(t)

    def get_scope(self):
        '''get list of variables the constraint is over'''
        return list(self.scope)

    def check(self, vals):
        '''Given list of values, one for each variable in the
           constraints scope, return true if and only if these value
           assignments satisfy the constraint by applying the
           constraints "satisfies" function.  Note the list of values
           are must be ordered in the same order as the list of
           variables in the constraints scope'''
        return tuple(vals) in self.sat_tuples

    def get_n_unasgn(self):
        '''return the number of unassigned variables in the constraint's scope'''
        n = 0
        for v in self.scope:
            if not v.is_assigned():
                n = n + 1
        return n

    def get_unasgn_vars(self): 
        '''return list of unassigned variables in constraint's scope. Note
           more expensive to get the list than to then number'''
        vs = []
        for v in self.scope:
            if not v.is_assigned():
                vs.append(v)
        return vs

    def has_support(self, var, val):
        '''Test if a variable value pair has a supporting tuple (a set
           of assignments satisfying the constraint where each value is
           still in the corresponding variables current domain
        '''
        if (var, val) in self.sup_tuples:
            for t in self.sup_tuples[(var, val)]:
                if self.tuple_is_valid(t):
                    return True
        return False

    def tuple_is_valid(self, t):
        '''Internal routine. Check if every value in tuple is still in
           corresponding variable domains'''
        for i, var in enumerate(self.scope):
            if not var.in_cur_domain(t[i]):
                return False
        return True

    def __str__(self):
        return("{}({})".format(self.name,[var.name for var in self.scope]))

class CSP:
    '''Class for packing up a set of variables into a CSP problem.
       Contains various utility routines for accessing the problem.
       The variables of the CSP can be added later or on initialization.
       The constraints must be added later'''

    def __init__(self, name, vars=[]):
        '''create a CSP object. Specify a name (a string) and 
           optionally a set of variables'''

        self.name = name
        self.vars = []
        self.cons = []
        self.vars_to_cons = dict()
        for v in vars:
            self.add_var(v)

    def add_var(self,v):
        '''Add variable object to CSP while setting up an index
           to obtain the constraints over this variable'''
        if not type(v) is Variable:
            print("Trying to add non variable ", v, " to CSP object")
        elif v in self.vars_to_cons:
            print("Trying to add variable ", v, " to CSP object that already has it")
        else:
            self.vars.append(v)
            self.vars_to_cons[v] = []

    def add_constraint(self,c):
        '''Add constraint to CSP. Note that all variables in the 
           constraints scope must already have been added to the CSP'''
        if not type(c) is Constraint:
            print("Trying to add non constraint ", c, " to CSP object")
        else:
            for v in c.scope:
                if not v in self.vars_to_cons:
                    print("Trying to add constraint ", c, " with unknown variables to CSP object")
                    return
                self.vars_to_cons[v].append(c)
            self.cons.append(c)

    def get_all_cons(self):
        '''return list of all constraints in the CSP'''
        return self.cons
        
    def get_cons_with_var(self, var):
        '''return list of constraints that include var in their scope'''
        return list(self.vars_to_cons[var])

    def get_all_vars(self):
        '''return list of variables in the CSP'''
        return list(self.vars)

    def print_all(self):
        print("CSP", self.name)
        print("   Variables = ", self.vars)
        print("   Constraints = ", self.cons)


    def print_soln(self):
        print("CSP", self.name, " Assignments = ")
        for v in self.vars:
            print(v, " = ", v.get_assigned_value(), "    ", end='')
        print("")

########################################################
# Backtracking Routine                                 #
########################################################

class BT:
    '''use a class to encapsulate things like statistics
       and bookeeping for pruning/unpruning variabel domains
       To use backtracking routine make one of these objects
       passing the CSP as a parameter. Then you can invoke
       that objects's bt_search routine with the right
       kind or propagator function to obtain plain backtracking
       forward-checking or gac'''

    def __init__(self, csp):
        '''csp == CSP object specifying the CSP to be solved'''

        self.csp = csp
        self.nDecisions = 0 #nDecisions is the number of variable 
                            #assignments made during search
        self.nPrunings  = 0 #nPrunings is the number of value prunings during search
        unasgn_vars = list() #used to track unassigned variables
        self.TRACE = False
        self.runtime = 0

    def trace_on(self):
        '''Turn search trace on'''
        self.TRACE = True

    def trace_off(self):
        '''Turn search trace off'''
        self.TRACE = False

        
    def clear_stats(self):
        '''Initialize counters'''
        self.nDecisions = 0
        self.nPrunings = 0
        self.runtime = 0

    def print_stats(self):
        print("Search made {} variable assignments and pruned {} variable values".format(
            self.nDecisions, self.nPrunings))

    def restoreValues(self,prunings):
        '''Restore list of values to variable domains
           each item in prunings is a pair (var, val)'''
        for var, val in prunings:
            var.unprune_value(val)

    def restore_all_variable_domains(self):
        '''Reinitialize all variable domains'''
        for var in self.csp.vars:
            if var.is_assigned():
                var.unassign()
            var.restore_curdom()

    def extractMRVvar(self):
        '''Remove variable with minimum sized cur domain from list of
           unassigned vars. Would be faster to use heap...but this is
           not production code.
        '''

        md = -1
        mv = None
        for v in self.unasgn_vars:
            if md < 0:
                md = v.cur_domain_size()
                mv = v
            elif v.cur_domain_size() < md:
                md = v.cur_domain_size()
                mv = v
        self.unasgn_vars.remove(mv)
        return mv

    def restoreUnasgnVar(self, var):
        '''Add variable back to list of unassigned vars'''
        self.unasgn_vars.append(var)
        
    def bt_search(self,propagator):


        self.clear_stats()
        stime = time.process_time()

        self.restore_all_variable_domains()
        
        self.unasgn_vars = []
        for v in self.csp.vars:
            if not v.is_assigned():
                self.unasgn_vars.append(v)

        status, prunings = propagator(self.csp) #initial propagate no assigned variables.
        self.nPrunings = self.nPrunings + len(prunings)

        if self.TRACE:
            print(len(self.unasgn_vars), " unassigned variables at start of search")
            print("Root Prunings: ", prunings)

        if status == False:
            print("CSP{} detected contradiction at root".format(
                self.csp.name))
        else:
            status = self.bt_recurse(propagator, 1)   #now do recursive search


        self.restoreValues(prunings)
        if status == False:
            print("CSP{} unsolved. Has no solutions".format(self.csp.name))
        if status == True:
            #print("CSP {} solved. CPU Time used = {}".format(self.csp.name,
                                                             #time.process_time() - stime))
            pass
            #self.csp.print_soln()

        print("bt_search finished")
        self.print_stats()

    def bt_recurse(self, propagator, level):
        '''Return true if found solution. False if still need to search.
           If top level returns false--> no solution'''

        if self.TRACE:
            print('  ' * level, "bt_recurse level ", level)
           
        if not self.unasgn_vars:
            #all variables assigned
            return True
        else:
            var = self.extractMRVvar()
            if self.TRACE:
                print('  ' * level, "bt_recurse var = ", var)

            for val in var.cur_domain():

                if self.TRACE:
                    print('  ' * level, "bt_recurse trying", var, "=", val)

                var.assign(val)
                self.nDecisions = self.nDecisions+1

                status, prunings = propagator(self.csp, var)
                self.nPrunings = self.nPrunings + len(prunings)

                if self.TRACE:
                    print('  ' * level, "bt_recurse prop status = ", status)
                    print('  ' * level, "bt_recurse prop pruned = ", prunings)

                if status:
                    if self.bt_recurse(propagator, level+1):
                        return True

                if self.TRACE:
                    print('  ' * level, "bt_recurse restoring ", prunings)
                self.restoreValues(prunings)
                var.unassign()

            self.restoreUnasgnVar(var)
            return False
