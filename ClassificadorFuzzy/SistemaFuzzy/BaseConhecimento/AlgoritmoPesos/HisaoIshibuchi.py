import numpy as np

class PesoHisao:

    def __init__(self, particoes, regras, instancias, classes):
        self.particoes = particoes
        self.classes = classes
        self.regras = regras
        self.instancias = instancias
        self.pesos = []


    def getPesos(self, temPesos):
        if temPesos:
            return self.calculaPesos()
        else:
            return [1] * len(self.regras)

    def calculaPesos(self):
        for regra in self.regras:
            classificacaoGeral = []
            antecedentes_regras = regra.antecedentes
            for _ in self.classes: classificacaoGeral.append([])
            for instancia in self.instancias:
                pertinencias_maximas = []
                caracteristicas = instancia.caracteristicas
                classe = instancia.classe
                for id_antecedente, caracteristica, particao in zip(antecedentes_regras, caracteristicas,
                                                                    self.particoes):
                    pertinencia = particao.getPertinenciaIdConjunto(id_antecedente, caracteristica)
                    pertinencias_maximas.append(pertinencia)
                compatibilidade = np.prod(pertinencias_maximas)  # operador produto #u1*u2*.....*un
                classificacaoGeral[classe].append(compatibilidade)
            lista_bg = []
            for indexClasse, classe in enumerate(classificacaoGeral):
                bg = np.sum(classificacaoGeral[indexClasse])
                lista_bg.append(bg)
            Bgx = np.max(lista_bg)
            M = len(lista_bg)
            lista_bg.remove(Bgx)
            betha = np.sum(lista_bg) / (M - 1)
            numerador = abs(Bgx - betha)
            denonimador = np.sum(lista_bg) + Bgx
            CF = numerador / denonimador
            self.pesos.append(CF)
        # print(len(self.regras), len(self.pesos))
        # print(self.pesos)
        return self.pesos

