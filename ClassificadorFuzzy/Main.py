from ClassificadorFuzzy.Diretorio import LeitorDiretorio
from ClassificadorFuzzy.Keel import LeitorKeel
from ClassificadorFuzzy.SistemaFuzzy.BaseConhecimento.BaseDados import BaseDados
from ClassificadorFuzzy.SistemaFuzzy.BaseConhecimento.BaseRegras import BaseRegras
from ClassificadorFuzzy.SistemaFuzzy.Raciocinio.Geral import Classificacao
from ClassificadorFuzzy.SistemaFuzzy.BaseConhecimento.AlgoritmoPesos.HisaoIshibuchi import PesoHisao
from examples.multiobjective.nsgaii import nsgaii_fuzzy as nsgaii

arquivos_treinamento = LeitorDiretorio.datasets("tra")
arquivos_teste = LeitorDiretorio.datasets("tst")
for nome_arquivo_train, nome_arquivo_test in zip(arquivos_treinamento, arquivos_teste):
    #Semente
    file = open(nome_arquivo_train, "r", encoding="utf8")
    extracao_keel = LeitorKeel.LeitorKeel(file)
    extracao_keel.extracaoDados()
    bd = BaseDados(extracao_keel.limites_inferiores_x, extracao_keel.limites_superiores_x, [1000,1000,1000,1000], [["TRAP", "TRI",  "TRAP"],["TRAP", "TRI",  "TRAP"],["TRAP", "TRI", "TRAP"],["TRAP", "TRI", "TRAP"]])
    particoes = bd.criarParticoes()
    br = BaseRegras(particoes, extracao_keel.instancias, extracao_keel.classes)
    regras = br.getRegras()
    pesoHisao = PesoHisao(particoes, regras, extracao_keel.instancias, extracao_keel.classes)
    pesos = pesoHisao.getPesos(False)
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