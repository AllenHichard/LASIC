import Semente
import Fitness
from ExtracaoKeel import LeitorKeel as reader, LeitorDiretorio as ltr
from SistemaFuzzy.BaseConhecimento import BaseDados
from SistemaFuzzy.BaseConhecimento import BaseRegras
from SistemaFuzzy.Raciocinio import Geral
from examples.multiobjective.nsgaii import nsgaii_kakarotto as nsgaii


def lower_upper_class(outputs):
    limitClass = list(outputs.values())
    return limitClass[len(limitClass)-1], limitClass[0]
def lower_upper_centroids(inputs, centroids):
    lower_centroids = []
    upper_centroids = []
    for chave, PM in zip(inputs, centroids):
        PI = inputs[chave][0]
        PS = inputs[chave][1]
        vi = PM - ((PM - PI) / 2)
        vs = PM + ((PS - PM) / 2)
        lower_centroids.append(vi)
        upper_centroids.append(vs)
    return lower_centroids, upper_centroids

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
    #lower_upper_inputs(obj_reader.inputs, semente[2])
    #print(objetivo)
    nsgaii.nsgaii_train(obj_reader, semente, lower_upper_class(obj_reader.output), lower_upper_centroids(obj_reader.inputs, semente[2]) )




