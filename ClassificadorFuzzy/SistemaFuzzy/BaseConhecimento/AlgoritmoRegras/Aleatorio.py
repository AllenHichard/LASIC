import numpy as np
from ClassificadorFuzzy.Model import Regra
import random

class Aleatorio:

    def __init__(self, particoes, instancias, classes):
        self.particoes = particoes
        self.instancias = instancias
        self.regras = []
        self.tnormas = []
        self.classes = classes

    def aleatorio(self):
        for _ in self.instancias:
            antecedentes = []
            peso = 1
            for posicao_antecedente, particao in enumerate(self.particoes):
                antecedentes.append(random.randint(0, len(particao.conjuntos)-1))
            consequente = random.randint(0, len(self.classes)-1)
            tnorma = 1
            regra = Regra.Regra(antecedentes, consequente, 1, peso)
            self.atualizarRegras(tnorma, regra)
        return self.regras


    def atualizarRegras(self, tnorma, regra):
        if tnorma > 0:
            index, cond = self.inconsistencia(regra)
            if not cond:
                self.regras.append(regra)
                self.tnormas.append(tnorma)
            elif self.tnormas[index] < tnorma:
                self.regras[index] = regra
                self.tnormas[index] = tnorma

    def inconsistencia(self,novaRegra):
        for index, r in enumerate(self.regras):
            if r.__eq__(novaRegra):
                return index, True
        return -1, False

    def printRegras(self):
        for regra in self.regras:
            print(regra.__str__())