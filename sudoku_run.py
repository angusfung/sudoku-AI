from sudoku_csp import *
from propagators import *
import ast, sys

b1 = ([[5,3,-1,-1,7,-1,-1,-1,-1],
        [6,-1,-1,1,9,5,-1,-1,-1],
        [-1,9,8,-1,-1,-1,-1,6,-1],
        [8,-1,-1,-1,6,-1,-1,-1,3],
        [4,-1,-1,8,-1,3,-1,-1,1],
        [7,-1,-1,-1,2,-1,-1,-1,6],
        [-1,6,-1,-1,-1,-1,2,8,-1],
        [-1,-1,-1,4,1,9,-1,-1,5],
        [-1,-1,-1,-1,8,-1,-1,7,9]])


def print_sudoku_soln(var_array):
    for row in var_array:
        print([var.get_assigned_value() for var in row])

if __name__ == "__main__":

    for b in [b1]:
        print("Solving board:")
        for row in b:
            print(row)

        print("Using Model 1")
        csp, var_array = sudoku_model(b1)
        solver = BT(csp)
        # print("=======================================================")
        # print("FC")
        # solver.bt_search(prop_FC)
        # print("Solution")
        # print_sudoku_soln(var_array)
        print("=======================================================")
        print("GAC")
        solver.bt_search(prop_GAC)
        print("Solution")
        print_sudoku_soln(var_array)

