#ia.ex -- 1)
#calculadora simples
print("|1| = adição, |2| = subtração, |3| = multiplicação, |4| = divisão")
opera = int (input("Escolha uma operação: "))
num1 =float (input("Primeiro numero: "))
num2 =float (input("Segundo numero: "))

if opera == 1:
    resultado = num1 + num2
    print("O resultado da operação é: ", resultado)
elif opera == 2:
    resultado = num1 - num2
    print("O resultado da operação é: ", resultado)
elif opera == 3:
    resultado = num1 * num2
    print("O resultado da operação é: ", resultado)
elif opera == 4:
    resultado = num1 / num2
    print("O resultado da operação é: ", resultado)
else:
    print("ERRO: Operação inválida")

#2)
#conversor de temperatura
print("|C| = Celsius, |F| = Fahrenheit")
unidade = input("Comverter para qual: ").strip()
temperatura = float(input("temperatura: "))

if unidade == 'C' or unidade == 'c':
    celsius = (temperatura - 32) * 5/9
    print("A temperatura convertido:",celsius)
elif unidade == 'F' or unidade == 'f':
    fahrenheit = (temperatura * 9/5) + 32
    print("A temperatura convertido:",fahrenheit)
else:
    print("ERRO: Operação inválida")

#3)
#Contador de Vogais
texto = input("excreva um texto: ").strip()

#primeira resposta da ia copilot
'''def contar_vogais(string):
    vogais = "aeiouAEIOU"
    contador = 0
    for char in string:
        if char in vogais:
            contador += 1
    return contador

# Exemplo de uso
texto = input("Digite uma frase: ")
total_vogais = contar_vogais(texto)
print(f"O número de vogais na frase é: {total_vogais}")'''

#segunda resposta da ia copilot
'''def contar_vogais(string):
    return sum(1 for char in string if char.lower() in "aeiou")
    
# Exemplo de uso
texto = input("Digite uma frase: ")
total_vogais = contar_vogais(texto)
print(f"O número de vogais na frase é: {total_vogais}")'''

#4)
#Verificação de Número Primo

numero =int (input("numero para verificar:"))
if (numero % 2) != 0 and (numero % 3) != 0 and (numero % 5) != 0:
    print(f"O numero {numero} não é primo")
else:
    print(f"O numero {numero} é primo")