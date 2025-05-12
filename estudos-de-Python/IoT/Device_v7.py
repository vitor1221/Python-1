import socket                   # Importa a biblioteca 'socket' para configurar comunicação de rede.
import json                     # Importa 'json' para decodificar mensagens em formato JSON.
import tkinter as tk            # Importa 'tkinter' para criar a interface gráfica.
from datetime import datetime   # Importa 'datetime' para registrar a data e hora dos dados recebidos.
import sqlite3                  # Importa 'sqlite3' para trabalhar com banco de dados SQLite.
import re                       # Importa 're' para trabalhar com expressões regulares.
import threading                # Importa 'threading' para rodar o servidor em paralelo.

# Constantes para arquivos
DB_FILE = "logs.db"
LOG_FILE = "sensor_data_log.txt"
TEMP_LOGER = 60                   

class Device:
    def __init__(self, host="127.0.0.1", port=5000, log_file=LOG_FILE):
        # Define os atributos básicos do dispositivo
        self.host = host                                    # Endereço IP onde o servidor escutará.
        self.port = port                                    # Porta onde o servidor escutará.
        self.log_file = log_file                            # Arquivo onde os dados recebidos serão salvos.
        self.last_data = {}                                 # Inicializa o dicionário para armazenar os dados anteriores.
        self.server_running = False                        # Controle do estado do servidor.

        # Interface Gráfica
        self.root = tk.Tk()                                 # Cria a janela principal do Tkinter.
        self.root.title("Device - Dados Recebidos")         # Define o título da janela.

        # Configura a exibição da última mensagem completa recebida
        self.label = tk.Label(self.root, text="DADOS RECEBIDOS [DEVICE]:", font=("Arial", 12, "bold"))
        self.label.pack(pady=5)                            # Adiciona espaço acima e abaixo do rótulo para estética.
        
        # Área de texto para mostrar a última mensagem recebida
        self.text_display = tk.Text(self.root, height=15, width=130, wrap=tk.WORD, font=("Arial", 10))
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

        # Variável para armazenar dados momentâneos
        self.temp_data = {}

    def log_data(self, data):
        """
        Registra os dados recebidos em um arquivo de log.
        """
        with open(self.log_file, "a") as log_file:  # Abre o arquivo de log no modo append.
            log_file.write(f"{datetime.now()} - {json.dumps(data)}\n")  # Escreve os dados com o timestamp.

    def temperature_values_check(self,temperature):
        if 37.5 <= temperature < 40:
            return "[ATENCAO]Possivel febre detectada, podendo indicar ferida infeccionada!"
        elif 40 <= temperature < 42:
            return "[ATENCAO]Possivel hipertemia grave detectada, podendo estar compromentendo as funcoes cerebrais e outros orgaos!"
        elif temperature >= 42:
            return "[ATENCAO]Possivel temperatura critica detectada, suas proteinas do corpo podem estar comecando a se desnaturar e as funcoes vitais podem falhar!"
        elif temperature < 35:
            return "[ATENCAO]Possivel hipotermia detectada, podendo indicar sintomas como tremores, confusao mental e compromentimento das funcoes vitais!"
        elif temperature < 28:
            return "[ATENCAO]Possivel hipotermia critica detectada, podendo idicar um grnade risco de falenciados orgaos e morte!"
        
    #PEDIR IDADE DA PESSOA?
    def heart_rate_values_check(self,HR):
        if HR < 50:
            return "[ATENCAO]Possivel bradicardia detectada, podendo indicar sintomas como tontura, fadiga ou desmaio!"
        elif HR > 100:
            return "[ATENCAO]Possivel taquicardia detectada caso esteja em descanso, podendo ser fatal se não tratado rapidamente!"
        #elif HR = 220 - age: 
        #   return "[ATENCAO]Possivel taquicardia detectada, podendo ser fatal se não tratado rapidamente!"

    def gyroscope_values_check(self,gyro):
        if gyro > 100:
            return "[ATENCAO]Possivel queda detectada!"
        
    def oxigen_rate_values_check(self,spo2):
        if 90 <= spo2 <= 94:
            return "[ATENCAO]Possivel hipoxemia leve detectada, podendo indicar um inicio de doença respiratoria ou a baixa pressao de oxigenio!"
        elif 85 <= spo2 < 90:
            return "[ATENCAO]Possivel hipoxemia moderada detectada, podendo indicar sinais de deficiencia significativa de oxigenio!"
        elif spo2 < 85:
            return "[ATENCAO]Possivel hipoxemia severa detectada, podendo indicar niveis perigosos de oxigenio levando a insuficiencia de orgaos ou morte sem tratamento imediato!" 

    def electrodermal_activity_values_check(self,electodermal):
        if -0.5 <= electodermal <= 0.5:
            return "[AVISO]Possivel estado emocional de calma ou repouso detectado."
        elif 0.5 < electodermal <= 2.5:
            return "[AVISO]Possivel alterações no seu estado emocional detectado, como estresse ou excitacao."
        
    def ambient_light_rate_values_check(self,ambientLight):
        if ambientLight > 10000:
            return "[ATENCAO]Possivel limite para exposicao a luz prolongada sem causar ou causando desconforto significativo detectada!"
        elif ambientLight < 10:
            return "[ATENCAO]Possivel iluminacao muito escura detectada, podendo causar desconforto visual, dificultar tarefas e aumentar o cansaço ocular!"
        
    def glucose_value_check(self,glucose):
        if glucose < 0.004:
            return "[ATENCAO]Possivel quantidade de glicose muito baixa detectada, podendo causar falha do cérebro em obter energia suficiente!"
        elif glucose > 0.06:
            return "[ATENCAO]Possivel sindrome hiperglicemica hiperosmolar detectada, podendo causar coma ou morte!"

    def update_display(self, data):
        """
        Atualiza a tela com dados novos, alterados e inalterados.
        Limpa a tela e exibe todos os dados atualizados, incluindo mensagens de alerta.
        """
        formatted_message = ""      # Texto a ser adicionado.
        
        # Cria a lista de sensores para verificar o estado (novo, alterado, inalterado)
        for sensor, value in data.items():
            status_message = ""  # Variável para mensagem adicional (alerta).
            sensor_value = value['value']
            
            # Chamadas às funções de verificação de sinais vitais
            if sensor == "Temperature Sensor (LM35)":
                status_message = self.temperature_values_check(sensor_value)
            elif sensor == "Heart Rate (HR) Sensor (GE Healthcare MAC 5500 HD)":
                status_message = self.heart_rate_values_check(sensor_value)
            elif sensor == "Gyroscope (MPU-6050)":
                status_message = self.gyroscope_values_check(sensor_value)
            elif sensor == "SpO2 Sensor (Texas Instruments AFE4400)":
                status_message = self.oxigen_rate_values_check(sensor_value)
            elif sensor == "Electrodermal Activity (EDA) Sensor (ADS1299)":
                status_message = self.electrodermal_activity_values_check(sensor_value)
            elif sensor == "Ambient Light Sensor (APDS-9301)":
                status_message = self.ambient_light_rate_values_check(sensor_value)
            elif sensor == "Glucose Sensor (Dexcom G6)":
                status_message = self.glucose_value_check(sensor_value)
            
            # Formatação da mensagem a ser exibida
            if sensor not in self.last_data:  # Novo dado
                formatted_message += f"[NOVO] {sensor}: {sensor_value} {self.units.get(sensor, '')}\n"
                self.last_data[sensor] = sensor_value
            elif self.last_data[sensor] != sensor_value:  # Valor alterado
                formatted_message += f"[ALTERADO] {sensor}: {sensor_value} {self.units.get(sensor, '')}\n"
                self.last_data[sensor] = sensor_value
            else:  # Dados inalterados
                formatted_message += f"[INALTERADO] {sensor}: {self.last_data[sensor]} {self.units.get(sensor, '')}\n"
            
            # Adiciona a mensagem de alerta, se houver
            if status_message:
                formatted_message += f"   {status_message}\n"

        # Limpa a área de texto e exibe a nova mensagem formatada
        self.text_display.config(state=tk.NORMAL)         # Permite edição temporária.
        self.text_display.delete(1.0, tk.END)             # Limpa o conteúdo atual da área de texto.
        self.text_display.insert(tk.END, formatted_message)  # Adiciona os dados ao final.
        self.text_display.config(state=tk.DISABLED)       # Desativa edição novamente.


    def process_log_and_create_db(self, log_file, db_file):
        """
        Processa um arquivo de log, extrai os dados e os insere em um banco de dados SQLite.
        """
        # Conectar ao banco de dados SQLite
        conn = sqlite3.connect(db_file)
        cursor = conn.cursor()

        # Criar a tabela de logs se não existir
        cursor.execute(""" 
            CREATE TABLE IF NOT EXISTS logs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT,
                sensor TEXT,
                status TEXT,
                value REAL
            )
        """)

        # Processar o arquivo de log
        with open(log_file, "r") as file:
            for line in file:
                try:
                    # Dividir timestamp e dados em JSON
                    timestamp, json_data = line.split(" - ", 1)
                    sensor_data = json.loads(json_data)

                    # Inserir dados no banco
                    for sensor, details in sensor_data.items():
                        status = details.get("status", "")
                        value = details.get("value", 0.0)
                        cursor.execute(
                            "INSERT INTO logs (timestamp, sensor, status, value) VALUES (?, ?, ?, ?)",
                            (timestamp, sensor, status, value)
                        )
                except Exception as e:
                    print(f"Erro ao processar linha do log: {line.strip()}\n{e}")

        # Salvar e fechar conexão
        conn.commit()
        conn.close()
        print(f"Banco de dados '{db_file}' criado e preenchido com sucesso!")

    def process_data(self, data):
        """
        Processa os dados recebidos: atualiza a interface gráfica
        com os dados alterados, novos e inalterados e registra no log.
        """
        self.update_display(data)  # Atualiza a interface gráfica com todos os dados
        self.temp_data = data      # Armazena os dados momentâneos

    def schedule_log(self):
        """
        Função que registra os dados momentâneos periodicamente a cada TEMP_LOGER segundos.
        """
        if self.temp_data:  # Se houver dados para registrar
            self.log_data(self.temp_data)
            print(f"Dados momentâneos registrados: {self.temp_data}")
        self.root.after(TEMP_LOGER * 1000, self.schedule_log)  # Chama a função novamente após TEMP_LOGER segundos.

    def start_server(self):
        self.server_running = True
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_sock:
            self.server_sock = server_sock
            server_sock.bind((self.host, self.port))
            server_sock.listen()
            while self.server_running:
                try:
                    conn, addr = server_sock.accept()
                    print(f"Conexão estabelecida com: {addr}")
                    with conn:
                        while self.server_running:
                            data = conn.recv(1024)
                            if not data:
                                break
                            sensor_data = json.loads(data.decode('utf-8'))
                            self.process_data(sensor_data)
                except Exception as e:
                    print(f"Erro no servidor: {e}")
    
    def run_server_in_thread(self):
        server_thread = threading.Thread(target=self.start_server, daemon=True)
        server_thread.start()

    def on_close(self):
        self.server_running = False
        if hasattr(self, 'server_sock'):
            self.server_sock.close()
        self.process_log_and_create_db(self.log_file, DB_FILE)  # Processa o log ao encerrar.
        self.root.destroy()

    def run(self):
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)
        self.run_server_in_thread()
        self.schedule_log()  # Inicia o temporizador para registrar dados.
        self.root.mainloop()

if __name__ == "__main__":
    device = Device()
    device.run()
