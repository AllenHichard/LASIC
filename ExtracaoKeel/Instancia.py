class Instancia:

    def __init__(self):
        self.atributos = []
        self.classe = 0

    def __setAtributos__(self, atributos):
        self.atributos = atributos

    def __setClasse__(self, classe):
        self.classe = classe

    def __getAtributos__(self):
        return self.atributos

    def __getClasse__(self):
        return self.classe

