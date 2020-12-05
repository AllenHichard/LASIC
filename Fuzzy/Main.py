from Fuzzy.Keel import LeitorDiretorio, LeitorKeel
from Fuzzy.BaseDados import BaseDados
from Fuzzy.BaseRegras import BaseRegras
from Fuzzy.Classificacao import Classificacao
arquivos_treinamento = LeitorDiretorio.datasets("tra")
arquivos_teste = LeitorDiretorio.datasets("tst")
for nome_arquivo_train, nome_arquivo_test in zip(arquivos_treinamento, arquivos_teste):
    file = open(nome_arquivo_train, "r", encoding="utf8")
    extracao_keel = LeitorKeel.LeitorKeel(file)
    extracao_keel.extracaoDados()
    bd = BaseDados(extracao_keel.limites_inferiores_x, extracao_keel.limites_superiores_x, [1000,1000,1000,1000], [["TRAP", "TRI", "TRAP"],["TRAP", "TRI", "TRAP"],["TRAP", "TRI", "TRAP"],["TRAP", "TRI", "TRAP"]])
    particoes = bd.criarParticoes()
    br = BaseRegras(particoes, extracao_keel.instancias)
    br.wangMendel()
    classificacao = Classificacao(particoes, br.regras, extracao_keel.instancias, extracao_keel.classes)
    print(classificacao.classificar())

    file = open(nome_arquivo_test, "r", encoding="utf8")
    extracao_keel = LeitorKeel.LeitorKeel(file)
    extracao_keel.extracaoDados()
    classificacao = Classificacao(particoes, br.regras, extracao_keel.instancias, extracao_keel.classes)
    print(classificacao.classificar())