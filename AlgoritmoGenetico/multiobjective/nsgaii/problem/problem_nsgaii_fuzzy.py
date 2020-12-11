import random
from jmetal.core.problem import Problem
from jmetal.core.solution import FloatSolution, CompositeSolution, IntegerSolution
from AlgoritmoGenetico.Reducao_Regras import Reducao
from SistemaFuzzy.Model.Regra import Regra
from SistemaFuzzy.Raciocinio.Geral import Classificacao
"""
.. module:: constrained
   :platform: Unix, Windows
   :synopsis: Unconstrained test problems for multi-objective optimization

.. moduleauthor:: Antonio J. Nebro <antonio@lcc.uma.es>
"""

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
    def __init__(self, particoes, regras, instancias, classes):
        super(MixedIntegerFloatProblem, self).__init__()
        self.particoes = particoes
        self.numeroAntecedentes = len(regras[0].antecedentes)
        self.maxAtributos = len(instancias)*(len(regras[0].antecedentes)+1)
        self.regras = regras
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
        #self.centroids = [particao.pontosCentrais for particao in self.particoes]
        self.centroids = []
        self.inicios = [particao.inicio for particao in self.particoes]
        self.fins = [particao.fim for particao in self.particoes]
        self.lower_centroids = []
        self.upper_centroids = []
        """
        for inicio, fim, pontoMedio in zip(self.inicios, self.fins, self.centroids):
            (limite_inferior, limite_superior) = self.lower_upper_centroids(inicio, fim, pontoMedio)
            self.lower_centroids.append(limite_inferior)
            self.upper_centroids.append(limite_superior)
        """
        """
               self.int_lower_bound_attribute = [-1 for _ in range(number_of_integer_variables_inputs)]
               self.int_upper_bound_attribute = [2 for _ in range(number_of_integer_variables_inputs)]
               self.int_lower_bound_label = [0 for _ in range(number_of_integer_variables_outputs)]
               self.int_upper_bound_label = [len(classes)-1 for _ in range(number_of_integer_variables_outputs)]
               """

        number_of_integer_variables_inputs = len(self.antecedentes)
        number_of_integer_variables_outputs = len(self.consequentes)
        number_of_float_variables_centralPoints = len(self.centroids)
        self.maxAtual = 0
        self.number_of_objectives = 2
        self.number_of_variables = 3
        #self.number_of_constraints = 0


        self.float_lower_bound_centralPoints = []
        self.float_upper_bound_centralPoints = []
        variacao_max_particoes = []
        for particao in self.particoes:
            self.float_lower_bound_centralPoints += particao.limiteInferior
            self.float_upper_bound_centralPoints += particao.limiteSuperior
            self.centroids += particao.pontosCentrais
            variacao_max_particoes.append(len(particao.tiposConjunto)-1)

        #print(variacao_max_particoes)
        self.int_lower_bound_attribute = [-1 for _ in range(number_of_integer_variables_inputs)]
        self.int_upper_bound_attribute = []


        for _ in range(0, len(self.antecedentes),  self.numeroAntecedentes):
            self.int_upper_bound_attribute +=variacao_max_particoes



        self.int_lower_bound_label = [0 for _ in range(number_of_integer_variables_outputs)]
        self.int_upper_bound_label = [len(classes) - 1 for _ in range(number_of_integer_variables_outputs)]

        #print(self.int_lower_bound_attribute)
        #print(self.int_upper_bound_attribute)

        #self.float_lower_bound_centralPoints = [particao for particao in  self.particoes]
        #self.float_upper_bound_centralPoints = [upper for upper in self.upper_centroids]

        self.obj_directions = [self.MINIMIZE]
        self.obj_labels = ['Ones']

        self.maiorInterpretabilidade = 0
        self.maiorAcuracia = 0

    """
    def lower_upper_centroids(self, inicio, fim, pontoMedio):
        PI = inicio
        PS = fim
        PM = pontoMedio
        vi = PM - ((PM - PI) / 2)
        vs = PM + ((PS - PM) / 2)
        lower_centroids = vi
        upper_centroids = vs
        return lower_centroids, upper_centroids
    """

    def evaluate(self, solution: CompositeSolution) -> CompositeSolution:
        if self.interacao % 1000 == 0:
            #print(self.interacao)
            pass
        self.interacao += 1
        antecedentes = solution.variables[0].variables
        consequentes = solution.variables[1].variables
        centroides = solution.variables[2].variables
        new_regras = self.cromossomo_para_regras(antecedentes, consequentes, self.numeroAntecedentes)
        #particoes = self.alterar_centroids(centroides)
        self.alterar_centroids(centroides)
        resultadoTrain = Classificacao(self.particoes, new_regras, self.instancias, self.classes)
        acuracia = resultadoTrain.classificar()
        interpretabilidade =  (1 - len(new_regras) / len(self.instancias))
        #print(acuracia, interpretabilidade)

        count = 0
        for r in new_regras:
            lista = r.antecedentes
            count += len(lista) + 1
            count -= lista.count(-1)
        interpretabilidade = (1 - count / self.maxAtributos)

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
        index = 0
        for particao in self.particoes:
            tamanhoPontoCentral = len(particao.pontosCentrais)
            #print(tamanhoPontoCentral)
            p_centrais_atuais = cromossomo_centroids[index:index + tamanhoPontoCentral]
            particao.setPontosCentrais(p_centrais_atuais)
            index += tamanhoPontoCentral

    def cromossomo_para_regras(self, cromossomo_antecedentes, cromossomo_consequente, tam_antecedentes):
        regras = []
        for index_classe, salto in enumerate(range(0, len(cromossomo_antecedentes), tam_antecedentes)):
            antecedentes = cromossomo_antecedentes[salto:salto+tam_antecedentes]
            consequente = cromossomo_consequente[index_classe]
            regra = Regra(antecedentes, consequente, 0)
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

