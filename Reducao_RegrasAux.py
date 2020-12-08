import numpy as np
import skfuzzy as fuzz
from ClassificadorFuzzy.Model import Regra

class Reducao:

    def __init__(self, regras, instancias, particoes):
        self.regrasComRuido = regras
        self.regrasSemRuido = []
        self.instancias = instancias
        self.particoes = particoes
        self.regras = []

    def reduzir(self):
        for instancia in self.instancias:
            caracteristicas = instancia.caracteristicas
            classe = instancia.classe
            for regraAtual in self.regrasComRuido:
                antecedentes_regras = regraAtual.antecedentes
                consequente = regraAtual.consequente
                pertinencias_maximas = []
                for id_antecedente, caracteristica, particao in zip(antecedentes_regras, caracteristicas, self.particoes):
                    #print(id_antecedente, caracteristicas, particao)
                    pertinencia = particao.getPertinenciaIdConjunto(id_antecedente, caracteristica)
                    pertinencias_maximas.append(pertinencia)
                tnorma = np.prod(pertinencias_maximas)
                self.atualizarRegras(tnorma, regraAtual)
        #self.preencher_regra_nula()

        #print("1 - ", len(self.regrasComRuido))
        #print("2 - ", len(self.regras))
        #print("3 - ", len(self.regrasSemRuido))
        #for regra in self.regrasSemRuido:
        #    print(regra)
        #a = 2 + "2"
        return self.regrasSemRuido

    def preencher_regra_nula(self):
        for regra in self.regrasComRuido:
            regraNula = Regra.Regra([-1] * len(regra.antecedentes), -1, 1, 1)
            self.regrasSemRuido.append(regraNula)
        for posicao, regra in enumerate(self.regrasComRuido):
            if regra in self.regras:
                self.regrasSemRuido[posicao] = regra



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