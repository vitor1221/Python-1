#import locale #inporta a biblioteca locale
#locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8') #define o local como português 
#Lista de python
nome = "Vitor"
print(F"Meu nome é: {nome}.")#F String

##tipos de variaveis
#
inteiro = 0 #int
texto = "texto" #String
ponto_fluante = 1.0 #float
Booleano = True #bool True ou False
variavel = 1
numero = 1
print(type(variavel))#veriviva e mostra o tipo de variavel
variavel = float(numero)#converte variaveis para outro tipo de variavel
#nome da variavel = tipo da variavel(valor para entrar na variavel)
variavel =int (input("Digite uma variavel \n"))#Scaner; \n para pular uma linha
#variavel para guardar valor = tipo de variavel(input(texto opcional))

##listas
lista = []
lista = [1,2,3,4,5,6,1,7]#começa com 0 e termina com n-1;contagem contraria dos índices -1 a -(n)
print(lista[0])
print(lista[-1])
lista.extend([8,9])#extende a lista com outra lista
print(lista)
lista.append(10)#adiciona ao fim ada lista uma valor
print(lista)
lista.insert(0,0)#insere na posição 0 o valor 0, nesta ordem; move os outros indice
print(lista)
lista.pop()#remove o ultimo indice
print(lista)
lista.remove(1)#remove o valor da lista, mas se tiver mais de um remove o primeiro
print(lista)
lista.clear()#limpa a lista
print(lista)
lista = [0,0,1,4,3,10,9,0]
print(lista.index(0))#acha o índice do valor pedido
print(lista.count(0))#conta as vezes que tem o valor pedido
lista.sort()#ordena a lista de maneira alfabética ou crescente
print(lista)
lista.reverse()#inverte a ordem da lista
lista2 = lista.copy()#para fazer uma copia da lista(pensa em backup)
tuples = (0, 1)#lista que não pode ser mudada

##estruturas

#estrutura condicional
if variavel < 10:#se
    print(f"a variavel:{variavel} tem um valor menor que 10")
elif variavel > 10:# se com senão
    print(f"a variavel:{variavel} tem um valor maior que 10")
else:#senão
    print(f"a variavel:{variavel} tem um valor igual 10")

#estrutura de repetição
i = 1
while i < 10:#enquanto i menor que 10 faz:
    print(i)
    i += 1
print("fim da repetição com while")

#para i em lista
for l in lista: #para
    print(l)

#sintaxe (começo,ate onde vai -1(obrigatorio), de quantos em quantos)
for i in range(3,25,3):
    print(i)


#operadores
''' COMPARAÇÂO
    igualdade           ==
    diferença           !=
    maior               > 
    maior igual         >=
    menor               <
    menor igual         <=

    LOGICOS
    or                  ou
    and                 e
    not                 não

    ARTIMEDICAS
    Adição              +
    Subtração           -
    Multiplicação       *
    Divisão             /
    Divisão (inteira)   //
    Divisão (Resto)     %'''

#fução
def funcao(variavel,numero):#declara a fução e passa dois parametros
    #altos codigos
    print(f"texto da função; valor da variavel que entra na fução : {variavel}")#printa um dos parametros passados
    return variavel + numero #retorna a soma dos parametros
retorno = funcao(variavel,numero) #coloca o valor que retorna da fução em uma variavel e chama a função
print(f"valor de retorno da fução:{retorno}") #printa o valor que vem da função

#Recursividade
def recursão(i, f):
    print(f"Exemplo de Recursão {i}") #definição de uma função
    i +=1
    if i == 5:                   # 
        return                   #definiçã de ponto de parada
    else:
        recursão(i, f)              #

recursão(0, 5) #chamada da função e da o valor a ela

#metodo de busta
#sequencial
def busca_seq(lista, num):
    total = 0
    res = []
    for i in range(len(lista)):
        if lista[i] == num:
            res.append(i)
            total += 1
            return i, total, True, False if len(res) == 0 else res
    return None, False

numero_busca = 1
info_lista = busca_seq(lista,numero_busca)
print(info_lista)
print("indice, ocorrências, fezientensia, índice das ocorrências")

