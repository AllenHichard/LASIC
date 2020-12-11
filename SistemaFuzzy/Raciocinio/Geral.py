import numpy as np
import skfuzzy as fuzz
from Metricas import Objetivos as obj

class Classificacao:

    def __init__(self, particoes, regras, instancias, classes):
        self.particoes = particoes
        self.classes = classes
        self.regras = regras
        self.instancias = instancias
        self.gabarito = []
        self.resultado = []

    def classeDefaut(self):
        ocorrencias = []
        for _ in self.classes:
            ocorrencias.append(0)
        for regra in self.regras:
            posicao = regra.consequente
            ocorrencias[posicao] += 1
        classeDefault = ocorrencias.index(np.min(ocorrencias))
        return classeDefault

    def classificar(self):
        dontcare = -1
        classeDefault = self.classeDefaut()
        for instancia in self.instancias:
            tnorma_classe = []
            self.gabarito.append(instancia.classe)
            for _ in self.classes: tnorma_classe.append([])
            caracteristicas = instancia.caracteristicas
            for regra in self.regras:
                pertinencias_maximas = []
                antecedentes_regras = regra.antecedentes
                for id_antecedente, caracteristica, particao in zip(antecedentes_regras, caracteristicas, self.particoes):
                    if not dontcare == id_antecedente:
                        pertinencia = particao.getPertinenciaIdConjunto(id_antecedente,caracteristica)
                        pertinencias_maximas.append(pertinencia)
                tnorma = self.composicao(pertinencias_maximas, regra, "PROD")
                self.tnormas_por_classe(tnorma, regra.consequente, tnorma_classe)

            classe = self.agregacao_get_classe(tnorma_classe, "MAX")
            if classe == -1: classe = classeDefault
            self.resultado.append(classe)
        objetivos = obj.Objetivos()
        objetivos.ACC(self.resultado, self.gabarito)
        objetivos.interpretabilidadeRegra(self.regras, self.instancias)
        return objetivos.acc, objetivos.interpretabilidadeRegras

    def tnormas_por_classe(self, tnorma, classe_ativada, tnorma_classe):
        if tnorma > 0:
            tnorma_classe[classe_ativada].append(tnorma)

    def composicao(self, graus_pertinencias, regra, operador_Composicao):
        if str(operador_Composicao).__eq__("MIN"):
            return np.min(graus_pertinencias) * regra.peso
        else:
            return np.prod(graus_pertinencias)* regra.peso
        #mudar a composição com um if (min, max, prod)

    def agregacao_get_classe(self, classificacaoGeral, operador_Agregacao):
        maiorPertinencia = 0
        classe = -1
        for c, lista_por_classe in enumerate(classificacaoGeral):
            if len(lista_por_classe) > 0:
                if str(operador_Agregacao).__eq__("MEAN"):
                    pertinencia = np.mean(lista_por_classe)
                else:
                    pertinencia = np.max(lista_por_classe)
                if pertinencia > maiorPertinencia:
                    maiorPertinencia = pertinencia
                    classe = c
        return classe


"""
ocorrencias = {}
    for output in outputs:
        ocorrencias[outputs[output]] = 0
    for classeRegra in regras[1]:
        ocorrencias[classeRegra]+=1
    classeDefault = sorted(ocorrencias, key=ocorrencias.get, reverse=False)[0]
"""