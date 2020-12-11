from SistemaFuzzy.BaseConhecimento import Particao


class BaseDados:
    # pontos iniciais [0,1,2,1]
    # pontos finais [100, 80, 46, 80]
    # discretizações [1000, 1000, 1000]
    # TipoCOnjuntos [[TRI,][][][]]
    def __init__(self, pontos_iniciais, pontos_finais , discretizacoes, tipos_conjuntos):
        self.particoes = []
        self.pontos_iniciais = pontos_iniciais
        self.pontos_finais = pontos_finais
        self.discretizacoes = discretizacoes
        self.tipos_conjuntos = tipos_conjuntos

    def criarParticoes(self):
        for inicio, fim, discretizacao, tiposConjunto in zip(self.pontos_iniciais, self.pontos_finais , self.discretizacoes, self.tipos_conjuntos):
            particao = Particao.Particao(inicio, fim, discretizacao, tiposConjunto)
            particao.criarConjunto()
            #particao.plotParticao()
            self.particoes.append(particao)
        return self.particoes

"""
BaseDados = BaseDados([0,100], [100, 200], [1000,1000], [["TRAP", "TRI", "TRAP"],["TRAP", "TRI", "TRAP"]])
BaseDados.criarParticoes()
"""