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
        self.largura_base_superior = (fim - inicio) / (2 * len(tiposConjunto) - 1)

        self.largura_entre_pontos_inferiores = (fim - inicio) / (len(tiposConjunto) - 1)

        self.ponto_referencial = inicio
        self.pontosIniciais = []
        self.pontosFinais = []
        self.limiteSuperior = []
        self.pontosCentrais = []
        self.limiteInferior = []

    def setPontosCentrais(self, novosPontosCentrais):
        iteracaoPontos = 0
        tam = len(self.tiposConjunto) - 1
        # print(self.tiposConjunto)
        # print(self.pontosIniciais)
        # print(self.pontosFinais)
        index = 1
        while index < tam:
            tipoConjunto = self.tiposConjunto[index]
            if tipoConjunto == "TRI":
                pontoInicial = self.pontosIniciais[iteracaoPontos]
                pontoFinal = self.pontosFinais[iteracaoPontos]
                self.conjuntos[index] = fuzz.trimf(self.eixo_x,
                                                   [pontoInicial, novosPontosCentrais[iteracaoPontos], pontoFinal])
                iteracaoPontos += 1
            elif tipoConjunto == "TRAP":
                pontoInicial = self.pontosIniciais[iteracaoPontos]
                p1 = novosPontosCentrais[iteracaoPontos]
                p2 = novosPontosCentrais[iteracaoPontos + 1]
                pontoFinal = self.pontosFinais[iteracaoPontos + 1]
                # print(pontoInicial, p1, p2, pontoFinal)
                self.conjuntos[index] = fuzz.trapmf(self.eixo_x, [pontoInicial, p1, p2, pontoFinal])
                iteracaoPontos += 2
                """
                self.pontosIniciais.append(pontoInicial)
                self.pontosCentrais.append(p1)
                self.pontosFinais.append(p2)

                self.pontosIniciais.append(p1)
                self.pontosCentrais.append(p2)
                self.pontosFinais.append(pontoFinal)
                """
            elif tipoConjunto == "GAUSS":
                desvio = self.largura_entre_pontos_inferiores / len(self.tiposConjunto)
                self.conjuntos[index] = fuzz.gaussmf(self.eixo_x, novosPontosCentrais[iteracaoPontos], desvio)
                iteracaoPontos += 1
            index += 1
        self.plotParticao()

    def calculaParticaoTriangular(self, index):
        pontoInicial = self.ponto_referencial
        pontoMedio = self.ponto_referencial + self.largura_entre_pontos_inferiores
        pontoFinal = self.ponto_referencial + self.largura_entre_pontos_inferiores * 2
        if index == 0:
            triangulo = [self.inicio, self.inicio, pontoMedio]
            self.pontosCentrais.append(pontoInicial)
        elif index == len(self.tiposConjunto) - 1:
            self.pontosCentrais.append(self.fim)
            triangulo = [pontoInicial, self.fim, self.fim]
        else:
            self.pontosIniciais.append(pontoInicial)
            self.pontosFinais.append(pontoFinal)
            self.pontosCentrais.append(pontoMedio)
            triangulo = [pontoInicial, pontoMedio, pontoFinal]
            self.ponto_referencial += self.largura_entre_pontos_inferiores
        return fuzz.trimf(self.eixo_x, triangulo)

    def calcularParticaoTrapezoidal(self, index):
        pontoInicial = self.ponto_referencial
        pontoMedio = self.ponto_referencial + self.largura_entre_pontos_inferiores
        pontoFinal = self.ponto_referencial + self.largura_entre_pontos_inferiores * 2
        if index == 0:
            p1 = self.inicio
            p2 = self.inicio+self.largura_base_superior/2
            self.pontosCentrais.append(p2)
            trapezio = [self.inicio, p1, p2, pontoMedio]
        elif index == len(self.tiposConjunto) - 1:
            p1 = self.fim - self.largura_base_superior/2
            p2 = self.fim
            self.pontosCentrais.append(p1)
            trapezio = [pontoInicial, p1, p2, self.fim]
        else:
            p1 = pontoMedio - self.largura_base_superior/2
            p2 = pontoMedio + self.largura_base_superior/2
            self.pontosIniciais.append(pontoInicial)
            self.pontosCentrais.append(p1)
            self.pontosFinais.append(p2)

            self.pontosIniciais.append(p1)
            self.pontosCentrais.append(p2)
            self.pontosFinais.append(pontoFinal)

            #print(pontoInicial, p1, p2, pontoFinal)
            trapezio = [pontoInicial, p1, p2, pontoFinal]
            self.ponto_referencial += self.largura_entre_pontos_inferiores
        return fuzz.trapmf(self.eixo_x, trapezio)

    def calcularParticaoGaussiana(self, index):
        pontoMedio = self.ponto_referencial + self.largura_entre_pontos_inferiores
        desvio = self.largura_entre_pontos_inferiores / 3.5
        if index == 0:
            self.pontosCentrais.append(self.inicio)
            return fuzz.gauss2mf(self.eixo_x, self.inicio, 0.1, self.inicio, desvio)
        elif index == len(self.tiposConjunto) - 1:
            self.pontosCentrais.append(self.fim)
            return fuzz.gauss2mf(self.eixo_x, self.fim, desvio, self.fim, 0.1)
        else:
            self.pontosCentrais.append(pontoMedio)
            self.pontosIniciais.append("GAUSS")
            self.pontosFinais.append("GAUSS")
            self.ponto_referencial += self.largura_entre_pontos_inferiores
            #return fuzz.gauss2mf(self.eixo_x, pontoMedio, desvio * 2, self.fim,  0.1)

            return fuzz.gaussmf(self.eixo_x, pontoMedio, desvio)

    def criarConjunto(self):
        for index, tipoConjunto in enumerate(self.tiposConjunto):
            if tipoConjunto == "TRI":
                self.conjuntos.append(self.calculaParticaoTriangular(index))
            elif tipoConjunto == "TRAP":
                self.conjuntos.append(self.calcularParticaoTrapezoidal(index))
            elif tipoConjunto == "GAUSS":
                self.conjuntos.append(self.calcularParticaoGaussiana(index))
        self.calculoLimites()
        self.plotParticao()
        return self.conjuntos

    def calculoLimites(self):
        for index in range(1, len(self.pontosCentrais) - 1):
            PI = self.pontosCentrais[index - 1]
            pontoMedio = self.pontosCentrais[index]
            PS = self.pontosCentrais[index + 1]
            self.limiteInferior.append(self.lower_centroids(PI, pontoMedio))
            self.limiteSuperior.append(self.upper_centroid(PS, pontoMedio))
        self.pontosCentrais = self.pontosCentrais[1:len(self.pontosCentrais) - 1]

    def lower_centroids(self, inicio, pontoMedio):
        PI = inicio
        PM = pontoMedio
        vi = PM - ((PM - PI) / 2)
        return vi

    def upper_centroid(self, fim, pontoMedio):
        PS = fim
        PM = pontoMedio
        vs = PM + ((PS - PM) / 2)
        return vs

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
        # print(len(self.conjuntos), indexConjunto)
        pertinencia = fuzz.interp_membership(self.eixo_x, self.conjuntos[indexConjunto], x)
        return pertinencia


"""
tiposConjunto = ["TRAP", "TRI", "TRAP"]
n = 1000
part = Particao(0, 80, n, tiposConjunto)
part.criarConjunto()
part.plotParticao()
"""