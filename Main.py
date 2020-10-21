import LeitorKeel as reader
import LeitorDiretorio as ltr

paths_treino = ltr.datasets("tra")
for dir in paths_treino:
    obj_reader = reader.LeitorKeel(dir)
    obj_reader.cabecalho()
    obj_reader.__str__()

