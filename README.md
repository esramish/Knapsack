# Knapsack

Experimental solutions to the NP-Complete Knapsack problem, as a team-based final project for a Data Structures and Algorithms course.

## Running

The easiest way to run our best current Knapsack-solving method is to use the solveKnapsackFile wrapper function:
```python
from backpack import solveKnapsackFile
default_solution = solveKnapsackFile("problems_size10.txt") # or some other filename
```

You can also specify the method to use:
```python
from backpack import Solver, solveKnapsackFile
print(list(Solver().SOLVER_METHODS)) # displays all the methods currently implemented
solution = solveKnapsackFile("problems_size10.txt", method="backtrack")
```

Run `python3 test_knapsack.py` in the command line to display a brief demo.

