import numpy as np
from Stack import Stack

class Solver:

    def __init__(self):

        # Constant dict that maps solving method parameter name to the corresponding function name
        self.SOLVER_METHODS = {
            "bruteForce": self.__solveBruteForce,
            "backtrack": self.__solveBacktrack,
            "branchAndBound": self.__solveBranchAndBound
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
                f"Invalid method. Valid method names: {', '.join(self.SOLVER_METHODS.keys())}")

        # Delegate to the function that uses the specified solving method
        return self.SOLVER_METHODS[method]()

    def __solveBruteForce(self):
        # TODO
        best_value = -1
        
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
                best_value = temp_value

                best_choice = np.copy(chosen_arr)
                # print(best_value)
                # print(temp_weight)
                # print(best_choice)
           # print(chosen_arr)
           
        # print(best_choice)
        
        return [item[0] for item, bit in zip(items, best_choice) if bit]
    
    def __solveBacktrack(self):
        best_value = -1
        best_choice = []

        capacity = self.problems[0][0]
        items = self.problems[0][1]
        num_items = len(items)

        stack = Stack() # Contains (curr_pack_indices: [], next_index, curr_value, curr_weight) tuples
        stack.push(([], 0, 0, 0))
        
        while not stack.is_empty():
            curr_pack_indices, next_index, curr_value, curr_weight = stack.pop()
            next_item = items[next_index]
            pack_indices_with_next_item = curr_pack_indices + [next_index]
            next_weight = curr_weight + next_item[2]
            next_value = curr_value + next_item[1]
            if next_weight <= capacity and next_value > best_value:
                best_value = next_value
                best_choice = pack_indices_with_next_item
            if next_index <= num_items - 2:
                if next_weight < capacity:
                    stack.push((pack_indices_with_next_item, next_index + 1, next_value, next_weight))
                stack.push((curr_pack_indices, next_index + 1, curr_value, curr_weight))
        
        return [items[i][0] for i in best_choice]

    def __solveBranchAndBound(self):
        best_value = -1
        best_choice_complement = []

        capacity = self.problems[0][0]
        items = self.problems[0][1]
        num_items = len(items)

        stack = Stack() # Contains (removed_items_indices: [], next_index, curr_value, curr_weight) tuples
        stack.push(([], 0, sum(item[1] for item in items), sum(item[2] for item in items)))
        
        while not stack.is_empty():
            removed_items_indices, next_index, curr_value, curr_weight = stack.pop()
            next_item = items[next_index]
            removed_indices_with_next_item = removed_items_indices + [next_index]
            next_weight = curr_weight - next_item[2]
            next_value = curr_value - next_item[1]
            
            still_overweight = next_weight > capacity
            next_is_best_value = next_value > best_value

            if not still_overweight and next_is_best_value:
                best_value = next_value
                best_choice_complement = removed_indices_with_next_item
            
            if next_index <= num_items - 2:
                if still_overweight and next_is_best_value: # here's the bounding; not interested in the subtree resulting from removing next_item if doing so put us below the weight threshold or below the best value so far, since removing more won't help in either case
                    stack.push((removed_indices_with_next_item, next_index + 1, next_value, next_weight))
                stack.push((removed_items_indices, next_index + 1, curr_value, curr_weight))
                
        return [items[i][0] for i in range(num_items) if i not in best_choice_complement]



def solveKnapsackFile(filename, method="bruteForce"):
    solver = Solver()
    solver.loadProblemFromFile(filename)
    return solver.getSolutions(method)
