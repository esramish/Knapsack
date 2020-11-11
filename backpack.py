import numpy as np
from Stack import Stack
from itertools import combinations
import time


class Solver:
    '''A class for storing and solving Knapsack Problem instances.'''
    
    def __init__(self):

        # Constant dict that maps solving method parameter name to the corresponding function name
        self.SOLVER_METHODS = {
            "bruteForce": self.__solveBruteForce,
            "backtrack": self.__solveBacktrack,
            "branchAndBound": self.__solveBranchAndBound,
            "meetInMiddle": self.__solveMiddle
        }

    def loadProblemFromFile(self, filename):
        '''Load the problems represented in the specified text file into this Solver.'''

        # List of (max_weight, [items]) tuples. Each item is a tuple of (name, value, weight)
        self.problems = []

        try:
            f = open(filename)
        except FileNotFoundError:
            f = open('problems/' + filename)

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
        
        f.close()

    def getSolutions(self, method, verbosity=0):
        '''Solve all of the problem instances loaded into this Solver, using the specified internal algorithm.'''

        # Confirm that method argument is valid
        if method not in self.SOLVER_METHODS:
            raise ValueError(f"Invalid method. Valid method names: {', '.join(self.SOLVER_METHODS.keys())}")

        # Delegate to the function that uses the specified solving method; return a list of solutions for the whole file
        solutions = []
        for i in range(len(self.problems)):
            start = time.perf_counter()
            problem_instance_solution = self.SOLVER_METHODS[method](i)
            end = time.perf_counter()
            solutions.append(sorted(problem_instance_solution))
            if verbosity == 1:
                print(f"Solved {i + 1}/{len(self.problems)} ({'%.3f' % (end - start)} sec)")
        return solutions

    def __solveBruteForce(self, problem_index):
        '''Solve using a brute force implementation. 
        
        The general idea for this implementation comes from http://www.micsymposium.org/mics_2005/papers/paper102.pdf'''

        # Constants for this problem instance
        capacity = self.problems[problem_index][0]
        items = self.problems[problem_index][1]
        num_items = len(items)

        # Variable to track of the highest value so far
        best_value = -1

        # A numpy array that represents a binary number that increments each time through the loop
        chosen_arr = np.zeros(num_items)

        # Loop 2^n times
        for i in range(0, 2**num_items):
            
            # Reset variables that will be used below
            j = num_items - 1
            temp_weight = 0
            temp_value = 0
            
            # Increment the binary number that chosen_arr represents
            while (chosen_arr[j] != 0 and j >= 0):
                chosen_arr[j] = 0
                j -= 1
            chosen_arr[j] = 1

            # Add up the values and weights of the chosen items
            for k in range(0, num_items):
                if chosen_arr[k] == 1:
                    temp_weight += items[k][2] # Indices meaning: which item, item weight
                    temp_value += items[k][1] # Indices meaning: which item, item value
            
            # If this is the best legal value so far, update variables accordingly
            if temp_value > best_value and temp_weight <= capacity:
                best_value = temp_value
                best_choice = np.copy(chosen_arr)
        
        # Convert binary list to a list of chosen item names; return it
        return [item[0] for item, bit in zip(items, best_choice) if bit]
    
    def __solveBacktrack(self, problem_index):
        '''Solve using an iterative backtracking implementation.'''

        # Constants for this problem instance
        capacity = self.problems[problem_index][0]
        items = self.problems[problem_index][1]
        num_items = len(items)
        
        # Variables to track the highest value so far and the corresponding items
        best_value = -1
        best_choice = []

        # Create a stack of "knapsack situations," each of which is a (curr_pack_indices: [], next_index, curr_value, curr_weight) tuple.
        # Push to it an empty knapsack where all the items starting with index 0 are still fair game for adding
        stack = Stack()
        stack.push(([], 0, 0, 0))
        
        # Iterate until we've addressed all hypothetical knapsack situations
        while not stack.is_empty():

            # Pop a knapsack situation 
            curr_pack_indices, next_index, curr_value, curr_weight = stack.pop()
            
            # The next item to cause situation branching by being added or not
            next_item = items[next_index] 
            
            # The variables representing the situation in which this next item is added
            pack_indices_with_next_item = curr_pack_indices + [next_index]
            next_weight = curr_weight + next_item[2]
            next_value = curr_value + next_item[1]

            # If this is the best legal value so far, update variables accordingly
            if next_weight <= capacity and next_value > best_value:
                best_value = next_value
                best_choice = pack_indices_with_next_item
            
            # If there are still more items remaining to add or not add, push those situations to the situation stack
            if next_index <= num_items - 2:
                
                # Here's the backtracking!!! Only push the situation with this item added if it doesn't put the knapsack over capacity
                if next_weight < capacity:
                    stack.push((pack_indices_with_next_item,
                                next_index + 1, next_value, next_weight))
                
                # Regardless of that next item's weight, push the situation in which it wasn't added
                stack.push((curr_pack_indices, next_index + 1, 
                            curr_value, curr_weight))
        
        # Convert list of chosen item indices to a list of chosen item names; return it
        return [items[i][0] for i in best_choice]

    def __solveBranchAndBound(self, problem_index):
        '''Solve using an iterative branch and bound implementation.'''

        # Constants for this problem instance
        capacity = self.problems[problem_index][0]
        items = self.problems[problem_index][1]
        num_items = len(items)

        # Variables to track the highest value so far and the corresponding items
        best_value = -1
        best_choice_complement = [] # That is, the indices of the items that are NOT in the knapsack in the best case so far

        # Create a stack of "knapsack situations," each of which is a (removed_items_indices: [], next_index, curr_value, curr_weight) tuple. 
        # Push to it a full knapsack where all the items starting with index 0 are still fair game for removing
        stack = Stack()
        stack.push(([], 0, sum(item[1] for item in items), 
                    sum(item[2] for item in items)))
        
        # Iterate until we've addressed all hypothetical knapsack situations
        while not stack.is_empty():
            
            # Pop a knapsack situation
            removed_items_indices, next_index, curr_value, curr_weight = stack.pop()
            
            # The next item to cause situation branching by being removed or not
            next_item = items[next_index]
            
            # The variables representing the situation in which this next item is removed
            removed_indices_with_next_item = removed_items_indices + \
                [next_index]
            next_weight = curr_weight - next_item[2]
            next_value = curr_value - next_item[1]
            still_overweight = next_weight > capacity
            next_is_best_value = next_value > best_value

            # If this is the best legal value so far, update variables accordingly
            if not still_overweight and next_is_best_value:
                best_value = next_value
                best_choice_complement = removed_indices_with_next_item
            
            # If there are still more items remaining to remove or not remove, push those situations to the situation stack
            if next_index <= num_items - 2:
                
                # Here's the bounding!!! Not interested in the subtree resulting from removing next_item 
                # if doing so puts us below the weight threshold or below the best value so far, 
                # since removing more items in addition to that one won't help in either of those cases.
                if still_overweight and next_is_best_value: 
                    stack.push((removed_indices_with_next_item, 
                                next_index + 1, next_value, next_weight))
                
                # Regardless of that next item's weight and value, push the situation in which it wasn't removed
                stack.push((removed_items_indices, next_index + 1, 
                            curr_value, curr_weight))
        
        # Convert list of *non-chosen* item indices to a list of *chosen* item names; return it
        return [items[i][0] for i in range(num_items) if i not in best_choice_complement]

    def __solveMiddle(self, problem_index):
        '''Solve using a Meet in the Middle implementation. 

        The general idea for this implementation comes from https://en.wikipedia.org/wiki/Knapsack_problem#Meet-in-the-middle'''

        #count = 0
        capacity = self.problems[problem_index][0]
        items = self.problems[problem_index][1]

        #Partition the list of items into two approximately equal sized lists
        items_a, items_b = np.array_split(items, 2)

        #Find the power set of each list
        subsets_a = self.findSubsets(items_a)
        subsets_b = self.findSubsets(items_b)
       
        #Sort b's subsets
        subsets_b_python_list = list(subsets_b)
        subsets_b_python_list.sort(key = lambda x: x[2])
        subsets_b = np.array(subsets_b_python_list)
        
        best_set = []
        for sub_a, a_values, a_weight in subsets_a:
       
            sub_best_values = -1
            #Remember the highest value subset for each subset in subsets_a
            good_set = []
            for sub_b, b_values, b_weight in subsets_b:
                
                if a_values + b_values > sub_best_values and a_weight + b_weight <= capacity:
                    sub_best_values = a_values + b_values
                    good_set = np.concatenate((sub_a, sub_b))
                elif a_weight + b_weight > capacity:
                    break
            #Update the best set
            if self.sumValues(good_set) > self.sumValues(best_set):
               
                best_set = np.copy(good_set)

        return [best_set[i][0] for i in range(len(best_set))]

    def findSubsets(self, items):
        '''Return the list of all non-empty subsets of a given list.'''

        sub_list = []
        #Iteration begins at 1 because we don't need the empty set
        for i in range(1, len(items)+1):
            for subset in combinations(items, i):
                sub_list.append((subset, self.sumValues(subset), self.sumWeights(subset)))
        return np.array(sub_list)

    def sumWeights(self, items):
        '''Return the sum of the weights of the given list of items.'''
        sum = 0
        for i in range(len(items)):

            sum += int(items[i][2])
        return sum

    def sumValues(self, items):
        '''Return the sum of the values of the given list of items.'''
        sum = 0
        for i in range(len(items)):
            sum += int(items[i][1])
        return sum

def solveKnapsackFile(filename, method="meetInMiddle", verbosity=0):
    '''A wrapper function for solving the problems in a file; load the file into a Solver instance and get the solutions using the specified method.'''
    solver = Solver()
    solver.loadProblemFromFile(filename)
    return solver.getSolutions(method, verbosity)
