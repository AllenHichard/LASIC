import numpy as np
from SistemaFuzzy.Model import Regra


class Reducao:

    def __init__(self, regras, instancias, particoes):
        self.regrasComRuido = regras
        self.regras_para_classificacao = []
        self.instancias = instancias
        self.particoes = particoes
        self.regras = []
        self.tnormas = []

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
        self.preencher_regra_nula()

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


regra1 = Regra.Regra([1, 1, 1, 1], 1, 0.5)
regra2 = Regra.Regra([1, 1, 1, 2], 1, 0.7)
regra3 = Regra.Regra([1, 1, 1, 2], 2, 0.5)
regra4 = Regra.Regra([1, 1, 1, 3], 3, 0.5)

regras = [regra1,regra2,regra3,regra4]
semDuplicidade = []
for regra in regras:
    if not regra in semDuplicidade:
        semDuplicidade.append(regra)
semAmbiguidade = []
comAmbiguidade = []
for regra in semDuplicidade:
    encontrou = False
    for sa in semAmbiguidade:
        if regra.eq_antecedentes(sa):
            semAmbiguidade.remove(sa)
            comAmbiguidade.append(sa)
            comAmbiguidade.append(regra)
            encontrou = True
    if not encontrou:
        semAmbiguidade.append(regra)

"""
print("Sem Ambiguidade")
for regra in semAmbiguidade:
    print(regra.__str__())

print("Com Ambiguidade")
for regra in comAmbiguidade:
    print(regra.__str__())

regrasTratadas = semAmbiguidade"""



