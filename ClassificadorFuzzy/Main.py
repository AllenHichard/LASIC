from ClassificadorFuzzy.Diretorio import LeitorDiretorio
from ClassificadorFuzzy.Keel import LeitorKeel
from ClassificadorFuzzy.SistemaFuzzy.BaseConhecimento.BaseDados import BaseDados
from ClassificadorFuzzy.SistemaFuzzy.BaseConhecimento.BaseRegras import BaseRegras
from ClassificadorFuzzy.SistemaFuzzy.Raciocinio.Geral import Classificacao
from ClassificadorFuzzy.SistemaFuzzy.BaseConhecimento.AlgoritmoPesos.HisaoIshibuchi import PesoHisao

arquivos_treinamento = LeitorDiretorio.datasets("tra")
arquivos_teste = LeitorDiretorio.datasets("tst")
for nome_arquivo_train, nome_arquivo_test in zip(arquivos_treinamento, arquivos_teste):
    file = open(nome_arquivo_train, "r", encoding="utf8")
    extracao_keel = LeitorKeel.LeitorKeel(file)
    extracao_keel.extracaoDados()
    bd = BaseDados(extracao_keel.limites_inferiores_x, extracao_keel.limites_superiores_x, [1000,1000,1000,1000], [["TRAP", "TRI", "TRAP"],["TRAP", "TRI", "TRAP"],["TRAP", "TRI", "TRAP"],["TRAP", "TRI", "TRAP"]])
    particoes = bd.criarParticoes()
    br = BaseRegras(particoes, extracao_keel.instancias, extracao_keel.classes)
    regras = br.getRegras("Wang-Mendel")
    pesoHisao = PesoHisao(particoes, regras, extracao_keel.instancias, extracao_keel.classes)
    pesos = pesoHisao.getPesos(True)
    resultadoTrain = Classificacao(particoes, regras, pesos, extracao_keel.instancias, extracao_keel.classes)

    file = open(nome_arquivo_test, "r", encoding="utf8")
    extracao_keel = LeitorKeel.LeitorKeel(file)
    extracao_keel.extracaoDados()
    resultadoTeste = Classificacao(particoes, regras, pesos, extracao_keel.instancias, extracao_keel.classes)
    print(resultadoTrain.classificar(), resultadoTeste.classificar())