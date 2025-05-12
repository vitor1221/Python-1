import sqlite3
import plotly.graph_objs as go
import plotly.io as pio
import tkinter as tk
from plotly.subplots import make_subplots

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

# Criar o gráfico com Plotly
fig = make_subplots(rows=1, cols=1)
fig.add_trace(go.Scatter(x=x, y=y, mode='lines', name='Dados'))

# Renderizar o gráfico como uma imagem estática
img_bytes = pio.to_image(fig, format='png')

# Exibir a imagem na interface Tkinter
img_label = tk.Label(root)
img_label.pack()
img = tk.PhotoImage(data=img_bytes)
img_label.config(image=img)
img_label.image = img

# Iniciar o loop principal do Tkinter
root.mainloop()

# Fechar a conexão com o banco de dados
conn.close()
