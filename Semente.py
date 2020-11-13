from ExtracaoKeel import LeitorKeel as reader, LeitorDiretorio as ltr
from SistemaFuzzy.BaseConhecimento import BaseDados
from SistemaFuzzy.BaseConhecimento import BaseRegras
from SistemaFuzzy.Raciocinio import Geral

def __getSemente__(obj_reader, base_de_dados, base_de_regras):
    #criação dos conjuntos fuzzy e partições de entradas
    base_de_dados.criarConjuntos(obj_reader.inputs, obj_reader.centroids)
    conjuntos_de_entradas_fuzzy = base_de_dados.__getConjuntosFuzzy__()
    particoes_entradas = base_de_dados.__getParticoes__()
    #Construção das regras para o sistema fuzzy
    base_de_regras.wangMendel(conjuntos_de_entradas_fuzzy, particoes_entradas, obj_reader.instancias)
    #Escolhe entre com e sem pesos
    regras = base_de_regras.__getRegras__()
    return regras[0], regras[1], obj_reader.centroids




