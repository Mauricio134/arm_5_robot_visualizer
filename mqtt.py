import paho.mqtt.client as mqtt
import time
import json
from datetime import datetime

class MQTTClient:
    def __init__(self, broker_host, broker_port=1883):
        self.broker_host = broker_host
        self.broker_port = broker_port
        self.client = mqtt.Client()
        
        # Configurar callbacks
        self.client.on_connect = self.on_connect
        self.client.on_publish = self.on_publish
        self.client.on_disconnect = self.on_disconnect
        
    def on_connect(self, client, userdata, flags, rc):
        if rc == 0:
            print(f"✅ Conectado al broker MQTT en {self.broker_host}:{self.broker_port}")
        else:
            print(f"❌ Error al conectar. Código: {rc}")
    
    def on_publish(self, client, userdata, mid):
        print(f"📤 Mensaje publicado con ID: {mid}")
    
    def on_disconnect(self, client, userdata, rc):
        print(f"🔌 Desconectado del broker. Código: {rc}")
    
    def connect(self):
        try:
            self.client.connect(self.broker_host, self.broker_port, 60)
            self.client.loop_start()
            return True
        except Exception as e:
            print(f"❌ Error de conexión: {e}")
            return False
    
    def send_message(self, topic, message):
        try:
            # Crear payload con timestamp
            payload = {
                "message": message,
                "timestamp": datetime.now().isoformat(),
                "source": "Python Client"
            }
            
            result = self.client.publish(topic, json.dumps(payload))
            
            if result.rc == mqtt.MQTT_ERR_SUCCESS:
                print(f"✉️  Mensaje enviado al topic '{topic}': {message}")
            else:
                print(f"❌ Error al enviar mensaje: {result.rc}")
                
        except Exception as e:
            print(f"❌ Error al publicar: {e}")
    
    def disconnect(self):
        self.client.loop_stop()
        self.client.disconnect()

def main():
    # Configuración - CAMBIAR por la IP de tu celular
    BROKER_IP = "172.18.3.235"  # IP de tu celular
    TOPIC = "test/messages"
    
    print("🚀 Iniciando cliente MQTT...")
    
    # Crear cliente
    mqtt_client = MQTTClient(BROKER_IP)
    
    # Conectar
    if mqtt_client.connect():
        time.sleep(2)  # Esperar conexión
        
        try:
            # Enviar mensajes de prueba
            messages = [
                "¡Hola desde Python!",
                "Mensaje de prueba #2",
                "Conexión MQTT funcionando correctamente",
                "Este es el último mensaje de prueba"
            ]
            
            for i, msg in enumerate(messages, 1):
                print(f"\n--- Enviando mensaje {i}/{len(messages)} ---")
                mqtt_client.send_message(TOPIC, msg)
                time.sleep(3)  # Esperar entre mensajes
                
        except KeyboardInterrupt:
            print("\n⚠️  Interrupción por usuario")
        
        finally:
            print("\n🔚 Cerrando conexión...")
            mqtt_client.disconnect()
    
    else:
        print("❌ No se pudo establecer conexión con el broker")

if __name__ == "__main__":
    main()