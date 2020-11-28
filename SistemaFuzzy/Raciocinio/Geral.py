import numpy as np
import skfuzzy as fuzz
from Metricas import Objetivos as obj


def classificar(operador_Agregacao, conjuntos_de_entradas_fuzzy, particoes_entradas, regras, pesos, instancias, outputs):
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
            tnorma = np.prod(graus_pertinencias)*peso #mudar a composição com um if (min, max, prod)
            if tnorma > 0:
                classificacaoGeral[classe].append(tnorma)
        classe = getClasse(classificacaoGeral, operador_Agregacao)
        if classe == 0: classe = classeDefault
        resultados.append(classe)
    return obj.Objetivos().__getAcuraciaDatasetBalanceado__(resultados, gabarito)

def getClasse(classificacaoGeral, operador_Agregacao):
    maiorPertinencia = 0
    classe = 0
    for c in classificacaoGeral:
        if len(classificacaoGeral[c]) > 0:
            if str(operador_Agregacao).__eq__("MAX"):
                pertinencia = np.max(classificacaoGeral[c])
            elif str(operador_Agregacao).__eq__("MEAN"):
                pertinencia = np.mean(classificacaoGeral[c])
            else:
                pertinencia = np.max(classificacaoGeral[c])
            if pertinencia > maiorPertinencia:
                maiorPertinencia = pertinencia
                classe = c
    return classe


