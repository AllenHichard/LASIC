from ExtracaoKeel import LeitorKeel as reader, LeitorDiretorio as ltr
from SistemaFuzzy.BaseConhecimento import BaseDados
from SistemaFuzzy.BaseConhecimento import BaseRegras
from SistemaFuzzy.Raciocinio import Geral

paths_treino = ltr.datasets("tra")
paths_teste = ltr.datasets("tst")
for dirTreino, dirTeste in zip(paths_treino, paths_teste):
    obj_reader = reader.LeitorKeel(dirTreino)
    obj_reader.cabecalho()
    base_de_dados = BaseDados.BaseDados()
    base_de_regras = BaseRegras.BaseRegras()
    base_de_dados.criarConjuntos(obj_reader.inputs, obj_reader.centroids)
    conjuntos_de_entradas_fuzzy = base_de_dados.__getConjuntosFuzzy__()
    particoes_entradas = base_de_dados.__getParticoes__()
    # Construção das regras para o sistema fuzzy
    base_de_regras.wangMendel(conjuntos_de_entradas_fuzzy, particoes_entradas, obj_reader.instancias)
    # Escolhe entre com e sem pesos
    regras = base_de_regras.__getRegras__()
    if False:
        pesos = base_de_regras.calculaPesos(base_de_dados.conjuntos_de_entradas_fuzzy, base_de_dados.particoes_entradas,
                                            obj_reader.instancias,obj_reader.output)
    else:
        pesos = [1] * len(regras[0])
    treinamento = Geral.classificar("MEAN",
                              conjuntos_de_entradas_fuzzy,
                              particoes_entradas,
                              regras,
                              pesos,
                              obj_reader.instancias,
                              obj_reader.output)
    obj_reader_teste = reader.LeitorKeel(dirTeste)
    obj_reader_teste.cabecalho()
    teste = Geral.classificar("MEAN", base_de_dados.conjuntos_de_entradas_fuzzy,
                                       base_de_dados.particoes_entradas, regras, pesos,
                                       obj_reader_teste.instancias, obj_reader_teste.output)
    print(treinamento, teste)