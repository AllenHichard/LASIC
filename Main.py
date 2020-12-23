from Util.Diretorio import LeitorDiretorio
from Util.Keel import LeitorKeel
from SistemaFuzzy.BaseConhecimento.BaseDados import BaseDados
from SistemaFuzzy.BaseConhecimento.BaseRegras import BaseRegras
from SistemaFuzzy.Raciocinio.Geral import Classificacao
from SistemaFuzzy.BaseConhecimento.AlgoritmoPesos.HisaoIshibuchi import PesoHisao
from AlgoritmoGenetico import main_nsgaii_fuzzy as nsgaii
import parametros

arquivos_treinamento = LeitorDiretorio.datasets("tra")
arquivos_teste = LeitorDiretorio.datasets("tst")
for nome_arquivo_train, nome_arquivo_test in zip(arquivos_treinamento, arquivos_teste):
    #Semente
    file = open(nome_arquivo_train, "r", encoding="utf8")
    extracao_keel_train = LeitorKeel.LeitorKeel(file)
    extracao_keel_train.extracaoDados()
    default = parametros.Default(extracao_keel_train.qtdCaracteristicas)
    bd = BaseDados(extracao_keel_train.limites_inferiores_x, extracao_keel_train.limites_superiores_x, default.discretizacoes, default.particoes )
    particoes = bd.criarParticoes()
    br = BaseRegras(particoes, extracao_keel_train.instancias, extracao_keel_train.classes)
    regras = br.getRegras() #"Wang-Mendel"
    pesoHisao = PesoHisao(particoes, regras, extracao_keel_train.instancias, extracao_keel_train.classes)
    pesoHisao.getPesos(False)

    # Algoritmo Genético
    particoesAG, regrasAG = nsgaii.nsgaii_train(particoes.copy(), regras.copy(), extracao_keel_train.instancias,
                                                extracao_keel_train.classes)

    file = open(nome_arquivo_test, "r", encoding="utf8")
    extracao_keel_test = LeitorKeel.LeitorKeel(file)
    extracao_keel_test.extracaoDados()

    resultadoTrainSAG = Classificacao(particoes, regras, extracao_keel_train.instancias, extracao_keel_train.classes)
    resultadoTesteSAG = Classificacao(particoes, regras, extracao_keel_test.instancias, extracao_keel_test.classes)



    resultadoTrainCAG = Classificacao(particoesAG, regrasAG, extracao_keel_train.instancias,
                                      extracao_keel_train.classes)
    resultadoTesteCAG = Classificacao(particoesAG, regrasAG, extracao_keel_test.instancias, extracao_keel_test.classes)

    print("Resultados Finais Sem AG")
    print(resultadoTrainSAG.classificar(), resultadoTesteSAG.classificar()[0])
    print("Resultados Finais Com AG")
    print(resultadoTrainCAG.classificar(), resultadoTesteCAG.classificar()[0])







