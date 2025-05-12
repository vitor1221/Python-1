import tkinter as tk
from tkinter import messagebox
from datetime import datetime
from tkcalendar import DateEntry
from dateutil.relativedelta import relativedelta


def calcular_idade():
    try:
        data_de_nascimento = date_entry.get_date()  # Obtém a data selecionada
        data_atual = datetime.now()

        # Calcular a diferença exata dos dias
        difference = relativedelta(data_atual, data_de_nascimento)

        anos = difference.years
        meses = difference.months
        dias = difference.days

        # Exibição do resultado
        resultado = f"Idade: {anos} anos, {meses} meses, {dias} dias."
        messagebox.showinfo("Resultado: ", resultado)
    except ValueError:
        messagebox.showinfo('Erro!', 'Por favor, selecione uma data válida.')


# Criação da janela principal
window = tk.Tk()
window.title("Calculadora de Idade")

label_rotulo = tk.Label(window, text='Selecione sua data de nascimento: ')
label_rotulo.pack(pady=10)

date_entry = DateEntry(window, date_pattern='dd/mm/yyyy', background='white', foreground='darkblue', borderwidth=2)
date_entry.pack(pady=5)

btn_calcular_idade = tk.Button(window, text="Calcular", command=calcular_idade)
btn_calcular_idade.pack(pady=20)

# Executa o loop principal
window.mainloop()