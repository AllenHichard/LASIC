import SBRF
import Fitness
from ExtracaoKeel import LeitorKeel as reader, LeitorDiretorio as ltr
from SistemaFuzzy.BaseConhecimento import BaseDados
from SistemaFuzzy.BaseConhecimento import BaseRegras
from SistemaFuzzy.Raciocinio import Geral

paths_treino = ltr.datasets("tra")
paths_teste = ltr.datasets("tst")

for dirTreino, dirTeste in zip(paths_treino, paths_teste):
    # Semente
    obj_reader = reader.LeitorKeel(dirTreino)
    obj_reader.cabecalho()
    base_de_dados = BaseDados.BaseDados()
    base_de_regras = BaseRegras.BaseRegras()
    semente = SBRF.__getSemente__(obj_reader, base_de_dados, base_de_regras)
    if True:
        pesos = base_de_regras.calculaPesos(base_de_dados.conjuntos_de_entradas_fuzzy, base_de_dados.particoes_entradas, obj_reader.instancias,
                                                obj_reader.output)
    else:
        pesos = [1] * len(semente[0])

    objetivo = Fitness.__getFitness__(obj_reader, semente, pesos)
    print(objetivoInicial)

    #Treinamento
    """
    Chama o ag, passar o cromossomo - sementre
    aguardar o resultado final 
    retorna melhor cromossomo
    """

    #Teste
    obj_reader_teste = reader.LeitorKeel(dirTeste)
    obj_reader_teste.cabecalho()
    regras = [semente[0], semente[1]]
    resultadoTeste = Geral.classificar("MEAN", base_de_dados.conjuntos_de_entradas_fuzzy, base_de_dados.particoes_entradas, regras, pesos,
                                       obj_reader_teste.instancias, obj_reader_teste.output)
    print(resultadoTesteFinal)