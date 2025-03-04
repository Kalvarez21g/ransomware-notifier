import requests
from bs4 import BeautifulSoup
import re
import time


URL = 'https://www.ransomware.live/map/ES'

expected_title_pattern = r'(\d+)\s+Ransomware victims from Spain'

last_known_number = None

TELEGRAM_TOKEN = 'yourtoken' 
TELEGRAM_CHAT_ID = 'yourId' 

def send_telegram_message(message):
    """
    Envía un mensaje al grupo de Telegram configurado.
    """
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {
        'chat_id': TELEGRAM_CHAT_ID,
        'text': message
    }
    try:
        response = requests.post(url, json=payload)
        if response.status_code == 200:
            print("📩 Mensaje enviado por Telegram.")
        else:
            print(f"⚠️ Error al enviar mensaje por Telegram: {response.status_code}")
    except Exception as e:
        print(f"❌ Error al enviar mensaje por Telegram: {e}")

def check_title_change():
    """
    Comprueba cambios en la página web monitoreada.
    """
    global last_known_number
    try:

        response = requests.get(URL, timeout=10)
        if response.status_code == 200:
            print("✅ Conexión exitosa a la página web.")
        else:
            print(f"⚠️ Advertencia: Código de estado HTTP {response.status_code}")
            return

        soup = BeautifulSoup(response.text, 'html.parser')
        titles = soup.find_all(string=re.compile(expected_title_pattern, re.IGNORECASE))

        for title in titles:
            match = re.search(expected_title_pattern, title)
            if match:
                current_number = int(match.group(1))
                if last_known_number is None:
                    last_known_number = current_number
                    print(f"🔍 Número inicial detectado: {current_number}")
                elif current_number != last_known_number:
                    print(f"📈 Cambio detectado: {last_known_number} ➡️ {current_number}")
                    message = f"🔔 Nuevo ataque registrado en la página monitoreada (España): {last_known_number} ➡️ {current_number}."
                    send_telegram_message(message)
                    last_known_number = current_number
                else:
                    print("🔄 Sin cambios detectados.")
    except Exception as e:
        print(f"❌ Error al comprobar la página: {e}")

send_telegram_message("🤖 Ransomware Notifier está activo y monitoreando cambios...")

while True:
    check_title_change()
    time.sleep(60)
