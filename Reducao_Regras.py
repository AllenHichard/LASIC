import numpy as np
import skfuzzy as fuzz
from ClassificadorFuzzy.Model import Regra

class Reducao:

    def __init__(self, regras, instancias, particoes):
        self.regrasComRuido = regras
        self.instancias = instancias
        self.particoes = particoes
        self.regras = []
        self.tnormas = []

    def reduzir(self):
        #print("1 - ", len(self.regrasComRuido))
        for instancia in self.instancias:
            caracteristicas = instancia.caracteristicas
            classe = instancia.classe
            for regraAtual in self.regrasComRuido:
                #print(regraAtual.__str__())
                antecedentes_regras = regraAtual.antecedentes
                consequente = regraAtual.consequente
                pertinencias_maximas = []
                for id_antecedente, caracteristica, particao in zip(antecedentes_regras, caracteristicas, self.particoes):
                    #print(id_antecedente, caracteristicas, particao)
                    pertinencia = particao.getPertinenciaIdConjunto(id_antecedente, caracteristica)
                    pertinencias_maximas.append(pertinencia)
                tnorma = np.prod(pertinencias_maximas)
                self.atualizarRegras(tnorma, regraAtual)
        #print("2 - ", len(self.regras))
        return self.regras


    def atualizarRegras(self, tnorma, regraAtual):
        if tnorma > 0:
            index, cond = self.inconsistencia(regraAtual)
            if not cond:
                self.regras.append(regraAtual)
                self.tnormas.append(tnorma)
            elif self.tnormas[index] < tnorma:
                self.regras[index] = regraAtual
                self.tnormas[index] = tnorma

    def inconsistencia(self, novaRegra):
        for index, r in enumerate(self.regras):
            if r.__eq__(novaRegra):
                return index, True
        return -1, False