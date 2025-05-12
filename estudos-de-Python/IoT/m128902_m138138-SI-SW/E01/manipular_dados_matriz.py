# Função para calcular a média de cada coluna da matriz
def calcular_media_coluna(matriz):
  somar_colunas = [0] * len(matriz[0])
  for linha in matriz:
    for i, valor in enumerate(linha):
      somar_colunas[i] += valor
  medias = [soma / len(matriz) for soma in somar_colunas]
  return medias

# Função para centralizar cada valor da matriz pela média da respectiva coluna
def meancenter(matriz, media_colunas):
  centrar_matriz = []
  for linha in matriz:
    centrar_linhas = [valor - media_colunas[i] for i, valor in enumerate(linha)]
    centrar_matriz.append(centrar_linhas)
  return centrar_matriz

# Função para ler a matriz a partir de um arquivo de texto
def ler_matriz():
  with open('matriz.txt', 'r') as arquivo:
    matriz = [] # Armazena o arquivo como uma lista de listas
    for linha in arquivo:
      linhas = list(map(float, linha.strip().split()))
      matriz.append(linhas)
  return matriz

# Função para salvar uma matriz em um arquivo de texto
def salvar_matriz(caminho_arquivo, matriz):
  with open(caminho_arquivo, 'w') as arquivo:
    for linha in matriz:
      arquivo.write(" ".join(map(str, linha)) + "\n")

# Função para salvar um valor em um arquivo de texto
def salvar_vetor(caminho_arquivo, vetor):
  with open(caminho_arquivo, 'w') as arquivo:
    arquivo.write(" ".join(map(str, vetor)) + "\n")

matriz = ler_matriz()
media_colunas = calcular_media_coluna(matriz)
centrar_matriz = meancenter(matriz, media_colunas)
salvar_vetor('average-col.txt', media_colunas) # Contém as médias de cada coluna
salvar_matriz('meancenter-col.txt', centrar_matriz) # Contém a matriz centralizada pela média das colunas

# Exibe uma mensagem para indicar o êxito da aplicação
print('Arquivos "average-col.txt" e "meancenter-col.txt" gerados com sucesso.')
