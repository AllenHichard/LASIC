import numpy as np
from ClassificadorFuzzy.Model import Regra

class WangMendel:

    def __init__(self, particoes, instancias):
        self.particoes = particoes
        self.instancias = instancias
        self.regras = []

    def wangMendel(self):
        for instancia in self.instancias:
            antecedentes = []
            consequente = instancia.classe
            pertinencias_maximas = []
            for atributo, particao in zip(instancia.caracteristicas, self.particoes):
                conjuntoAtivado, pertinenciaMax = particao.getPertinenciaConjuntos(atributo)
                antecedentes.append(conjuntoAtivado)
                pertinencias_maximas.append(pertinenciaMax)
            tnorma = np.prod(pertinencias_maximas)
            regra = Regra.Regra(antecedentes, consequente, tnorma)
            self.atualizarRegras(regra)
        return self.regras

    def atualizarRegras(self, regra):
        if regra.tnorma > 0:
            index, cond = self.inconsistencia(regra)
            if not cond:
                self.regras.append(regra)
            elif self.regras[index].tnorma < regra.tnorma:
                self.regras[index] = regra

    def inconsistencia(self,novaRegra):
        for index, r in enumerate(self.regras):
            if r.eq_antecedentes(novaRegra):
                return index, True
        return -1, False

    def printRegras(self):
        for regra in self.regras:
            print(regra.__str__())