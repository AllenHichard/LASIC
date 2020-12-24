from jmetal.algorithm.multiobjective.nsgaii import NSGAII
from jmetal.operator import SBXCrossover, PolynomialMutation, IntegerPolynomialMutation
from jmetal.operator.crossover import CompositeCrossover, IntegerSBXCrossover
from jmetal.operator.mutation import CompositeMutation
from AlgoritmoGenetico.Problema.problem_nsgaii_fuzzy import MixedIntegerFloatProblem
from jmetal.util.solution import get_non_dominated_solutions, print_function_values_to_file, \
    print_variables_to_file
from jmetal.util.termination_criterion import StoppingByEvaluations

def nsgaii_train(particoes, regras, instancias, classes):
    problem = MixedIntegerFloatProblem(particoes, regras, instancias, classes)

    max_evaluations = 10
    algorithm = NSGAII(
        problem=problem,
        population_size=10,
        offspring_population_size=10,
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

    minAcuracia = 0
    index = -1
    for i, f in enumerate(front):
        if minAcuracia > f.objectives[0]:
            minAcuracia =  f.objectives[0]
            index = i

    #for variable in front[index].variables:
       #print(variable.variables)


    particoes = problem.alterar_centroids(front[index].variables[2].variables)
    new_regras = problem.cromossomo_para_regras(front[index].variables[0].variables, front[index].variables[1].variables, problem.semente.qtdAntecedenteRegra, particoes)
    return particoes, new_regras

    #for i in particoes:
        #print(i.plotParticao())




