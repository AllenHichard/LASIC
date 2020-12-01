import json

def getArcEntrada():
    with open('Config/FORMAT.json', 'r') as json_file:
        dados_entrada = json.load(json_file)
    return dados_entrada


#print(type(dados_entrada['GRANULARIDADE']), type(dados_entrada['REGRA']))
