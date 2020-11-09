import numpy as np


class Solver:

    def __init__(self):

        # Constant dict that maps solving method parameter name to the corresponding function name
        self.SOLVER_METHODS = {
            "bruteForce": self.__solveBruteForce
        }

    def loadProblemFromFile(self, filename):
        # List of (max_weight, [items]) tuples. Each item is a tuple of (name, value, weight)
        self.problems = []

        with open(filename) as f:

            # Skip the first line
            next(f)

            # Read each subsequent line
            for line in f:
                line_values = line.split()

                # Check if the line is a problem name
                if len(line_values) == 1:
                    # Append a new (max_weight, [items]) tuple to the list of problems, with the list of items currently empty
                    self.problems.append((int(next(f).strip()), []))
                    continue

                # Okay, it's a normal line with an item on it. Add it to the current list of items
                line_values[1] = int(line_values[1])
                line_values[2] = int(line_values[2])
                line_values = tuple(line_values)
                self.problems[-1][1].append(line_values)

    def getSolutions(self, method):

        # Confirm that method argument is valid
        if method not in self.SOLVER_METHODS:
            raise ValueError(
                f"Invalid method. Valid method names: {self.SOLVER_METHODS.keys}")

        # Delegate to the function that uses the specified solving method
        return self.SOLVER_METHODS[method]()

    def __solveBruteForce(self):
        # TODO
        best_value = -1
        count = 0
        capacity = self.problems[0][0]
       # print(capacity)
        # for i in range(len(self.problems[0][1])):

        num_items = len(self.problems[0][1])
        items = self.problems[0][1]
        chosen_arr = np.zeros(num_items)
        for i in range(0, 2**num_items):
            j = num_items - 1
            temp_weight = 0
            temp_value = 0
            
            while (chosen_arr[j] != 0 and j >= 0):
                chosen_arr[j] = 0
                j -= 1
            chosen_arr[j] = 1

            for k in range(0, num_items):
                
                # Which problem, list of items, which item, weight
                if chosen_arr[k] == 1:
                    temp_weight += items[k][2]
                    temp_value += items[k][1]
            if temp_value > best_value and temp_weight <= capacity:
                count+=1
                best_value = temp_value

                best_choice = np.copy(chosen_arr)
                # print(best_value)
                # print(temp_weight)
                # print(best_choice)
           # print(chosen_arr)
           
        # print(best_choice)
        #print(count)
        return [item[0] for item, bit in zip(items, best_choice) if bit]


def solveKnapsackFile(filename, method="bruteForce"):
    solver = Solver()
    solver.loadProblemFromFile(filename)
    return solver.getSolutions(method)
