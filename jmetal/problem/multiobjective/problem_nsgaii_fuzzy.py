import random
from math import sqrt, exp, pow, sin
import Fitness
from jmetal.core.problem import FloatProblem, BinaryProblem, Problem
from jmetal.core.solution import FloatSolution, BinarySolution, CompositeSolution, IntegerSolution
from Reducao_Regras import Reducao
from ClassificadorFuzzy.Model.Regra import Regra
from ClassificadorFuzzy.SistemaFuzzy.Raciocinio.Geral import Classificacao
"""
.. module:: constrained
   :platform: Unix, Windows
   :synopsis: Unconstrained test problems for multi-objective optimization

.. moduleauthor:: Antonio J. Nebro <antonio@lcc.uma.es>
"""
import itertools


"""from Config import ParametrosJSON as json
inputs = json.getArcEntrada()
fuzzy, ag = inputs['SISTEMA']
conjuntos = inputs['CONJUNTO_FUZZY']
granularidade = inputs['GRANULARIDADE']
composicao = inputs['OPERADOR_COMPOSICAO']
agregacao = inputs['OPERADOR_AGREGACAO']
inferencia = inputs['INFERENCIA']
seed = inputs["SEMENTE"]
temPeso = inputs['PESOS']
default = inputs['DEFAULT']
"""



class MixedIntegerFloatProblem(Problem):
    def __init__(self, particoes, regras, pesos, instancias, classes):
        super(MixedIntegerFloatProblem, self).__init__()
        self.particoes = particoes
        self.regras = regras
        self.pesos = pesos
        self.interacao = 0
        self.instancias = instancias
        self.classes = classes
        self.antecedentes = []
        self.consequentes = []
        self.isSeed = True
        for regra in self.regras:
            self.antecedentes += regra.antecedentes
            self.consequentes.append(regra.consequente)
        self.interpretabilidadeInicial = len(self.regras) / len(self.instancias)
        self.centroids = [particao.pico for particao in self.particoes]
        self.inicios = [particao.inicio for particao in self.particoes]
        self.fins = [particao.fim for particao in self.particoes]
        self.lower_centroids = []
        self.upper_centroids = []
        for inicio, fim, pontoMedio in zip(self.inicios, self.fins, self.centroids):
            (limite_inferior, limite_superior) = self.lower_upper_centroids(inicio, fim, pontoMedio)
            self.lower_centroids.append(limite_inferior)
            self.upper_centroids.append(limite_superior)
        number_of_integer_variables_inputs = len(self.antecedentes)
        number_of_integer_variables_outputs = len(self.consequentes)
        number_of_float_variables_centralPoints = len(self.centroids)
        self.maxAtual = 0
        self.number_of_objectives = 2
        self.number_of_variables = 3
        #self.number_of_constraints = 0

        self.int_lower_bound_attribute = [0 for _ in range(number_of_integer_variables_inputs)]
        self.int_upper_bound_attribute = [2 for _ in range(number_of_integer_variables_inputs)]
        self.int_lower_bound_label = [0 for _ in range(number_of_integer_variables_outputs)]
        self.int_upper_bound_label = [len(classes)-1 for _ in range(number_of_integer_variables_outputs)]
        self.float_lower_bound_centralPoints = [lower for lower in  self.lower_centroids]
        self.float_upper_bound_centralPoints = [upper for upper in self.upper_centroids]

        self.obj_directions = [self.MINIMIZE]
        self.obj_labels = ['Ones']

        self.maiorInterpretabilidade = 0
        self.maiorAcuracia = 0

    def lower_upper_centroids(self, inicio, fim, pontoMedio):
        PI = inicio
        PS = fim
        PM = pontoMedio
        vi = PM - ((PM - PI) / 2)
        vs = PM + ((PS - PM) / 2)
        lower_centroids = vi
        upper_centroids = vs
        return lower_centroids, upper_centroids

    def evaluate(self, solution: CompositeSolution) -> CompositeSolution:
        if self.interacao % 1000 == 0:
            #print(self.interacao)
            pass
        self.interacao += 1
        antecedentes = solution.variables[0].variables
        consequentes = solution.variables[1].variables
        centroides = solution.variables[2].variables
        new_regras = self.cromossomo_para_regras(antecedentes, consequentes, len(centroides))
        particoes = self.alterar_centroids(centroides)
        resultadoTrain = Classificacao(particoes, new_regras, self.pesos, self.instancias, self.classes)
        acuracia = resultadoTrain.classificar()
        interpretabilidade =  (1 - len(new_regras) / len(self.instancias))
        #print(acuracia, interpretabilidade)


        if (acuracia > self.maiorAcuracia):
            self.maiorAcuracia = acuracia
            self.maiorInterpretabilidade = interpretabilidade
            print("evolução acc: ", acuracia, "evolução inter: ", len(new_regras) ,self.maiorInterpretabilidade)
        if acuracia >=  self.maiorAcuracia and interpretabilidade > self.maiorInterpretabilidade:
            self.maiorInterpretabilidade = interpretabilidade
            print("evolução acc: ", acuracia, "evolução inter: ", len(new_regras) ,self.maiorInterpretabilidade)

        solution.objectives[0] = -acuracia
        solution.objectives[1] = -interpretabilidade
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

    def alterar_centroids(self, cromossomo_centroids):
        particoes = []
        for particao, pontoCentral in zip(self.particoes, cromossomo_centroids):
            particao.pico = pontoCentral
            particoes.append(particao)
        return particoes

    def cromossomo_para_regras(self, cromossomo_antecedentes, cromossomo_consequente, tam_antecedentes):
        regras = []
        for index_classe, salto in enumerate(range(0, len(cromossomo_antecedentes), tam_antecedentes)):
            antecedentes = cromossomo_antecedentes[salto:salto+tam_antecedentes]
            consequente = cromossomo_consequente[index_classe]
            regra = Regra(antecedentes, consequente, 1, 1)
            regras.append(regra)
            #print(index_classe, regra.__str__())
        return Reducao(regras, self.instancias, self.particoes).reduzir()

    def insert_seed(self):
        attributes_solution = IntegerSolution(self.int_lower_bound_attribute, self.int_upper_bound_attribute,
                                              self.number_of_objectives, self.number_of_constraints)

        labels_solution = IntegerSolution(self.int_lower_bound_label, self.int_upper_bound_label,
                                          self.number_of_objectives, self.number_of_constraints)

        points_solution = FloatSolution(self.float_lower_bound_centralPoints, self.float_upper_bound_centralPoints,
                                        self.number_of_objectives, self.number_of_constraints)

        attributes_solution.variables = self.antecedentes

        labels_solution.variables =  self.consequentes

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

