import numpy as np
import skfuzzy as fuzz
import matplotlib.pyplot as plt

class BaseDados:

    def __init__(self):
        self.conjuntos_de_entradas_fuzzy = []
        self.particoes_entradas = []

    def __getConjuntosFuzzy__(self):
        return self.conjuntos_de_entradas_fuzzy

    def __getParticoes__(self):
        return self.particoes_entradas

    def criarConjuntos(self, atributos):
        for atributo in atributos:
            (inicio, fim) = atributos[atributo]
            n = 1000  # varia entre 9999 e 10000
            eixo_x = np.arange(inicio, fim, (fim - inicio) / (n - 1))
            eixo_x[len(eixo_x) - 1] = fim
            centroide = (inicio+fim)/2
            #essa variavel armazena a quantidade que deve ser somada ao ponto inicial e definir o ponto médio do trapézio
            passos_centros = (fim-inicio)/4
            baixo = fuzz.trapmf(eixo_x, [inicio, inicio, inicio+passos_centros, centroide])
            medio = fuzz.trimf(eixo_x, [inicio+passos_centros, centroide, fim-passos_centros])
            alto = fuzz.trapmf(eixo_x, [centroide, fim-passos_centros, fim, fim])
            self.conjuntos_de_entradas_fuzzy.append([baixo, medio, alto])
            self.particoes_entradas.append(eixo_x)
            #plt.plot(eixo_x, baixo, 'b', linewidth=1.5, label='Bad')
            #plt.plot(eixo_x, medio, 'g', linewidth=1.5, label='Decent')
            #plt.plot(eixo_x, alto, 'r', linewidth=1.5, label='Great')
            #plt.show()