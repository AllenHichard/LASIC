class Regra:

    def __init__(self, antecedentes, consequente, tnorma, peso):
        self.antecedentes = antecedentes
        self.consequente = consequente
        self.tnorma = tnorma
        self.peso = peso

    def getAntecedentes(self):
        return self.antecedentes

    def getConsequente(self):
        return self.consequente

    def getPeso(self):
        return self.peso

    def getTnorma(self):
        return self.tnorma

    def __eq__(self, other):
        return self.antecedentes == other

    def __str__(self):
        return str(self.antecedentes) + " - " + str(self.consequente)