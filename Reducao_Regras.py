import numpy as np
import skfuzzy as fuzz
from ClassificadorFuzzy.Model import Regra

class Reducao:

    def __init__(self, regras, instancias, particoes):
        self.regrasComRuido = regras.copy()
        self.instancias = instancias
        self.particoes = particoes
        self.regras = []

    def reduzir(self):
        dontcare = -1
        for instancia in self.instancias:
            caracteristicas = instancia.caracteristicas
            classe = instancia.classe
            for regraAtual in self.regrasComRuido:
                antecedentes_regras = regraAtual.antecedentes
                consequente = regraAtual.consequente
                pertinencias_maximas = []
                if not antecedentes_regras == [-1]*len(antecedentes_regras):
                    for id_antecedente, caracteristica, particao in zip(antecedentes_regras, caracteristicas, self.particoes):
                        #print(id_antecedente, caracteristicas, particao)
                        if not dontcare == id_antecedente:
                            pertinencia = particao.getPertinenciaIdConjunto(id_antecedente, caracteristica)
                            pertinencias_maximas.append(pertinencia)
                    tnorma = np.prod(pertinencias_maximas)
                    regraAtual.tnorma = tnorma
                    self.atualizarRegras(regraAtual)

        #print("como veio", len(self.regrasComRuido))
        #for regra in self.regrasComRuido:
        #    print(regra.__str__())
        #print("como vai", len(self.regras))
        #for regra in self.regras:
        #    print(regra.__str__())
        #a = '1' + 2
        return self.regras

    def atualizarRegras(self, regra):
        if regra.tnorma > 0:
            index, cond = self.inconsistencia(regra)
            if not cond:
                self.regras.append(regra)
            elif self.regras[index].tnorma < regra.tnorma:
                self.regras[index] = regra

    def inconsistencia(self, novaRegra):
        for index, r in enumerate(self.regras):
            if r.eq_antecedentes(novaRegra):
                return index, True
        return -1, False