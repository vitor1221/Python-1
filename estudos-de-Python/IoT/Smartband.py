# Sensor de Temperatura: LM35 (Texas Instruments) [-55°C -> 150°C] |Precisão razoavel, Baixo consumo de energia e Possui uma saída analógica proporcional à temperatura medida, facilitando a integração com microcontroladores|                                                                               
# Frequência Cardíaca (HR): GE Healthcare MAC 5500 HD [0BPM -> 240BPM] |Sensor utilizado em ambientes clínicos|                                                                                                                                                                                                
# Acelerômetro: MPU-6050 (InvenSense) [-16g -> 16g] |Quedas estão frequentemente na faixa de 4g a 10g ou mais & Amplamente utilizado em wearables para detecção de movimento e queda|                                                                                                                          
# Giroscópio: MPU-6050 (InvenSense) [-2000°/s -> 2000°/s] |Para movimentos rápidos como esportes de ação uma faixa de ±2000°/s a ±4000°/s é necessária para capturar toda a dinâmica do movimento|                                                                                                             
# Sensor de SpO2 (Saturação de Oxigênio): Texas Instruments AFE4400 [70% a 100%] |Utilizado em aplicações médicas e de monitoramento contínuo de pacientes. Utiliado no aplle watch|                                                                                                                           
# Sensor de Eletrodermal (EDA): ADS1299 (TexasInstruments) [-2.5mV -> 2.5mV] |Alta precisão, Baixo consumo de energia e  interface de comunicação flexível, incluindo SPI, o que facilita a integração com microcontroladores e outros dispositivos|                                                           
# Sensor de Luz Ambiente: APDS-9301 (Broadcom agora Avago Technologies) [0lux(ambiente escuro) -> 100.000lux(luz solar direta)] |Precisão Nescessaria, Baixo consumo de energia e  interface de comunicação flexível, incluindo IC2, o que facilita a integração com microcontroladores e outros dispositivos| 
# Sensor de Glicose: Dexcom G6 [-10% -> 10%]

import random
import socket
import time
import json
import tkinter as tk
from tkinter import ttk

class SmartBand:
    def __init__(self, server_ip="127.0.0.1", server_port=5000):
        self.sensors = {
            "Temperature Sensor (LM35)": {"min": -55, "max": 150, "unit": "°C"},
            "Heart Rate (HR) Sensor (GE Healthcare MAC 5500 HD)": {"min": 0, "max": 240, "unit": "BPM"},
            "Accelerometer (MPU-6050)": {"min": -16, "max": 16, "unit": "g"},
            "Gyroscope (MPU-6050)": {"min": -2000, "max": 2000, "unit": "°/s"},
            "SpO2 Sensor (Texas Instruments AFE4400)": {"min": 70, "max": 100, "unit": "%"},
            "Electrodermal Activity (EDA) Sensor (ADS1299)": {"min": -2.5, "max": 2.5, "unit": "mV"},
            "Ambient Light Sensor (APDS-9301)": {"min": 0, "max": 100000, "unit": "lux"},
            "Glucose Sensor (Dexcom G6)": {"min": -10, "max": 10, "unit": "%"}
        }
        self.server_ip = server_ip
        self.server_port = server_port
        self.root = tk.Tk()
        self.root.title("SmartBand - Dados Enviados")
        self.tree = ttk.Treeview(self.root, columns=("Valor", "Unidade"), show="headings")
        self.tree.heading("Valor", text="Valor")
        self.tree.heading("Unidade", text="Unidade")
        self.tree.pack(expand=True, fill=tk.BOTH)
        self.setup_connection()

    def setup_connection(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((self.server_ip, self.server_port))
        print("Conectado ao servidor do dispositivo.")

    def generate_sensor_data(self):
        sensor_data = {}
        for sensor_name, sensor_info in self.sensors.items():
            sensor_data[sensor_name] = round(random.uniform(sensor_info["min"], sensor_info["max"]), 2)
        return sensor_data

    def update_display(self, data):
        for item in self.tree.get_children():
            self.tree.delete(item)
        for sensor, value in data.items():
            unit = self.sensors[sensor]["unit"]
            self.tree.insert("", "end", values=(value, unit))

    def send_data(self):
        try:
            while True:
                sensor_data = self.generate_sensor_data()
                message = json.dumps(sensor_data)
                self.sock.sendall(message.encode('utf-8'))
                #print("Dados enviados:", sensor_data)
                self.update_display(sensor_data)
                self.root.update()
                time.sleep(2)
        except KeyboardInterrupt:
            print("Conexão finalizada pelo usuário.")
        except Exception as e:
            print(f"Erro na transmissão: {e}")

    def run(self):
        self.root.after(0, self.send_data)
        self.root.mainloop()

if __name__ == "__main__":
    smartband = SmartBand()
    smartband.run()
