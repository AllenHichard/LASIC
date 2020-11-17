from ExtracaoKeel import LeitorKeel as reader, LeitorDiretorio as ltr
from SistemaFuzzy.BaseConhecimento import BaseDados
from SistemaFuzzy.BaseConhecimento import BaseRegras
from SistemaFuzzy.Raciocinio import Geral
import Reducao_Regras as red


def __getFitness__(obj_reader, cromossomo, pesos):
    (antecedentes, classes, centroids) = cromossomo
    base_de_dados = BaseDados.BaseDados()
    base_de_dados.criarConjuntos(obj_reader.inputs, centroids)
    conjuntos_de_entradas_fuzzy = base_de_dados.__getConjuntosFuzzy__()
    particoes_entradas = base_de_dados.__getParticoes__()
    regras = [antecedentes, classes]
    #print(1, regras)
    regras = red.reduzir(conjuntos_de_entradas_fuzzy, particoes_entradas, regras,
                                                 pesos, obj_reader.instancias)
    #print(2, regras)
    return regras, Geral.classificar("MEAN",
                             conjuntos_de_entradas_fuzzy,
                             particoes_entradas,
                             regras,
                             pesos,
                             obj_reader.instancias,
                             obj_reader.output)