#binaria
def busca_binaria(lista, num):
    inicio = 0
    fim = len(lista) -1

    while inicio <= fim:
        meio = (inicio + fim)//2

        if num == lista[meio]:
            return meio
        elif num < lista[meio]:
            fim = meio - 1
        else:
            inicio = meio + 1
    
    return None

resultado = busca_binaria(lista,numero_busca)
print(resultado)

#metodo de ordenação
lista = [1,4,3,20,6,55,5,7,9,3,100]
lista_ordenada = sorted(lista)
print(lista_ordenada)
print(lista)

lista.sort()
print(lista)
lista.sort(reverse=True)
print(lista)

student_tuples = [
    ('john', 'A', 15),
    ('jane', 'B', 12),
    ('dave', 'B', 10),
]
sorted(student_tuples, key=lambda student: student[2])   # sort by age
[('dave', 'B', 10), ('jane', 'B', 12), ('john', 'A', 15)]
#https://docs.python.org/pt-br/dev/howto/sorting.html

#arquivos
'''
"r" -> Usado somente para ler algo
"w" -> Usado somente para escrever algo
"r+" -> Usado para ler e escrever algo
"a" -> Usado para acrescentar algo
'''
arquivo = open("arquivo.txt", "w")#abre o arquivo
arquivo.write("Olá mundo!")#escreve no arquivo
#arquivo.seek(0,0)#posicionar ponteiro do arquivo
#arquivo.read()#ler arquivo
arquivo.close()#fecha o arquivo
#https://docs.python.org/pt-br/3/tutorial/inputoutput.html#reading-and-writing-files

##coisa a mais por organizar
print(f"\033[31mtexto em vermelho\033[0m")#printa com uma cor o texto
#https://awari.com.br/python-aprenda-a-imprimir-em-cores/?utm_source=blog&utm_campaign=projeto+blog&utm_medium=Python:%20Aprenda%20a%20Imprimir%20em%20Cores


#lista por organizar
'''
False      await      else       import     pass
None       break      except     in         raise
True       class      finally    is         return
and        continue   for        lambda     try
as         def        from       nonlocal   while
assert     del        global     not        with
async      elif       if         or         yield


False: Representa o valor booleano falso.

await: Utilizada para esperar por um resultado em funções assíncronas.

else: Define um bloco de código que será executado se a condição em um if ou elif for falsa.

import: Importa módulos para o script.

pass: Indica um bloco de código vazio, usado como um placeholder.

None: Representa a ausência de valor ou um valor nulo.

break: Interrompe um loop for ou while.

except: Define um bloco de código que será executado se ocorrer uma exceção.

in: Verifica se um valor está presente em uma sequência (como uma lista, tupla ou string).

raise: Lança uma exceção.

True: Representa o valor booleano verdadeiro.

class: Define uma nova classe.

finally: Define um bloco de código que será executado independentemente de uma exceção ter ocorrido ou não.

is: Verifica se duas variáveis referenciam o mesmo objeto.

return: Finaliza a execução de uma função e retorna um valor.

and: Operador lógico que retorna verdadeiro se ambas as expressões forem verdadeiras.

continue: Interrompe a iteração atual de um loop e passa para a próxima iteração.

for: Inicia um loop que itera sobre uma sequência.

lambda: Cria uma função anônima.

try: Define um bloco de código para testar uma exceção.

as: Cria um alias para um módulo importado.

def: Define uma nova função.

from: Importa partes específicas de um módulo.

nonlocal: Declara que uma variável não é local e deve ser referenciada no escopo mais externo.

while: Inicia um loop que continua enquanto uma condição for verdadeira.

assert: Verifica se uma condição é verdadeira e lança uma exceção se for falsa.

del: Remove uma variável, lista, ou item de um dicionário.

global: Declara que uma variável é global.

not: Operador lógico que inverte o valor de uma expressão.

with: Simplifica o gerenciamento de recursos, como arquivos.

async: Define uma função assíncrona.

elif: Define uma condição adicional em um bloco if.

if: Inicia uma declaração condicional.

or: Operador lógico que retorna verdadeiro se pelo menos uma das expressões for verdadeira.

yield: Pausa a execução de uma função e retorna um valor para o chamador, podendo ser retomada posteriormente.'''