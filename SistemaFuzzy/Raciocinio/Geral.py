import numpy as np
import skfuzzy as fuzz



def classificar(conjuntos_de_entradas_fuzzy, particoes_entradas, regras, instancias, outputs):
    classificacaoGeral = {}
    for output in outputs:
        classificacaoGeral[outputs[output]] = []
    print(classificacaoGeral)
    acertos = 0
    for instancia in instancias:
        atributos = instancia.__getAtributos__()
        gabarito = instancia.__getClasse__()
        for regra in regras:
            graus_pertinencias = []
            for i, valor in enumerate(atributos):
                nível_ativado = regra[i]-1
                grau = fuzz.interp_membership(particoes_entradas[i], conjuntos_de_entradas_fuzzy[i][nível_ativado], valor)
                graus_pertinencias.append(grau)
            tnorma = np.prod(graus_pertinencias) #mudar a composição com um if (min, max, prod)
            if  tnorma > 0:
                classe = regra[len(regra)-1]
                classificacaoGeral[classe].append(tnorma)
        classe = getClasse(classificacaoGeral)
        if classe == gabarito:
            acertos +=1
    acuracia = acertos/len(instancias)
    return acuracia

def getClasse(classificacaoGeral):
    maiorPertinencia = 0
    classe = 0
    for c in classificacaoGeral:
        if len(classificacaoGeral[c]) > 0:
            MedArit = np.mean(classificacaoGeral[c])
            if  MedArit > maiorPertinencia:
                maiorPertinencia = MedArit
                classe = c
    return classe
