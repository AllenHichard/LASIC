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
        self.passos = (fim - inicio) / (len(tiposConjunto) + 1)
        self.ponto_referencial = inicio

    def calculaParticaoTriangular(self):
        print(self.ponto_referencial, self.passos)
        pontoMedio = self.ponto_referencial + self.passos
        conjunto = fuzz.trimf(self.eixo_x, [self.ponto_referencial,
                                            pontoMedio,
                                            self.ponto_referencial +self.passos * 2])
        self.ponto_referencial += self.passos
        return conjunto
    def calcularParticaoTrapezoidal(self, index):
        passoTrap = self.passos / 2
        pontoMedio = self.ponto_referencial + self.passos
        if index == 0:
            conjunto = fuzz.trapmf(self.eixo_x, [self.ponto_referencial,self.ponto_referencial,
                                                 pontoMedio,
                                                 self.ponto_referencial + self.passos * 2])
        elif index == len(self.tiposConjunto) - 1:
            conjunto = fuzz.trapmf(self.eixo_x, [self.ponto_referencial,
                                                 pontoMedio,
                                                 self.ponto_referencial + self.passos * 2,
                                                 self.ponto_referencial + self.passos * 2])
        else:
            conjunto =  fuzz.trapmf(self.eixo_x,[self.ponto_referencial,
                                                self.ponto_referencial + passoTrap,
                                                 self.ponto_referencial + passoTrap * 3,
                                                self.ponto_referencial + self.passos * 2])
        self.ponto_referencial += self.passos
        return conjunto

    def calcularParticaoGaussiana(self):
        pontoMedio = self.ponto_referencial + self.passos
        conjunto =  fuzz.gaussmf(self.eixo_x, pontoMedio, self.passos/len(self.tiposConjunto))
        self.ponto_referencial += self.passos
        return conjunto

    def criarConjunto(self):
        for index, tipoConjunto in enumerate(self.tiposConjunto):
            if tipoConjunto == "TRI":
                conjuntoAtual = self.calculaParticaoTriangular()
                self.conjuntos.append(conjuntoAtual)
                plt.plot(self.eixo_x, conjuntoAtual)
            elif tipoConjunto == "TRAP":
                conjuntoAtual = self.calcularParticaoTrapezoidal(index)
                self.conjuntos.append(conjuntoAtual)
                plt.plot(self.eixo_x, conjuntoAtual)
            elif tipoConjunto == "GAUSS":
                conjuntoAtual = self.calcularParticaoGaussiana()
                self.conjuntos.append(conjuntoAtual)
                plt.plot(self.eixo_x, conjuntoAtual)
            #self.particoes_entradas.append(eixo_x)

        plt.show()

tiposConjunto = ["TRAP", "TRI", "TRAP"]

n = 1000
part = Particao(0, 100, n, tiposConjunto)
part.criarConjunto()
