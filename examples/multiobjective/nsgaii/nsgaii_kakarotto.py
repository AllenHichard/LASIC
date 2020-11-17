from jmetal.algorithm.multiobjective.nsgaii import NSGAII
from jmetal.operator import SBXCrossover, PolynomialMutation, IntegerPolynomialMutation
from jmetal.operator.crossover import CompositeCrossover, IntegerSBXCrossover
from jmetal.operator.mutation import CompositeMutation
from jmetal.problem.multiobjective.kakarotto import MixedIntegerFloatProblem
from jmetal.util.solution import get_non_dominated_solutions, print_function_values_to_file, \
    print_variables_to_file
from jmetal.util.termination_criterion import StoppingByEvaluations

def nsgaii_train( obj_reader, semente, lower_upper_class, lower_upper_centroids):
    problem = MixedIntegerFloatProblem(obj_reader, semente, lower_upper_class, lower_upper_centroids)

    max_evaluations = 25000
    algorithm = NSGAII(
        problem=problem,
        population_size=100,
        offspring_population_size=100,
        mutation=CompositeMutation([IntegerPolynomialMutation(0.05, 20),
                                    IntegerPolynomialMutation(0.05, 20),
                                    PolynomialMutation(0.05, 20.0)]),
        crossover=CompositeCrossover([IntegerSBXCrossover(probability=0.95, distribution_index=20),
                                      IntegerSBXCrossover(probability=0.95, distribution_index=20),
                                      SBXCrossover(probability=0.95, distribution_index=20)]),
        termination_criterion=StoppingByEvaluations(max_evaluations=max_evaluations)
    )

    algorithm.run()
    front = get_non_dominated_solutions(algorithm.get_result())

    # Save results to file
    print_function_values_to_file(front, 'FUN.' + algorithm.label)
    print_variables_to_file(front, 'VAR.' + algorithm.label)

    print('Algorithm (continuous problem): ' + algorithm.get_name())
    print('Problem: ' + problem.get_name())
    print('Computing time: ' + str(algorithm.total_computing_time))
