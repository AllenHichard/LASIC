from ExtracaoKeel import LeitorKeel as reader
from SistemaFuzzy.BaseConhecimento import BaseDados
from SistemaFuzzy.BaseConhecimento import BaseRegras
from SistemaFuzzy.Raciocinio import Geral


def SistemaFuzzy(paths_treino, paths_teste, agregacao,composicao, temPeso):
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
        #print(regras[0].__len__())
        if temPeso:
            pesos = base_de_regras.calculaPesos(base_de_dados.conjuntos_de_entradas_fuzzy, base_de_dados.particoes_entradas,
                                                obj_reader.instancias,obj_reader.output)
        else:
            pesos = [1] * len(regras[0])
        treinamento = Geral.classificar(agregacao,composicao,
                                  conjuntos_de_entradas_fuzzy,
                                  particoes_entradas,
                                  regras,
                                  pesos,
                                  obj_reader.instancias,
                                  obj_reader.output)
        obj_reader_teste = reader.LeitorKeel(dirTeste)
        obj_reader_teste.cabecalho()
        teste = Geral.classificar(agregacao,composicao, base_de_dados.conjuntos_de_entradas_fuzzy,
                                           base_de_dados.particoes_entradas, regras, pesos,
                                           obj_reader_teste.instancias, obj_reader_teste.output)
        print("Treinamento ", treinamento, "Teste", teste)