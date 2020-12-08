class Regra:

    def __init__(self, antecedentes, consequente, tnorma):
        self.antecedentes = antecedentes
        self.consequente = consequente
        self.tnorma = tnorma
        self.peso = 1

    def getAntecedentes(self):
        return self.antecedentes

    def getConsequente(self):
        return self.consequente

    def getPeso(self):
        return self.peso

    def getTnorma(self):
        return self.tnorma

    def nao_e_melhor_que(self, regra):
        return self.tnorma < regra.tnorma

    def eq_antecedentes(self, regra):
        return self.antecedentes == regra.antecedentes

    def __eq__(self, regra):
        return self.antecedentes == regra.antecedentes and self.consequente == regra.consequente

    def __str__(self):
        return str(self.antecedentes) + " - " + str(self.consequente)