class Semente:

    def __init__(self, regras, instancias, particoes):
        self.regras = regras
        self.instancias = instancias
        self.particoes = particoes
        self.qtdAntecedenteRegra = len(regras[0].antecedentes)
        self.maxAtributos = len(instancias) * (self.qtdAntecedenteRegra + 1)

    def preProcessamentoRegra(self):
        antecedentes = []
        consequentes = []
        for regra in self.regras:
            antecedentes += regra.antecedentes
            consequentes.append(regra.consequente)
        return antecedentes, consequentes

    def preProcessamentoCentroid(self):
        limiteInferior = []
        centroids = []
        limiteSuperior = []
        variacao_max_conjuntos = []
        for particao in self.particoes:
            limiteInferior += particao.limiteInferior
            limiteSuperior += particao.limiteSuperior
            centroids += particao.pontosCentrais
            variacao_max_conjuntos.append(len(particao.tiposConjunto)-1)
        return limiteInferior, centroids, limiteSuperior, variacao_max_conjuntos