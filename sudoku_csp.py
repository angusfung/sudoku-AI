from csp import *
import itertools
import time
    
def binary_not_equal(x,y):
    return x != y

def all_diff(array):
    return len(list(set(array))) == len(list(array))

def sudoku_model(initial_grid):
    
    ##variable array
    variable_array = []
    for i in range(len(initial_grid)):
        vars = []
        for j in range(len(initial_grid[i])):
            if initial_grid[i][j] == -1:
                dom = [k for k in range(1,10)]
            else:
                dom = [initial_grid[i][j]]
            vars.append(Variable('{}{}'.format(i,j),dom))
        variable_array.append(vars)
        
    ##constraints
    
    cons = [] #add all constraints objects in a list
    '''
    1) Uniqueness in each row.    (binary)
    2) Uniqueness in each column. (binary)
    3) Uniqueness in each square. (all-diff)
    4) Uniqueness in each square. (binary)
    
    '''
    
    #1 Row
    for i in range(len(initial_grid)):
        for j in range(len(initial_grid[i])):
            for k in range(j+1,len(initial_grid[i])):
                var_scope = [variable_array[i][j], variable_array[i][k]]
                con = Constraint('Row({},{})'.format(j,k), var_scope)
                sat_tuples = []
                cur_domain1 = variable_array[i][j].cur_domain()
                cur_domain2 = variable_array[i][k].cur_domain()
                
                for t in itertools.product(cur_domain1, cur_domain2):
                    if binary_not_equal(t[0], t[1]):
                        sat_tuples.append(t)
                con.add_satisfying_tuples(sat_tuples)
                cons.append(con)
    
    #2 Column
    for i in range(0,9):
        for j in range(0,9):
            for k in range(j+1,9):
                var_scope = [variable_array[j][i],variable_array[k][i]]
                con = Constraint('Column({},{})'.format(j,k), var_scope)
                sat_tuples = []
                cur_domain1 = variable_array[j][i].cur_domain()
                cur_domain2 = variable_array[k][i].cur_domain()
        
                for t in itertools.product(cur_domain1, cur_domain2):
                    if binary_not_equal(t[0], t[1]):
                        sat_tuples.append(t)
                con.add_satisfying_tuples(sat_tuples)
                cons.append(con)

'''
    #3 Square (all-diff)
    center_sq = [(1,1),(4,1),(7,1),(1,4),(4,4),(7,4),(1,7),(4,7),(7,7)]

    for i in range(0,9):
        for j in range(0,9):
            print(i,j)
            if (i,j) in center_sq:
                top_left      = variable_array[i-1][j-1]
                top_center    = variable_array[i-1][j  ]
                top_right     = variable_array[i-1][j+1]
                left          = variable_array[i  ][j-1]
                center        = variable_array[i  ][j  ]
                right         = variable_array[i  ][j+1]
                bottom_left   = variable_array[i+1][j-1]
                bottom_center = variable_array[i+1][j  ]
                bottom_right  = variable_array[i+1][j+1]
                
                var_scope = [top_left   , top_center   , top_right,
                             left       , center       , right    ,
                             bottom_left, bottom_center, bottom_right] 
                
                con = Constraint('Column({},{})'.format(j,k), var_scope)
                sat_tuples = []
                
                cur_domain = []
                for var in var_scope:
                    cur_domain.append(var.cur_domain())
                
                for t in itertools.product(*cur_domain):
                    if all_diff(t):
                        sat_tuples.append(t)
                        
                con.add_satisfying_tuples(sat_tuples)
                cons.append(con)
'''

        
        
    csp = CSP('Sudoku', [value for sublist in variable_array for value in sublist])
    for c in cons:
        csp.add_constraint(c)
    return csp, variable_array
                
        
    

