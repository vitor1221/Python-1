import tkinter as tk
from tkinter import messagebox

# Função para validação de login
def validar_login():
    usuario = entry_usuario.get()
    senha = entry_senha.get()

    if usuario == "admin" and senha == "admin":
        messagebox.showinfo("Acesso permitido", "Usuário e senha corretos. Bem-vindo(a)!")
    else:
        messagebox.showinfo("Acesso negado", "Usuário e senha não conferem.")

# Configuração da janela principal
parent = tk.Tk()
parent.title("Autenticação de Login do Usuário")

# Criação dos widgets
label_usuario = tk.Label(parent, text="Usuário:")
label_usuario.pack()

entry_usuario = tk.Entry(parent)
entry_usuario.pack()

label_senha = tk.Label(parent, text="Senha:")
label_senha.pack()

entry_senha = tk.Entry(parent, show="*")
entry_senha.pack()

botao_entrar = tk.Button(parent, text="Entrar", command=validar_login)
botao_entrar.pack()

parent.mainloop()
