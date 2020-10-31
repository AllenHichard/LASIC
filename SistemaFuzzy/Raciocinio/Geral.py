import numpy as np
import skfuzzy as fuzz


def classificar(operador_Agregacao, conjuntos_de_entradas_fuzzy, particoes_entradas, regras, pesos, instancias, outputs):
    ocorrencias = {}
    for output in outputs:
        ocorrencias[outputs[output]] = 0
    for regra in regras:
        classeRegra = regra[len(regra) - 1]
        ocorrencias[classeRegra]+=1
    classeDefault = sorted(ocorrencias, key=ocorrencias.get, reverse=False)[0]
    acertos = 0
    for instancia in instancias:
        classificacaoGeral = {}
        for output in outputs:
            classificacaoGeral[outputs[output]] = []
        atributos = instancia.__getAtributos__()
        gabarito = instancia.__getClasse__()
        for regra, peso in zip(regras, pesos):
            graus_pertinencias = []
            for i, valor in enumerate(atributos):
                nível_ativado = regra[i]-1
                grau = fuzz.interp_membership(particoes_entradas[i], conjuntos_de_entradas_fuzzy[i][nível_ativado], valor)
                graus_pertinencias.append(grau)
            tnorma = np.prod(graus_pertinencias)*peso #mudar a composição com um if (min, max, prod)
            if tnorma > 0:
                classe = regra[len(regra) - 1]
                classificacaoGeral[classe].append(tnorma)
        classe = getClasse(classificacaoGeral, operador_Agregacao)
        if classe == gabarito:
                acertos += 1
        else:
            if classe == 0 and gabarito == classeDefault:
                acertos += 1
                classe = classeDefault
            #print("Classificou como: ", classe, "| Era pra ser: ", gabarito)
    acuracia = acertos / len(instancias)
    return acuracia

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


