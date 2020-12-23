import random
from jmetal.core.problem import Problem
from jmetal.core.solution import FloatSolution, CompositeSolution, IntegerSolution
from AlgoritmoGenetico.Problema.Reducao_Regras import Reducao
from SistemaFuzzy.Model.Regra import Regra
from SistemaFuzzy.Raciocinio.Geral import Classificacao
from AlgoritmoGenetico.Problema.Semente import Semente
from copy import copy

class MixedIntegerFloatProblem(Problem):
    def __init__(self, particoes, regras, instancias, classes): # CONFIGURACAO DO PROBLEMA
        super(MixedIntegerFloatProblem, self).__init__()
        self.particoes = particoes
        self.regras = regras
        self.instancias = instancias
        self.classes = classes
        self.isSeed = True
        self.semente = Semente(self.regras, self.instancias, self.particoes)
        self.antecedentes, self.consequentes = self.semente.preProcessamentoRegra()
        self.lower_centroids, self.centroids, self.upper_centroids, variacao_max_conjuntos = self.semente.preProcessamentoCentroid()
        tamanho_antecedentes = len(self.antecedentes)
        tamanho_consequentes = len(self.consequentes)

        self.int_lower_bound_attribute = [-1 for _ in range(tamanho_antecedentes)]
        self.int_upper_bound_attribute = []
        for _ in range(0, len(self.antecedentes),  self.semente.qtdAntecedenteRegra):
            self.int_upper_bound_attribute += variacao_max_conjuntos
        self.int_lower_bound_label = [0 for _ in range(tamanho_consequentes)]
        self.int_upper_bound_label = [len(classes) - 1 for _ in range(tamanho_consequentes)]

        #VALORES JMETAL
        self.number_of_objectives = 2
        self.number_of_variables = 3
        self.number_of_constraints = 0
        self.obj_directions = [self.MINIMIZE]
        self.obj_labels = ['Ones']
        self.controle = 1

    def create_solution(self) -> CompositeSolution: # INICIALIZAÇÂO DO PROBLEMA
        attributes_solution = IntegerSolution(self.int_lower_bound_attribute, self.int_upper_bound_attribute,
                                              self.number_of_objectives, self.number_of_constraints)

        labels_solution = IntegerSolution(self.int_lower_bound_label, self.int_upper_bound_label,
                                          self.number_of_objectives, self.number_of_constraints)

        points_solution = FloatSolution(self.lower_centroids, self.upper_centroids,
                                        self.number_of_objectives, self.number_of_constraints)
        if self.isSeed:
            attributes_solution.variables = self.antecedentes
            labels_solution.variables = self.consequentes
            points_solution.variables = self.centroids
            self.isSeed = False
        else:
            attributes_solution.variables = \
                [random.randint(self.int_lower_bound_attribute[i], self.int_upper_bound_attribute[i]) for i in
                 range(len(self.int_lower_bound_attribute))]

            labels_solution.variables = \
                [random.randint(self.int_lower_bound_label[i], self.int_upper_bound_label[i]) for i in
                 range(len(self.int_lower_bound_label))]

            points_solution.variables = \
                [random.uniform(self.lower_centroids[i], self.upper_centroids[i]) for i
                 in range(len(self.lower_centroids))]

        return CompositeSolution([attributes_solution, labels_solution, points_solution])

    def get_name(self) -> str:
        return "Mixed Integer Float Problem"

    def alterar_centroids(self, cromossomo_centroids):
        index = 0
        particoes = []
        for particao in self.particoes:
            particao = copy(particao)
            tamanhoPontoCentral = len(particao.pontosCentrais)
            p_centrais_atuais = cromossomo_centroids[index:index + tamanhoPontoCentral]
            particao.setPontosCentrais(p_centrais_atuais)
            index += tamanhoPontoCentral
            particoes.append(particao)
        return particoes

    def cromossomo_para_regras(self, cromossomo_antecedentes, cromossomo_consequente, tam_antecedentes, particoes):
        regras = []
        for index_classe, salto in enumerate(range(0, len(cromossomo_antecedentes), tam_antecedentes)):
            antecedentes = cromossomo_antecedentes[salto:salto+tam_antecedentes]
            consequente = cromossomo_consequente[index_classe]
            regra = Regra(antecedentes, consequente, 0)
            regras.append(regra)
        return Reducao(regras, self.instancias, particoes).reduzir()

    def evaluate(self, solution: CompositeSolution) -> CompositeSolution:
        antecedentes = solution.variables[0].variables
        consequentes = solution.variables[1].variables
        centroides = solution.variables[2].variables
        particoes = self.alterar_centroids(centroides)
        new_regras = self.cromossomo_para_regras(antecedentes, consequentes, self.semente.qtdAntecedenteRegra, particoes)
        classificacao = Classificacao(particoes, new_regras, self.instancias, self.classes)
        acuracia, interpretabilidadeCondicoes = classificacao.classificar()
        solution.objectives[0] = -acuracia
        solution.objectives[1] = -interpretabilidadeCondicoes
        return solution