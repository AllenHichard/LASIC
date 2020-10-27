class LeitorKeel:

    def __init__(self, dir):
        self.relation = ""
        self.inputs = {}
        self.output = {}
        self.data = []
        self.file = open(dir, "r")

    def cabecalho(self):
        for line in self.file:
            if line.__contains__("relation"):
                self.relation = line.split(" ")[1].split("\n")[0]
            elif line.__contains__("["):
                universe = line.split("[")
                interval = universe[1].split("]")[0].replace(" ", "").split(",")
                interval = [float(val) for val in interval]
                self.inputs[universe[0].split(" ")[1]] = interval
            elif line.__contains__("{"):
                label = line.split("{")[1].split("}")[0].replace(" ", "").split(",")
                for index in range(len(label)):
                    self.output[label[index]] = -(index + 1)
            elif line.__contains__("data"):
                self.instancias()

    def instancias(self):
        for line in self.file:
            instancia_completa = line.replace(" ", "").split("\n")[0].split(",")
            instancia_atributos = [float(val) for val in instancia_completa[:len(instancia_completa)-1]]
            rotulo = instancia_completa.__getitem__(len(instancia_completa)-1)
            idRotulo = self.output[rotulo]
            instancia_atributos.append(idRotulo)
            instancia_completa = instancia_atributos.copy()
            self.data.append(instancia_completa)

    def __str__(self):
        print("Nome do dataset = {}\nEntradas = {}\nSaída = {}\n".format(self.relation, self.inputs, self.output))
        for instancia in self.data:
            print(instancia)



