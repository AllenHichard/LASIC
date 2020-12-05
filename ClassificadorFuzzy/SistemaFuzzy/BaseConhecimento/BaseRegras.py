import numpy as np
import skfuzzy as fuzz
from ClassificadorFuzzy.Model import Regra
from ClassificadorFuzzy.SistemaFuzzy.BaseConhecimento.BaseDados import BaseDados as bd

class BaseRegras:

    def __init__(self, particoes, instancias):
        self.particoes = particoes
        self.instancias = instancias
        self.regras = []
        self.tnormas = []

    def wangMendel(self):
        for instancia in self.instancias:
            antecedentes = []
            consequente = instancia.classe
            pertinencias_maximas = []
            peso = 1
            for atributo, particao in zip(instancia.caracteristicas, self.particoes):
                conjuntoAtivado, pertinenciaMax = particao.getPertinenciaConjuntos(atributo)
                antecedentes.append(conjuntoAtivado)
                pertinencias_maximas.append(pertinenciaMax)
            tnorma = np.prod(pertinencias_maximas)
            regra = Regra.Regra(antecedentes, consequente, tnorma, peso)
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

"""
mudou a entrada para instâncias
BaseDados = bd.BaseDados([0,100], [100, 200], [1000,1000], [["TRAP", "TRI", "TRAP"],["TRAP", "TRI", "TRAP"]])
particoes = BaseDados.criarParticoes()
entradas = [[0,140],[0,168], [0,189]]
saidas = [1,2,1]
br = BaseRegras(particoes, entradas, saidas)
br.wangMendel()
print("BaseRegras")
br.printRegras()
"""