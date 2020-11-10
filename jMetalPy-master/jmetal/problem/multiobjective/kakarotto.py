import random
from math import sqrt, exp, pow, sin

from jmetal.core.problem import FloatProblem, BinaryProblem, Problem
from jmetal.core.solution import FloatSolution, BinarySolution, CompositeSolution, IntegerSolution

"""
.. module:: constrained
   :platform: Unix, Windows
   :synopsis: Unconstrained test problems for multi-objective optimization

.. moduleauthor:: Antonio J. Nebro <antonio@lcc.uma.es>
"""


class MixedIntegerFloatProblem(Problem):
    def __init__(self):
        super(MixedIntegerFloatProblem, self).__init__()
        entradas = [1,2,1,1,2,3,1,2,1,2,2,2]
        saida = [-3,-2,-1]
        pontos = [5.8, 8.9, 7.5, 3.8]

        number_of_integer_variables_inputs = len(entradas)
        number_of_integer_variables_outputs = len(saida)
        number_of_float_variables_centralPoints = len(pontos)

        lower_label = saida[0]
        upper_label = saida[2]

        self.number_of_objectives = 2
        self.number_of_variables = 3
        #self.number_of_constraints = 0


        self.float_lower_bound_centralPoints = [2 for _ in range(number_of_float_variables_centralPoints)]
        self.float_upper_bound_centralPoints = [10 for _ in range(number_of_float_variables_centralPoints)]
        self.int_lower_bound_attribute = [1 for _ in range(number_of_integer_variables_inputs)]
        self.int_upper_bound_attribute = [3 for _ in range(number_of_integer_variables_inputs)]
        self.int_lower_bound_label = [lower_label for _ in range(number_of_integer_variables_outputs)]
        self.int_upper_bound_label = [upper_label for _ in range(number_of_integer_variables_outputs)]

        self.obj_directions = [self.MINIMIZE]
        self.obj_labels = ['Ones']

    def evaluate(self, solution: CompositeSolution) -> CompositeSolution:

        antecedentes = solution.variables[0].variables
        consequentes = solution.variables[1].variables
        centroides = solution.variables[2].variables
        #print(solution.variables[0].variables, solution.variables[1].variables, solution.variables[2].variables)
        #print(solution.variables[0].variables)
        solution.objectives[0] = 1
        solution.objectives[1] = 1
        return solution

    def create_solution(self) -> CompositeSolution:
        attributes_solution = IntegerSolution(self.int_lower_bound_attribute, self.int_upper_bound_attribute, self.number_of_objectives, self.number_of_constraints)

        labels_solution = IntegerSolution(self.int_lower_bound_label, self.int_upper_bound_label, self.number_of_objectives, self.number_of_constraints)

        points_solution = FloatSolution(self.float_lower_bound_centralPoints,self.float_upper_bound_centralPoints,self.number_of_objectives, self.number_of_constraints)

        attributes_solution.variables = \
            [random.randint(self.int_lower_bound_attribute[i], self.int_upper_bound_attribute[i]) for i in
             range(len(self.int_lower_bound_attribute))]

        labels_solution.variables = \
            [random.randint(self.int_lower_bound_label[i], self.int_upper_bound_label[i]) for i in
             range(len(self.int_lower_bound_label))]

        points_solution.variables = \
            [random.uniform(self.float_lower_bound_centralPoints[i], self.float_upper_bound_centralPoints[i]) for i in
             range(len(self.float_lower_bound_centralPoints))]


        return CompositeSolution([attributes_solution, labels_solution, points_solution])

    def get_name(self) -> str:
        return "Mixed Integer Float Problem"

