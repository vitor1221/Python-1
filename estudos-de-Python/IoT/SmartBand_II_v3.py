import random
import socket
import time
import json
import tkinter as tk
from tkinter import ttk
import statistics

class SmartBand:
    """
    Classe que representa a SmartBand, responsável por gerar, exibir e enviar dados de sensores para um servidor.
    """

    def __init__(self, server_ip="127.0.0.1", server_port=5000):
        """
        Inicializa a classe SmartBand com os parâmetros do servidor e configura a interface gráfica.

        :param server_ip: Endereço IP do servidor para enviar dados. Padrão: "127.0.0.1".
        :param server_port: Porta do servidor para enviar dados. Padrão: 5000.
        """
        self.sensors = {
            "Temperature Sensor (LM35)": {"min": 28, "max": 46, "unit": "°C", "std_dev": 1.0},
            "Heart Rate (HR) Sensor (GE Healthcare MAC 5500 HD)": {"min": 50, "max": 100, "unit": "BPM", "std_dev": 3.0},
            "Accelerometer (MPU-6050)": {"min": -16, "max": 16, "unit": "g", "std_dev": 1.0},
            "Gyroscope (MPU-6050)": {"min": 100, "max": 200, "unit": "°/s", "std_dev": 7.0},
            "SpO2 Sensor (Texas Instruments AFE4400)": {"min": 85, "max": 100, "unit": "%", "std_dev": 2.0},
            "Electrodermal Activity (EDA) Sensor (ADS1299)": {"min": -0.5, "max": 2.5, "unit": "mV", "std_dev": 0.2},
            "Ambient Light Sensor (APDS-9301)": {"min": 0, "max": 10000, "unit": "lux", "std_dev": 1000},
            "Glucose Sensor (Dexcom G6)": {"min": 0.004, "max": 0.02, "unit": "%", "std_dev": 0.5}
        }
        self.server_ip = server_ip
        self.server_port = server_port
        self.root = tk.Tk()
        self.root.title("SmartBand - Dados Enviados")
        # Configuração da interface gráfica
        self.tree = ttk.Treeview(self.root, columns=("Valor", "Unidade"), show="headings")
        self.tree.heading("Valor", text="Valor")
        self.tree.heading("Unidade", text="Unidade")
        self.tree.pack(expand=True, fill=tk.BOTH)
        self.setup_connection()
        self.last_data = {sensor: None for sensor in self.sensors.keys()}  # Armazena os dados anteriores

    def setup_connection(self):
        """
        Configura a conexão com o servidor usando sockets.
        """
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((self.server_ip, self.server_port))
        print("Conectado ao servidor do dispositivo.")

    def generate_sensor_data(self):
        """
        Gera dados aleatórios para os sensores configurados.

        :return: Um dicionário com os nomes dos sensores e seus valores gerados.
        """
        sensor_data = {}
        for sensor_name, sensor_info in self.sensors.items():
            sensor_data[sensor_name] = round(random.uniform(sensor_info["min"], sensor_info["max"]), 2)
        return sensor_data

    def classify_data(self, current_data):
        """
        Classifica os dados como [NOVO], [ALTERADO] ou [INALTERADO].

        :param current_data: Dicionário contendo os dados atuais dos sensores.
        :return: Dicionário com dados classificados.
        """
        classified_data = {}
        for sensor, value in current_data.items():
            if self.last_data[sensor] is None:  # Dados novos
                classified_data[sensor] = {"status": "[NOVO]", "value": value}
            elif self.last_data[sensor] != value:  # Dados alterados
                classified_data[sensor] = {"status": "[ALTERADO]", "value": value}
            else:  # Dados inalterados
                classified_data[sensor] = {"status": "[INALTERADO]", "value": value}
        
        # Atualiza os dados anteriores
        self.last_data = current_data
        return classified_data

    def send_data(self):
        """
        Coleta dados dos sensores, calcula a média a cada minuto e envia os resultados ao servidor.
        """
        collected_data = {sensor: [] for sensor in self.sensors.keys()}  # Inicializa armazenamento de dados
        start_time = time.time()

        try:
            while True:
                current_time = time.time()
                if current_time - start_time >= 5:  # 1 minuto - 5 seg para acelerar o teste
                    # Gera dados dos sensores e classifica-os
                    sensor_data = self.generate_sensor_data()
                    classified_data = self.classify_data(sensor_data)
                    
                    # Converte os dados classificados para envio
                    message = json.dumps(classified_data)
                    self.sock.sendall(message.encode('utf-8'))
                    self.update_display(classified_data)

                    # Reinicia os dados coletados e o cronômetro
                    collected_data = {sensor: [] for sensor in self.sensors.keys()}
                    start_time = current_time
                else:
                    # Adiciona novos dados ao buffer de coleta
                    sensor_data = self.generate_sensor_data()
                    for sensor, value in sensor_data.items():
                        collected_data[sensor].append(value)
                self.root.update()
                time.sleep(2)
        except KeyboardInterrupt:
            print("Conexão finalizada pelo usuário.")
        except Exception as e:
            print(f"Erro na transmissão: {e}")

    def update_display(self, data):
        """
        Atualiza a interface gráfica com os dados enviados.

        :param data: Dicionário contendo os dados a serem exibidos.
        """
        for item in self.tree.get_children():
            self.tree.delete(item)
        for sensor, info in data.items():
            self.tree.insert("", "end", values=(f"{info['status']} {info['value']}", self.sensors[sensor]["unit"]))

    def run(self):
        """
        Inicia o envio de dados e o loop principal da interface gráfica.
        """
        self.root.after(0, self.send_data)
        self.root.mainloop()

if __name__ == "__main__":
    smartband = SmartBand()
    smartband.run()
