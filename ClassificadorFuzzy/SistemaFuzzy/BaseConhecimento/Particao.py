import numpy as np
import skfuzzy as fuzz
import matplotlib.pyplot as plt

class Particao:

    def __init__(self, inicio, fim, discretizacao, tiposConjunto):
        self.inicio = inicio
        self.fim = fim
        self.discretizacao = discretizacao
        self.tiposConjunto = tiposConjunto
        self.conjuntos = []
        self.eixo_x = np.arange(inicio, fim, (fim - inicio) / (discretizacao - 1))
        self.eixo_x[len(self.eixo_x) - 1] = fim
        self.largura_base_superior = (fim - inicio) / (2*len(tiposConjunto) - 1)
        self.largura_base_inferior = (fim - inicio) / (len(tiposConjunto) + 1)
        self.ponto_referencial = inicio

    def calculaParticaoTriangular(self):
        pontoInicial = self.ponto_referencial
        pontoMedio = self.ponto_referencial + self.largura_base_inferior
        pontoFinal = self.ponto_referencial +self.largura_base_inferior * 2
        self.ponto_referencial += self.largura_base_inferior
        return fuzz.trimf(self.eixo_x, [pontoInicial, pontoMedio,pontoFinal])

    def calcularParticaoTrapezoidal(self, index):
        pontoInicial = self.ponto_referencial
        pontoMedio = self.ponto_referencial + self.largura_base_inferior
        pontoFinal = self.ponto_referencial + self.largura_base_inferior * 2
        if index == 0:
            trapezio = [pontoInicial, pontoInicial, pontoMedio, pontoFinal]
        elif index == len(self.tiposConjunto) - 1:
            trapezio = [pontoInicial, pontoMedio, pontoFinal, pontoFinal]
        else:
            trapezio = [pontoInicial, pontoInicial+self.largura_base_superior ,pontoFinal-self.largura_base_superior, pontoFinal]
        self.ponto_referencial += self.largura_base_inferior
        return fuzz.trapmf(self.eixo_x, trapezio)

    def calcularParticaoGaussiana(self):
        pontoMedio = self.ponto_referencial + self.largura_base_inferior
        self.ponto_referencial += self.largura_base_inferior
        return fuzz.gaussmf(self.eixo_x, pontoMedio, self.largura_base_inferior/len(self.tiposConjunto))

    def criarConjunto(self):
        for index, tipoConjunto in enumerate(self.tiposConjunto):
            if tipoConjunto == "TRI":
                self.conjuntos.append(self.calculaParticaoTriangular())
            elif tipoConjunto == "TRAP":
                self.conjuntos.append(self.calcularParticaoTrapezoidal(index))
            elif tipoConjunto == "GAUSS":
                self.conjuntos.append(self.calcularParticaoGaussiana())
        return self.conjuntos

    def plotParticao(self):
        for conjunto in self.conjuntos:
            plt.plot(self.eixo_x, conjunto)
        plt.show()

    def getPertinenciaConjuntos(self, x):
        conjuntoAtivado = -1
        pertinenciaMax = 0
        for index, conjunto in enumerate(self.conjuntos):
            pertinencia = fuzz.interp_membership(self.eixo_x, conjunto, x)
            if pertinenciaMax < pertinencia:
                conjuntoAtivado = index
                pertinenciaMax = pertinencia
        return conjuntoAtivado, pertinenciaMax

    def getPertinenciaIdConjunto(self, indexConjunto, x):
        pertinencia = fuzz.interp_membership(self.eixo_x, self.conjuntos[indexConjunto], x)
        return pertinencia


"""
tiposConjunto = ["TRAP", "TRI", "TRAP"]
n = 1000
part = Particao(0, 80, n, tiposConjunto)
part.criarConjunto()
part.plotParticao()
"""