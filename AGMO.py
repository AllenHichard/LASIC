import Semente
import Fitness
from ExtracaoKeel import LeitorKeel as reader, LeitorDiretorio as ltr
from SistemaFuzzy.BaseConhecimento import BaseDados
from SistemaFuzzy.BaseConhecimento import BaseRegras
from SistemaFuzzy.Raciocinio import Geral
from examples.multiobjective.nsgaii import nsgaii_kakarotto as nsgaii

paths_treino = ltr.datasets("tra")
paths_teste = ltr.datasets("tst")
for dirTreino, dirTeste in zip(paths_treino, paths_teste):
    obj_reader = reader.LeitorKeel(dirTreino)
    obj_reader.cabecalho()
    #instanciando objetos de dados e regras
    base_de_dados = BaseDados.BaseDados()
    base_de_regras = BaseRegras.BaseRegras()
    semente = Semente.__getSemente__(obj_reader, base_de_dados, base_de_regras)
    pesos = [1] * len(semente[0])
    objetivo = Fitness.__getFitness__(obj_reader, semente, pesos)
    print(objetivo)
    nsgaii.nsgaii_classify()


