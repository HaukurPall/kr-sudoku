from satispy import Variable, Cnf
from satispy.solver import Minisat, Lingeling

def translate_for_satispy(sudoku):
    v1 = Variable("v1")
    v2 = Variable("v2")
    v3 = Variable("v3")
    exp = (v1 | -v2) & (v2 | v3) & (-v3 | -v1)
    solver = Lingeling()
    solution = solver.solve(exp)
    if solution.success:
        print "Found a solution:"
        print v1, solution[v1]
        print v2, solution[v2]
        print v3, solution[v3]
    else:
        print "The expression cannot be satisfied"

def translate_for_pycosat():
    raise

translate_for_satispy("")