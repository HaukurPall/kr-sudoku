# Knowledge Representation Sudoku assignment

# Flow
* Create X many Sudokus. Save them to disk. They can be proper and improper. Finish all trivial steps (cannot be solved)
* Read Sudokus and per Sudoku generate a directed node graph with all possible solutions. Save to disk
* Translate non-trivial sudokus to different SAT solvers format. Save to disk
* Run SAT-X solver on translated sudoku. Extract nodes which were traversed. Save to disk
- https://pypi.python.org/pypi/pycosat
- https://pypi.python.org/pypi/satispy
* Compare SAT solvers traversing. 