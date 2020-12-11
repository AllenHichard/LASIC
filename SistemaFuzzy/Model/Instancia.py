class Instancia:

    def __init__(self, caracteristicas, classe):
        self.caracteristicas = caracteristicas
        self.classe = classe

    def __str__(self):
        return str([self.caracteristicas, self.classe])

