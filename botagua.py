import os
import time
import threading
import requests
from http.server import HTTPServer, BaseHTTPRequestHandler
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("TOKEN")
CHAT_ID = os.getenv("CHAT_ID")
INTERVALO_MINUTOS = 20

# Servidor HTTP básico para o Render entender que o Web Service está ativo
class DummyHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"Bot de Agua Rodando!")

    def log_message(self, format, *args):
        return  # Silencia os logs do servidor HTTP

def rodar_servidor():
    port = int(os.getenv("PORT", 8080))
    server = HTTPServer(("0.0.0.0", port), DummyHandler)
    server.serve_forever()

def enviar_mensagem():
    mensagem = "💧 **Hora de beber água!** Mantenha-se hidratado."
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    payload = {"chat_id": CHAT_ID, "text": mensagem, "parse_mode": "Markdown"}
    
    try:
        response = requests.post(url, data=payload)
        if response.status_code == 200:
            print("Mensagem enviada com sucesso!")
        else:
            print(f"Erro ao enviar: {response.text}")
    except Exception as e:
        print(f"Exceção ao tentar enviar: {e}")

def loop_bot():
    print("💧 Robô de hidratação iniciado na nuvem!")
    while True:
        enviar_mensagem()
        time.sleep(INTERVALO_MINUTOS * 60)

if __name__ == "__main__":
    # Inicia o servidor HTTP em segundo plano
    threading.Thread(target=rodar_servidor, daemon=True).start()
    # Inicia o loop principal do bot
    loop_bot()