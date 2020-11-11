from backpack import solveKnapsackFile, Solver
import unittest
import time
import matplotlib.pyplot as plt

class BackpackTest(unittest.TestCase):

    def testMethodsOnFile(self, problems_filename="problems_size10.txt", solutions_filename="problems_size10_solutions.txt"):
        
        # Locate solutions file
        try:
            f = open(solutions_filename)
        except FileNotFoundError:
            f = open('problems/' + solutions_filename)
        
        # Load expected solutions
        expected_solution_string = next(f)
        expected_solution = eval(expected_solution_string)
        f.close()

        # Test each algorithm that the solver currently supports
        solver = Solver()
        solver.loadProblemFromFile(problems_filename)
        for method in solver.SOLVER_METHODS:
            print(f"Testing {method}...")
            self.assertEqual(solver.getSolutions(method), expected_solution, f"\n\n\n\nThis failure occurred when testing {method}.")
            print(f"{method} test was successful.")


def produce_plots():
    
    SIZES = [10, 15, 20]
    timings = dict() # maps file's approximate problem size to time to solve entire file

    for size in SIZES:

        # Record how long the file for this size takes
        start = time.perf_counter()
        solution = solveKnapsackFile(f"problems_size{size}.txt")
        end = time.perf_counter()
        timings[size] = end - start

        # No need to plot just one datapoint
        if len(timings) == 1: 
            continue
        
        # Plot all the datapoints so far; this way the user can kill the program once the graphs are taking too long to generate, but still see graphs on the way to that point
        plt.title(f"Timings for Problem Sizes {', '.join([str(size) for size in timings])}")
        plt.xlabel("Approximate Problem Size")
        plt.ylabel("Running Time (sec)")
        plt.xticks(ticks=list(timings.keys()))
        plt.plot(list(timings.keys()), list(timings.values()))
        plt.show()


def main(run_unit_tests=True, plot=False):
    
    # Print a demo solution
    demo_filename = "problems_size15.txt"
    print(f"Solution for {demo_filename}:")
    solution = solveKnapsackFile("problems_size15.txt")
    print(solution)

    # Run tests and produce plots, if so desired
    if run_unit_tests:
        print("\n----------------------------------------------------------------------\nNow running unit tests on all knapsack implementations.\n")
        unittest.main()
    if plot:
        produce_plots()

if __name__ == '__main__':
    main()
