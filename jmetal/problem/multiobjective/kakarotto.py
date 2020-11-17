import random
from math import sqrt, exp, pow, sin
import Fitness
from jmetal.core.problem import FloatProblem, BinaryProblem, Problem
from jmetal.core.solution import FloatSolution, BinarySolution, CompositeSolution, IntegerSolution

"""
.. module:: constrained
   :platform: Unix, Windows
   :synopsis: Unconstrained test problems for multi-objective optimization

.. moduleauthor:: Antonio J. Nebro <antonio@lcc.uma.es>
"""
import itertools

class MixedIntegerFloatProblem(Problem):
    def __init__(self, obj_reader, semente, lower_upper_class, lower_upper_centroids):
        super(MixedIntegerFloatProblem, self).__init__()
        self.entrada = obj_reader
        self.isSeed= False
        self.antecedentes = []
        for antecedente in semente[0]:
            self.antecedentes += antecedente
        self.labels = semente[1]
        self.inter = len(self.antecedentes) / len(self.entrada.instancias)
        self.centroids = semente[2]
        lower_label = lower_upper_class[0]
        upper_label = lower_upper_class[1]
        number_of_integer_variables_inputs = len(self.antecedentes)
        number_of_integer_variables_outputs = len(self.labels)
        number_of_float_variables_centralPoints = len(self.centroids)
        self.maxAtual = 0


        self.number_of_objectives = 2
        self.number_of_variables = 3
        #self.number_of_constraints = 0


        self.float_lower_bound_centralPoints = [lower for lower in lower_upper_centroids[0]]
        self.float_upper_bound_centralPoints = [upper for upper in lower_upper_centroids[1]]
        self.int_lower_bound_attribute = [1 for _ in range(number_of_integer_variables_inputs)]
        self.int_upper_bound_attribute = [3 for _ in range(number_of_integer_variables_inputs)]
        self.int_lower_bound_label = [lower_label for _ in range(number_of_integer_variables_outputs)]
        self.int_upper_bound_label = [upper_label for _ in range(number_of_integer_variables_outputs)]

        self.obj_directions = [self.MAXIMIZE]
        self.obj_labels = ['Ones']

    def evaluate(self, solution: CompositeSolution) -> CompositeSolution:

        antecedentes = solution.variables[0].variables
        consequentes = solution.variables[1].variables
        centroides = solution.variables[2].variables
        #print(solution.variables[0].variables, solution.variables[1].variables, solution.variables[2].variables)
        #print(solution.variables[0].variables)
        new_antecedentes = list(self.chunks(antecedentes, len(centroides)))
        pesos =  [1]*len(antecedentes)
        #inter = len(new_antecedentes)
        regras, acuracia = Fitness.__getFitness__(self.entrada,
                                          [new_antecedentes,consequentes,centroides],
                                          pesos)
        inter = len(regras[0])/len(self.entrada.instancias)
        if (acuracia > self.maxAtual):
            self.maxAtual = acuracia
            print("evolução acc: ", acuracia)
            print(1, "evolução inter: ", len(regras[0]), inter)
        if inter < self.inter:
            self.inter = 1-inter
            print(2, "evolução inter: ", len(regras[0]) ,self.inter)

        solution.objectives[0] = self.maxAtual
        solution.objectives[1] = self.inter
        return solution

    def create_solution(self) -> CompositeSolution:
        if self.isSeed:
            self.isSeed = False
            return self.insert_seed()
        return self.random_solution()

    def get_name(self) -> str:
        return "Mixed Integer Float Problem"

    def chunks(self, lista, n):
        for i in range(0, len(lista), n):
            yield lista[i:i + n]

    def insert_seed(self):
        attributes_solution = IntegerSolution(self.int_lower_bound_attribute, self.int_upper_bound_attribute,
                                              self.number_of_objectives, self.number_of_constraints)

        labels_solution = IntegerSolution(self.int_lower_bound_label, self.int_upper_bound_label,
                                          self.number_of_objectives, self.number_of_constraints)

        points_solution = FloatSolution(self.float_lower_bound_centralPoints, self.float_upper_bound_centralPoints,
                                        self.number_of_objectives, self.number_of_constraints)

        attributes_solution.variables = self.antecedentes

        labels_solution.variables =  self.labels

        points_solution.variables =  self.centroids
        return CompositeSolution([attributes_solution, labels_solution, points_solution])

    def random_solution(self):
        attributes_solution = IntegerSolution(self.int_lower_bound_attribute, self.int_upper_bound_attribute,
                                              self.number_of_objectives, self.number_of_constraints)

        labels_solution = IntegerSolution(self.int_lower_bound_label, self.int_upper_bound_label,
                                          self.number_of_objectives, self.number_of_constraints)

        points_solution = FloatSolution(self.float_lower_bound_centralPoints, self.float_upper_bound_centralPoints,
                                        self.number_of_objectives, self.number_of_constraints)

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
