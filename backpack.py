class Solver:


    def __init__(self):
        
        # Constant dict that maps solving method parameter name to the corresponding function name
        self.SOLVER_METHODS = {
            "bruteForce": self.__solveBruteForce
        }


    def loadProblemFromFile(self, filename):
        self.problems = [] # List of (max_weight, [items]) tuples. Each item is a tuple of (name, value, weight)
        
        with open(filename) as f:
            
            # Skip the first line
            next(f)

            # Read each subsequent line
            for line in f:
                line_values = tuple(line.split())
                
                # Check if the line is a problem name
                if len(line_values) == 1:
                    # Append a new (max_weight, [items]) tuple to the list of problems, with the list of items currently empty
                    self.problems.append((int(next(f).strip()), []))
                    continue
                
                # Okay, it's a normal line with an item on it. Add it to the current list of items
                self.problems[-1][1].append(line_values)

    
    def getSolutions(self, method):
        
        # Confirm that method argument is valid
        if method not in self.SOLVER_METHODS:
            raise ValueError(f"Invalid method. Valid method names: {self.SOLVER_METHODS.keys}")

        # Delegate to the function that uses the specified solving method
        return self.SOLVER_METHODS[method]()
    

    def __solveBruteForce(self):
        # TODO
        pass


def solveKnapsackFile(filename, method="bruteForce"):
    solver = Solver()
    solver.loadProblemFromFile(filename)
    return solver.getSolutions(method)