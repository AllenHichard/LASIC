import numpy as np
import skfuzzy as fuzz
from Metricas import Objetivos as obj


def classificar(operador_Agregacao, operador_Composicao, conjuntos_de_entradas_fuzzy, particoes_entradas, regras, pesos, instancias, outputs):
    resultados = []
    gabarito = []
    ocorrencias = {}
    for output in outputs:
        ocorrencias[outputs[output]] = 0
    for classeRegra in regras[1]:
        ocorrencias[classeRegra]+=1
    classeDefault = sorted(ocorrencias, key=ocorrencias.get, reverse=False)[0]
    for instancia in instancias:
        classificacaoGeral = {}
        for output in outputs:
            classificacaoGeral[outputs[output]] = []
        atributos = instancia.__getAtributos__()
        gabarito.append(instancia.__getClasse__())
        #print(len(regras[0]), len(regras[1]), len(pesos))
        for antecedentes, classe, peso in zip(regras[0], regras[1], pesos):
            #print(antecedentes, classe)
            graus_pertinencias = []
            for i, valor in enumerate(atributos):
                nível_ativado = antecedentes[i]-1
                grau = fuzz.interp_membership(particoes_entradas[i], conjuntos_de_entradas_fuzzy[i][nível_ativado], valor)
                graus_pertinencias.append(grau)
            tnorma = composicao(graus_pertinencias, peso, operador_Composicao)
            if tnorma > 0:
                classificacaoGeral[classe].append(tnorma)
        classe = getClasse(classificacaoGeral, operador_Agregacao)
        if classe == 0: classe = classeDefault
        resultados.append(classe)
    return obj.Objetivos().__getAcuraciaDatasetBalanceado__(resultados, gabarito)

def composicao(graus_pertinencias, peso, operador_Composicao):
    if str(operador_Composicao).__eq__("MIN"):
        return np.min(graus_pertinencias) * peso
    else:
        return np.prod(graus_pertinencias)*peso
    #mudar a composição com um if (min, max, prod)

def getClasse(classificacaoGeral, operador_Agregacao):
    maiorPertinencia = 0
    classe = 0
    for c in classificacaoGeral:
        if len(classificacaoGeral[c]) > 0:
            if str(operador_Agregacao).__eq__("MEAN"):
                pertinencia = np.mean(classificacaoGeral[c])
            else:
                pertinencia = np.max(classificacaoGeral[c])
            if pertinencia > maiorPertinencia:
                maiorPertinencia = pertinencia
                classe = c
    return classe


def calculaPesos(self, conjuntos_de_entradas_fuzzy, particoes_entradas, instancias, outputs):
    for antecedentes in self.regras[0]:
        classificacaoGeral = {}
        for output in outputs:
            classificacaoGeral[outputs[output]] = []
        for instancia in instancias:
            graus_pertinencias = []
            atributos = instancia.__getAtributos__()
            classe = instancia.__getClasse__()
            for i, valor in enumerate(atributos):
                nível_ativado = antecedentes[i] - 1
                grau = fuzz.interp_membership(particoes_entradas[i],
                                              conjuntos_de_entradas_fuzzy[i][nível_ativado],
                                              valor)
                graus_pertinencias.append(grau)
            compatibilidade = np.prod(graus_pertinencias)  # operador produto #u1*u2*.....*un
            classificacaoGeral[classe].append(compatibilidade)
        lista_bg = []
        for classe in classificacaoGeral:
            bg = np.sum(classificacaoGeral[classe])
            lista_bg.append(bg)
        Bgx = np.max(lista_bg)
        M = len(lista_bg)
        lista_bg.remove(Bgx)
        betha = np.sum(lista_bg) / (M-1)
        numerador = abs(Bgx - betha)
        denonimador = np.sum(lista_bg) + Bgx
        CF = numerador/denonimador
        self.pesos.append(CF)
    #print(len(self.regras), len(self.pesos))
    #print(self.pesos)
    return self.pesos

