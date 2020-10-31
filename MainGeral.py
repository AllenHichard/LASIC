from ExtracaoKeel import LeitorKeel as reader, LeitorDiretorio as ltr
from SistemaFuzzy.BaseConhecimento import BaseDados
from SistemaFuzzy.BaseConhecimento import BaseRegras
from SistemaFuzzy.Raciocinio import Geral

paths_treino = ltr.datasets("tra")
paths_teste = ltr.datasets("tst")

for dirTreino, dirTeste in zip(paths_treino, paths_teste):
    #Treinamento
    obj_reader = reader.LeitorKeel(dirTreino)
    obj_reader.cabecalho()
    #print(obj_reader.relation)
    #obj_reader.__str__()

    base_de_dados = BaseDados.BaseDados()
    base_de_regras = BaseRegras.BaseRegras()

    conjuntos_de_entradas_fuzzy = base_de_dados.__getConjuntosFuzzy__()
    particoes_entradas = base_de_dados.__getParticoes__()

    base_de_dados.criarConjuntos(obj_reader.inputs)
    base_de_regras.wangMendel(conjuntos_de_entradas_fuzzy, particoes_entradas, obj_reader.instancias)

    regras = base_de_regras.__getRegras__()

    resultadoTreinamento = Geral.classificar(conjuntos_de_entradas_fuzzy, particoes_entradas, regras, obj_reader.instancias, obj_reader.output)
    print(resultadoTreinamento)
