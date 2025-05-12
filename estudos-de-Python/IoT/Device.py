import socket
import json
import tkinter as tk
from datetime import datetime

class Device:
    def __init__(self, host="127.0.0.1", port=5000, log_file="sensor_data_log.txt"):
        self.host = host
        self.port = port
        self.log_file = log_file
        self.root = tk.Tk()
        self.root.title("Device - Últimos Dados Recebidos")

        # Configura a exibição da última mensagem completa recebida
        self.label = tk.Label(self.root, text="Última mensagem recebida:", font=("Arial", 12, "bold"))
        self.label.pack(pady=10)
        
        # Área de texto para mostrar a última mensagem recebida
        self.text_display = tk.Text(self.root, height=15, width=60, wrap=tk.WORD, font=("Arial", 10))
        self.text_display.pack(padx=20, pady=10)
        self.text_display.config(state=tk.DISABLED)  # Desativa a edição pelo usuário

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
        }

    def log_data(self, data):
        # Registra a mensagem recebida com data e hora em um arquivo de log
        with open(self.log_file, "a") as file:
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            file.write(f"\n--- Dados Recebidos em {timestamp} ---\n")
            for sensor, value in data.items():
                unit = self.units.get(sensor, "")
                file.write(f"{sensor}: {value} {unit}\n")
            file.write("\n")  # Adiciona uma linha em branco entre registros

    def update_display(self, data):
        # Cria uma string formatada com valores e unidades
        formatted_message = "Dados Recebidos:\n\n"
        for sensor, value in data.items():
            unit = self.units.get(sensor, "")  # Obtém a unidade correspondente ou "" se não houver
            formatted_message += f"{sensor}: {value} {unit}\n"
        
        # Atualiza o campo de texto com a mensagem formatada
        self.text_display.config(state=tk.NORMAL)
        self.text_display.delete("1.0", tk.END)
        self.text_display.insert(tk.END, formatted_message)
        self.text_display.config(state=tk.DISABLED)

    def start_server(self):
        # Configura o servidor para receber dados
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_sock:
            server_sock.bind((self.host, self.port))
            server_sock.listen()
            #print(f"Servidor do dispositivo iniciado em {self.host}:{self.port}")
            conn, addr = server_sock.accept()
            print(f"Conexão estabelecida com: {addr}")

            with conn:
                while True:
                    data = conn.recv(1024)
                    if not data:
                        break
                    # Decodifica e exibe a última mensagem recebida
                    sensor_data = json.loads(data.decode('utf-8'))
                    print("Dados recebidos dos sensores:", sensor_data)
                    self.update_display(sensor_data)
                    self.log_data(sensor_data)  # Escreve os dados recebidos no arquivo de log
                    self.root.update()

    def run(self):
        self.root.after(0, self.start_server)
        self.root.mainloop()

if __name__ == "__main__":
    device = Device()
    device.run()
