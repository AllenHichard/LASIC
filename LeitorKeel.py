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
                    self.output[label[index]] = index
            elif line.__contains__("data"):
                self.instancias()

    def instancias(self):
        for line in self.file:
            sample = line.replace(" ", "").split("\n")[0].split(",")
            rotulo = sample.__getitem__(len(sample)-1)
            idRotulo = self.output[rotulo]
            sample[len(sample)-1] = idRotulo
            self.data.append(sample)

    def __str__(self):
        print("Nome do dataset = {}\nEntradas = {}\nSaída = {}\n".format(self.relation, self.inputs, self.output))
        for instancia in self.data:
            print(instancia)



