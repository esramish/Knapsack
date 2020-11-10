from backpack import solveKnapsackFile, Solver
import unittest

class BackpackTest(unittest.TestCase):

    def testMethodsOnFile(self, problems_filename="problems/problems_size10.txt", solutions_filename="problems/problems_size10_solutions.txt"):
        with open(solutions_filename) as f:
            expected_solution_string = next(f)
        expected_solution = eval(expected_solution_string)

        solver = Solver()
        solver.loadProblemFromFile(problems_filename)
        for method in solver.SOLVER_METHODS:
            print(f"Testing {method}...")
            self.assertEqual(solver.getSolutions(method), expected_solution, f"\n\n\n\nThis failure occurred when testing {method}.")
            print(f"{method} test was successful.")


def main(run_unit_tests=True):
    solution = solveKnapsackFile("problems/problems_size10.txt")
    print(solution)
    if run_unit_tests:
        print("\n----------------------------------------------------------------------\nNow running unit tests.\n")
        unittest.main()

if __name__ == '__main__':
    main()