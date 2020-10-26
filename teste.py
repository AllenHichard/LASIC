import numpy as np
import skfuzzy as fuzz
import matplotlib.pyplot as plt

# Generate universe variables
#   * Quality and service on subjective ranges [0, 10]
#   * Tip has a range of [0, 25] in units of percentage points
"""
instancia = [5.1, 3.5, 1.4, 0.2, "Iris-setosa"]

atributos = {'SepalLength': [4.3, 7.9],
            'SepalWidth': [2.0, 4.4],
            'PetalLength': [1.0, 6.9],
            'PetalWidth': [0.1, 2.5]}

Saída = {'Iris-setosa': 0,
         'Iris-versicolor': 1,
         'Iris-virginica': 2}
"""


conjuntos_de_entradas_fuzzy = []
particoes_entradas = []
t_norma_das_regras = []
valores_linguisticos = {0: "baixo",1: "medio", 2: "alto"}

def criarConjuntos(atributos):
    for atributo in atributos:
        (inicio, fim) = atributos[atributo]
        fim = fim+0.1
        eixo_x = np.arange(inicio, fim, (fim - inicio) / 100)
        centroide = (inicio+fim)/2
        #essa variavel armazena a quantidade que deve ser somada ao ponto inicial e definir o ponto médio do trapézio
        passos_centros = (fim-inicio)/4
        baixo = fuzz.trapmf(eixo_x, [inicio, inicio, inicio+passos_centros, centroide])
        medio = fuzz.trimf(eixo_x, [inicio+passos_centros, centroide, fim-passos_centros])
        alto = fuzz.trapmf(eixo_x, [centroide, fim-passos_centros, fim, fim])
        conjuntos_de_entradas_fuzzy.append([baixo, medio, alto])
        particoes_entradas.append(eixo_x)

def criarRegrasWangMendel(instancias):
    regras = []
    for instancia in instancias:
        regra = []
        lista_maiores_pertinencias = []
        for conjuntos, particao, valor in zip(conjuntos_de_entradas_fuzzy, particoes_entradas, instancia):
            nivel_baixo = fuzz.interp_membership(particao, conjuntos[0], valor)
            nivel_medio = fuzz.interp_membership(particao, conjuntos[1], valor)
            nivel_alto = fuzz.interp_membership(particao, conjuntos[2], valor)
            pertinencias = [nivel_baixo, nivel_medio, nivel_alto]
            regra.append(valores_linguisticos[pertinencias.index(max(pertinencias))])
            lista_maiores_pertinencias.append(max(pertinencias))
        regra.append(instancia.__getitem__(len(instancia)-1))
        #print(sum(lista_maiores_pertinencias))
        #print(regra[:4])
        (cond, index) = inconsistencia(regras, regra)
        tnorma = sum(lista_maiores_pertinencias)
        if cond:
            regras.append(regra)
            t_norma_das_regras.append(tnorma)  # tnorma soma
        elif t_norma_das_regras[index] < tnorma:
            regras.__setitem__(index, regra)
            t_norma_das_regras.__setitem__(index, tnorma)

    for i, t in zip(regras, t_norma_das_regras):
        print(i, t)
    print(len(regras))
    return regras

def inconsistencia(regras, regra):
    for i, r in enumerate(regras):
        if r[:4] == regra[:4]:
            return False, i # calcula t norma
    return True, -1

"""    

qual_level_lo = fuzz.interp_membership(particao_entrada, baixo, atri)
qual_level_md = fuzz.interp_membership(particao_entrada, medio, atri)
qual_level_hi = fuzz.interp_membership(particao_entrada, alto, atri)
print(qual_level_lo, qual_level_md, qual_level_hi)


# Generate fuzzy membership functions
qual_lo = fuzz.trimf(x_qual, [0, 0, 5])
qual_md = fuzz.trimf(x_qual, [0, 5, 10])
qual_hi = fuzz.trimf(x_qual, [5, 10, 10])

serv_lo = fuzz.trimf(x_serv, [0, 0, 5])
serv_md = fuzz.trimf(x_serv, [0, 5, 10])
serv_hi = fuzz.trimf(x_serv, [5, 10, 10])

tip_lo = fuzz.trimf(x_tip, [0, 0, 13])
tip_md = fuzz.trimf(x_tip, [0, 13, 25])
tip_hi = fuzz.trimf(x_tip, [13, 25, 25])


qual_level_lo = fuzz.interp_membership(x_qual, qual_lo, 6.5)
qual_level_md = fuzz.interp_membership(x_qual, qual_md, 6.5)
qual_level_hi = fuzz.interp_membership(x_qual, qual_hi, 6.5)

serv_level_lo = fuzz.interp_membership(x_serv, serv_lo, 9.8)
serv_level_md = fuzz.interp_membership(x_serv, serv_md, 9.8)
serv_level_hi = fuzz.interp_membership(x_serv, serv_hi, 9.8)


print(qual_level_lo)
print(qual_level_md)
print(qual_level_hi)
"""