import socket                   # Importa a biblioteca 'socket' para configurar comunicação de rede.
import json                     # Importa 'json' para decodificar mensagens em formato JSON.
import tkinter as tk            # Importa 'tkinter' para criar a interface gráfica.
from datetime import datetime   # Importa 'datetime' para registrar a data e hora dos dados recebidos.
from tkinter.scrolledtext import ScrolledText

class Device:
    def __init__(self, host="127.0.0.1", port=5000, log_file="sensor_data_log.txt"):
        # Define os atributos básicos do dispositivo
        self.host = host                                    # Endereço IP onde o servidor escutará.
        self.port = port                                    # Porta onde o servidor escutará.
        self.log_file = log_file                            # Arquivo onde os dados recebidos serão salvos.
        self.last_data = {}                                  # Inicializa o dicionário para armazenar os dados anteriores.
        self.root = tk.Tk()                                 # Cria a janela principal do Tkinter.
        self.root.title("Device - Dados Recebidos")         # Define o título da janela.

        # Configura a exibição da última mensagem completa recebida
        self.label = tk.Label(self.root, text="DADOS RECEBIDOS [DEVICE]:", font=("Arial", 12, "bold"))
        self.label.pack(pady=5)                            # Adiciona espaço acima e abaixo do rótulo para estética.
        
        # Área de texto para mostrar a última mensagem recebida
        self.text_display = tk.Text(self.root, height=10, width=70, wrap=tk.WORD, font=("Arial", 10))
        self.text_display.pack(padx=10, pady=10)            # Adiciona margem nas laterais e no topo/rodapé.
        self.text_display.config(state=tk.DISABLED)         # Desativa a edição pelo usuário.

        # Dicionário de unidades dos sensores
        self.units = {
            "Temperature Sensor (LM35)": "°C",
            "Heart Rate (HR) Sensor (GE Healthcare MAC 5500 HD)": "BPM",
            "Accelerometer (MPU-6050)": "g",
            "Gyroscope (MPU-6050)": "°/s",
            "SpO2 Sensor (Texas Instruments AFE4400)": "%",
            "Electrodermal Activity (EDA) Sensor (ADS1299)": "mV",
            "Ambient Light Sensor (APDS-9301)": "lux",
            "Glucose Sensor (Dexcom G6)": "%"
        }  # Define as unidades para cada sensor, para formatar os dados exibidos.

    def log_data(self, data):
        """
        Registra os dados recebidos em um arquivo de log.
        """
        with open(self.log_file, "a") as log_file:  # Abre o arquivo de log no modo append.
            log_file.write(f"{datetime.now()} - {json.dumps(data)}\n")  # Escreve os dados com o timestamp.

    def update_display(self, data):
        """
        Atualiza a tela com dados novos, alterados e inalterados.
        Limpa a tela e exibe todos os dados atualizados.
        """
        formatted_message = ""      # Texto a ser adicionado.
        
        # Cria a lista de sensores para verificar o estado (novo, alterado, inalterado)
        for sensor, value in data.items():
            if sensor not in self.last_data:  # Novo dado
                formatted_message += f"[NOVO] {sensor}: {value['value']} {self.units.get(sensor, '')}\n"
                self.last_data[sensor] = value['value']
            elif self.last_data[sensor] != value['value']:  # Valor alterado
                formatted_message += f"[ALTERADO] {sensor}: {value['value']} {self.units.get(sensor, '')}\n"
                self.last_data[sensor] = value['value']
            else:  # Dados inalterados
                formatted_message += f"[INALTERADO] {sensor}: {self.last_data[sensor]} {self.units.get(sensor, '')}\n"

        # Limpa a área de texto e exibe a nova mensagem formatada
        self.text_display.config(state=tk.NORMAL)         # Permite edição temporária.
        self.text_display.delete(1.0, tk.END)             # Limpa o conteúdo atual da área de texto.
        self.text_display.insert(tk.END, formatted_message)  # Adiciona os dados ao final.
        self.text_display.config(state=tk.DISABLED)       # Desativa edição novamente.

    def process_data(self, data):
        """
        Processa os dados recebidos: atualiza a interface gráfica
        com os dados alterados, novos e inalterados e registra no log.
        """
        self.update_display(data)  # Atualiza a interface gráfica com todos os dados
        self.log_data(data)        # Registra os dados no log

    def start_server(self):
        # Configura o servidor para receber dados
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_sock:
            server_sock.bind((self.host, self.port))            # Associa o socket ao endereço e porta definidos.
            server_sock.listen()                                # Coloca o servidor em estado de escuta.
            conn, addr = server_sock.accept()                   # Aguarda uma conexão.
            print(f"Conexão estabelecida com: {addr}")          # Exibe mensagem de conexão no console.

            with conn:
                while True:
                    data = conn.recv(1024)                      # Recebe dados do cliente.
                    if not data:
                        break                                   # Encerra o loop se não houver dados.
                    sensor_data = json.loads(data.decode('utf-8'))  # Decodifica o JSON recebido.
                    self.process_data(sensor_data)              # Processa os dados recebidos.
                    self.root.update()                          # Atualiza a interface gráfica.

    def run(self):
        self.root.after(0, self.start_server)   # Agende `start_server` para rodar após o início da GUI.
        self.root.mainloop()                    # Inicia o loop principal da interface gráfica.

if __name__ == "__main__":
    device = Device()       # Cria uma instância da classe Device.
    device.run()            # Inicia o dispositivo e o servidor de monitoramento.
