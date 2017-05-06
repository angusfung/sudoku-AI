Sodoku solver by modelling it as a CSP (constraint-satification problem), and additionally as an exact cover problem using Dancing Links (TO DO). 

# How to run the code:
1. Clone the repository.
2. Run sudoku_csp.py

Additional problems can be input into sudoku_run.py. 

# CSP:
1. Constraint 1: Uniqueness in each row     [binary-not-equal constraints]
2. Constraint 2: Uniqueness in each column  [binary-not-equal constraints]
3. Constraint 3a: Uniqueness in each square [all-different constraints]
4. Constraint 3b: Uniqueness in each square [binary-not-equal constraints]

Constraint 3a was commented out since it was too slow. 



