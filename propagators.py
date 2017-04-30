import queue

def prop_BT(csp, newVar=None):
    '''Do plain backtracking propagation. That is, do no 
    propagation at all. Just check fully instantiated constraints'''
    
    if not newVar:
        return True, []
    for c in csp.get_cons_with_var(newVar):
        if c.get_n_unasgn() == 0:
            vals = []
            vars = c.get_scope()
            for var in vars:
                vals.append(var.get_assigned_value())
            if not c.check(vals):
                return False, []
    return True, []

def prop_FC(csp, newVar=None):
    '''Do forward checking. That is check constraints with 
       only one uninstantiated variable. Remember to keep 
       track of all pruned variable,value pairs and return '''
    prunings = []
    vals = []
    if not newVar:
        for c in csp.get_all_cons():
            if c.get_n_unasgn() == 1:
                var = c.get_unasgn_vars()
                var = var[0]
                temp = []
                for val in var.cur_domain():
                    if not c.check([val]):
                        temp.append((var, val))
                for pair in temp:
                    pair[0].prune_value(pair[1])
                prunings = prunings + temp
                if var.cur_domain_size() == 0:
                    return False, prunings
        return True, prunings
    
    for c in csp.get_cons_with_var(newVar):
        if c.get_n_unasgn() == 1:
            var = c.get_unasgn_vars()
            var = var[0]
            temp = []
            for val in var.cur_domain():
                scope = c.get_scope()
                var.assign(val)
                for item in scope:
                    vals.append(item.get_assigned_value())
                if not c.check(vals):
                    temp.append((var, val))
                var.unassign()
                vals = []
            for pair in temp:
                pair[0].prune_value(pair[1])
            prunings = prunings + temp
            if var.cur_domain_size() == 0:
                return False, prunings
    return True, prunings
            
                        
                
        

def prop_GAC(csp, newVar=None):
    '''Do GAC propagation. If newVar is None we do initial GAC enforce 
       processing all constraints. Otherwise we do GAC enforce with
       constraints containing newVar on GAC Queue'''

    q = []
    prunings = []
    if not newVar:
        for c in csp.get_all_cons():
            q.append(c)
        while len(q) != 0: 
            c = q.pop(0)
            for var in c.get_scope():
                initial_domain = var.cur_domain()
                for val in initial_domain:
                    if not c.has_support(var, val):
                        var.prune_value(val)
                        prunings.append((var, val))
                        if var.cur_domain_size() == 0:
                            return False, prunings
                        for c_prime in csp.get_cons_with_var(var):
                            if c_prime not in q: 
                                q.append(c_prime)
        return True, prunings
    
    for c in csp.get_cons_with_var(newVar):
        q.append(c)
    while len(q) != 0: 
        c = q.pop(0)
        for var in c.get_scope():
            initial_domain = var.cur_domain()
            for val in initial_domain:
                if not c.has_support(var, val):
                    var.prune_value(val)
                    prunings.append((var, val))
                    if var.cur_domain_size() == 0:
                        return False, prunings
                    for c_prime in csp.get_cons_with_var(var):
                        if c_prime not in q: 
                            q.append(c_prime)
    return True, prunings
        
                        
        
        
        
        
        
        
        
        
        
        
        
        
