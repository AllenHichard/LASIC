import numpy as np
import skfuzzy as fuzz



def classificar(conjuntos_de_entradas_fuzzy, particoes_entradas, regras, instancias):
    acertos = 0
    for instancia in instancias:
        atributos = instancia.__getAtributos__()
        gabarito = instancia.__getClasse__()
        classe = 0
        maiorPertinencia = 0
        for regra in regras:
            graus_pertinencias = []
            for i, valor in enumerate(atributos):
                nível_ativado = regra[i]-1
                grau = fuzz.interp_membership(particoes_entradas[i], conjuntos_de_entradas_fuzzy[i][nível_ativado], valor)
                graus_pertinencias.append(grau)
            tnorma = np.prod(graus_pertinencias) #mudar a composição com um if (min, max, prod)
            if  tnorma > maiorPertinencia:
                maiorPertinencia = tnorma
                classe = regra[len(regra)-1]
        #print(classe, gabarito)
        if classe == gabarito:
            acertos +=1
        else:
            pass
            #print("Classificou como: ", classe, "| Era pra ser: ", gabarito)
    acuracia = acertos/len(instancias)
    return acuracia

"""
# Generate universe variables
#   * Quality and service on subjective ranges [0, 10]
#   * Tip has a range of [0, 25] in units of percentage points
instancia = [5.1, 3.5, 1.4, 0.2, "Iris-setosa"]

atributos = {'SepalLength': [4.3, 7.9],
            'SepalWidth': [2.0, 4.4],
            'PetalLength': [1.0, 6.9],
            'PetalWidth': [0.1, 2.5]}

Saída = {'Iris-setosa': 0,
         'Iris-versicolor': 1,
         'Iris-virginica': 2}
"""

