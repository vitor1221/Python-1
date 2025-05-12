import tkinter as tk

# Função para contar palavras e caracteres de um texto
def contar_palavras_caracteres(texto):
    palavras = len(texto.split())
    caracteres = len(texto.replace(" ", "")) # Conta os caracteres sem espaços
    return palavras, caracteres

# Função para acessar um arquivo e lê-lo
def abrir_arquivo():
    with open('texto.txt', mode= 'r') as arquivo:
        texto = arquivo.read()

    palavras, caracteres = contar_palavras_caracteres(texto)

    # Exibir os resultados na GUI
    lbl_palavras['text'] = f"Total de palavras: {palavras}"
    lbl_caracteres['text'] = f"Total de caracteres: {caracteres}"

    # Salvar o resultado em um novo arquivo de texto
    with open('resultado.txt', 'w') as arquivo:
        arquivo.write(texto)

# Criação da interface gráfica
root = tk.Tk()
root.title("Contador de Palavras e Caracteres em Python")

# Botão para acessar o arquivo
btn_abrir = tk.Button(root, text= "Abrir arquivo", command= abrir_arquivo)
btn_abrir.pack(pady=10)

# Rótulo para mostrar o resultado
lbl_palavras = tk.Label(root, text= "Total de palavras: ")
lbl_palavras.pack(pady=5)

lbl_caracteres = tk.Label(root, text= "Total de caracteres: ")
lbl_caracteres.pack(pady=5)

root.mainloop()
