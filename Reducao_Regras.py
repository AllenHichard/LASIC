import numpy as np
import skfuzzy as fuzz

def reduzir(conjuntos_de_entradas_fuzzy, particoes_entradas, regras, pesos, instancias):
    selfRegras = [[],[]]
    pertinenciaRegras = []
    for instancia in instancias:
        atributos = instancia.__getAtributos__()
        gabarito = instancia.__getClasse__()
        for antecedentes, classe, peso in zip(regras[0], regras[1], pesos):
            graus_pertinencias = []
            for i, valor in enumerate(atributos):
                nível_ativado = antecedentes[i]-1
                grau = fuzz.interp_membership(particoes_entradas[i], conjuntos_de_entradas_fuzzy[i][nível_ativado], valor)
                graus_pertinencias.append(grau)
            tnorma = np.prod(graus_pertinencias)*peso #mudar a composição com um if (min, max, prod)
            (cond, index) = inconsistencia(selfRegras, antecedentes)
            if cond:
                selfRegras[0].append(antecedentes)
                selfRegras[1].append(classe)
                pertinenciaRegras.append(tnorma)
            elif pertinenciaRegras[index] < tnorma:
                selfRegras[0].__setitem__(index, antecedentes)
                selfRegras[1].__setitem__(index, classe)
                pertinenciaRegras.__setitem__(index, tnorma)
    #print(len(selfRegras[0]), len(selfRegras[1]))
    return selfRegras[0], selfRegras[1] #antecedente, consequente

def inconsistencia(regras, antecedentes):
    for i, r_ant in enumerate(regras[0]): # lista de antecedentes das regras
        if r_ant == antecedentes:
            #return True, -1
            return False, i  # calcula t norma
    return True, -1