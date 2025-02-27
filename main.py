import network
import urequests
import utime
from machine import ADC


WIFI_NOMBRE = "redpivada"
WIFI_CLAVE = "privado"
CANAL_THINGSPEAK_ID = "privado"
API_THINGSPEAK_CLAVE = "privado"
URL_THINGSPEAK = f"https://api.thingspeak.com/update?api_key={API_THINGSPEAK_CLAVE}"

def conectar_wifi():
    conexion = network.WLAN(network.STA_IF)
    conexion.active(True)
    conexion.connect(WIFI_NOMBRE, WIFI_CLAVE)
    while not conexion.isconnected():
        print("Intentando conexión Wi-Fi...")
        utime.sleep(1)
    print("Conexión Wi-Fi establecida! Dirección IP:", conexion.ifconfig()[0])


def obtener_temperatura():
    sensor_interno = ADC(4) 
    factor_conversion = 3.3 / 65535  
    lectura = sensor_interno.read_u16() * factor_conversion  
    temperatura_celsius = 27 - (lectura - 0.706) / 0.001721  
    return round(temperatura_celsius, 2)


def enviar_a_thingspeak(temperatura):
    parametros = f"&field1={temperatura}"
    respuesta = urequests.get(URL_THINGSPEAK + parametros)
    print("Datos enviados a ThingSpeak: ", respuesta.text)
    respuesta.close()


conectar_wifi()
while True:
    temp_actual = obtener_temperatura()
    print(f"Temperatura actual: {temp_actual} °C")
    enviar_a_thingspeak(temp_actual)
    utime.sleep(180)  # Espera de 180 segundos
s