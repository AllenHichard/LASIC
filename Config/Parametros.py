arq_entrada = open("FORMAT.FLC", 'r')
conjunto_entradas = \
{'SISTEMA FUZZY': '',
'CONJUNTO FUZZY': '',
'GRANULARIDADE': 3,
'OPERADOR COMPOSICAO': '',
'OPERADOR AGREGACAO': '',
'INFERENCIA': '',
'REGRA': False,
'DEFAULT': ''}

for linha in arq_entrada.readlines():
    #print(linha)
    variavel = linha.split(':')[0]
    valor = linha.split(':')[1].split('#')[0]
    conjunto_entradas[variavel] = valor
print(conjunto_entradas)
