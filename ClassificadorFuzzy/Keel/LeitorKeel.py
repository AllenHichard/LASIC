from ClassificadorFuzzy.Model import Instancia
import re

class LeitorKeel:

    def __init__(self, file):
        self.nome_dataset = ""
        self.nomes_caracteristicas = []
        self.nome_classe = "" #Class
        self.classes = []
        self.limites_inferiores_x = []
        self.limites_superiores_x = []
        self.instancias = []
        self.file = file

    def extracaoDados(self):
        [cabecalho_dataset, instancias_dataset] = self.file.read().replace(' ', "").split("@data")
        self.nomes_inputs_outputs(cabecalho_dataset)
        self.limites_inferior_superior(cabecalho_dataset)
        instancias_dataset = self.nominal_para_Inteiro(self.classes, instancias_dataset)
        self.getInstancias(instancias_dataset)

    def nomes_inputs_outputs(self,cabecalho_dataset, ):
        for line in cabecalho_dataset.split("\n"):
            if line.__contains__("@relation"):
                self.nome_dataset = line.split("@relation")[1]
            elif line.__contains__("@inputs"):
                self.nomes_caracteristicas = line.split("@inputs")[1].split(",")
            elif line.__contains__("@outputs"):
                self.nome_classe = line.split("@outputs")[1]

    def limites_inferior_superior(self,cabecalho_dataset):
        for line in cabecalho_dataset.split("@inputs")[0].split("\n"):
            for nome_caracteristica in self.nomes_caracteristicas:
                if line.__contains__(nome_caracteristica):
                    inferior, superior = re.search("\[[\w|\W]+\]", line).group().split(",")
                    inferior = float(re.search("\d+((.)\d*)?", inferior).group())
                    superior = float(re.search("\d+((.)\d*)?", superior).group())
                    self.limites_inferiores_x.append(inferior)
                    self.limites_superiores_x.append(superior)
            if line.__contains__(self.nome_classe):
                self.classes = re.search("\{[\w|\W]+\}", line).group()
                self.classes = self.classes.replace("{", "").replace("}", "").split(",")


    def nominal_para_Inteiro(self, classes, instancias_dataset):
        for index, classe in enumerate(classes):
            instancias_dataset = instancias_dataset.replace(classe, str(index))
        return instancias_dataset


    def getInstancias(self, instancias_dataset):
        separador = len(self.limites_inferiores_x)
        for instancia in instancias_dataset.split("\n"):
            if instancia != "":
                dados_instancia = instancia.split(",")
                caracteristicas = [float(dado) for dado in dados_instancia[:separador]]
                classe = int(dados_instancia[separador])
                instancia = Instancia.Instancia(caracteristicas, classe)
                self.instancias.append(instancia)

    def printInstancias(self):
        for instancia in self.instancias:
            print(instancia)


"""
file = open("C:\\Lasic\\LASIC/dataset/iris-10-fold/iris-10-1tra.dat", "r", encoding="utf8")
keel = LeitorKeel(file)
keel.extracaoDados()
keel.printInstancias()
print(keel.limites_inferiores_x)
print(keel.limites_superiores_x)
"""




