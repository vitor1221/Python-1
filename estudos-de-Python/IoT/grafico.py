import sqlite3
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import tkinter as tk

# Conectar ao banco de dados SQLite
conn = sqlite3.connect('seu_banco_de_dados.db')
cursor = conn.cursor()

# Recuperar dados do banco de dados
cursor.execute("SELECT coluna_x, coluna_y FROM sua_tabela")
dados = cursor.fetchall()

# Processar os dados
x = [linha[0] for linha in dados]
y = [linha[1] for linha in dados]

# Criar a interface gráfica com Tkinter
root = tk.Tk()
root.title("Gráfico do SQLite com Tkinter")

# Criar o gráfico com matplotlib
fig, ax = plt.subplots()
ax.plot(x, y)

# Integrar o gráfico na interface Tkinter
canvas = FigureCanvasTkAgg(fig, master=root)
canvas.draw()
canvas.get_tk_widget().pack()

# Iniciar o loop principal do Tkinter
root.mainloop()

# Fechar a conexão com o banco de dados
conn.close()