from Util.Diretorio import LeitorDiretorio
from Util.Keel import LeitorKeel
from SistemaFuzzy.BaseConhecimento.BaseDados import BaseDados
from SistemaFuzzy.BaseConhecimento.BaseRegras import BaseRegras
from SistemaFuzzy.Raciocinio.Geral import Classificacao
from SistemaFuzzy.BaseConhecimento.AlgoritmoPesos.HisaoIshibuchi import PesoHisao
from AlgoritmoGenetico import main_nsgaii_fuzzy as nsgaii

arquivos_treinamento = LeitorDiretorio.datasets("tra")
arquivos_teste = LeitorDiretorio.datasets("tst")
for nome_arquivo_train, nome_arquivo_test in zip(arquivos_treinamento, arquivos_teste):
    #Semente
    file = open(nome_arquivo_train, "r", encoding="utf8")
    extracao_keel = LeitorKeel.LeitorKeel(file)
    extracao_keel.extracaoDados()
    bd = BaseDados(extracao_keel.limites_inferiores_x, extracao_keel.limites_superiores_x, [1000,1000,1000,1000], [["TRAP", "TRI", "TRAP"],["TRAP", "TRAP", "TRAP", "TRAP"],["TRAP", "TRI", "GAUSS","TRI"],["TRAP","GAUSS", "TRAP"]])
    particoes = bd.criarParticoes()
    br = BaseRegras(particoes, extracao_keel.instancias, extracao_keel.classes)
    regras = br.getRegras("Wang-Mendel")
    pesoHisao = PesoHisao(particoes, regras, extracao_keel.instancias, extracao_keel.classes)
    pesoHisao.getPesos(False)
    #for regra in regras:
        #print(regra.peso)
    #particoes[0].setPontoCentral(6.7)
    #particoes[1].setPontoCentral(3.5)
    #particoes[2].setPontoCentral(4.2)
    #particoes[3].setPontoCentral(1.0)
    #particoes[0].plotParticao()
    #print("a", particoes[0].pontosCentrais)
    resultadoTrain = Classificacao(particoes, regras, extracao_keel.instancias, extracao_keel.classes)

    #Algoritmo Genético
    nsgaii.nsgaii_train(particoes, regras, extracao_keel.instancias, extracao_keel.classes)

    #Teste
    file = open(nome_arquivo_test, "r", encoding="utf8")
    extracao_keel = LeitorKeel.LeitorKeel(file)
    extracao_keel.extracaoDados()
    resultadoTeste = Classificacao(particoes, regras, extracao_keel.instancias, extracao_keel.classes)
    print(resultadoTrain.classificar(), resultadoTeste.classificar())