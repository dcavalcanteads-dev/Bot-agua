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

class DummyHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-type", "text/plain; charset=utf-8")
        self.end_headers()
        self.wfile.write(b"Bot de Agua Rodando!")

    def log_message(self, format, *args):
        return  # Silencia logs das requisições HTTP do ping

def enviar_mensagem():
    if not TOKEN or not CHAT_ID:
        print("❌ ERRO: Variáveis TOKEN ou CHAT_ID não encontradas no ambiente!")
        return

    mensagem = "💧 **Hora de beber água!** Mantenha-se hidratado."
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    payload = {"chat_id": CHAT_ID, "text": mensagem, "parse_mode": "Markdown"}
    
    try:
        response = requests.post(url, data=payload, timeout=10)
        if response.status_code == 200:
            print("✅ Mensagem enviada com sucesso!")
        else:
            print(f"⚠️ Erro ao enviar (Status {response.status_code}): {response.text}")
    except Exception as e:
        print(f"❌ Exceção ao tentar enviar: {e}")

def loop_bot():
    print("💧 Robô de hidratação iniciado em background!")
    while True:
        try:
            enviar_mensagem()
        except Exception as e:
            print(f"❌ Erro inesperado no loop: {e}")
        time.sleep(INTERVALO_MINUTOS * 60)

if __name__ == "__main__":
    # Inicia a rotina de envio do bot em um thread separado
    bot_thread = threading.Thread(target=loop_bot, daemon=True)
    bot_thread.start()

    # Mantém o servidor HTTP no processo principal para garantir a porta aberta no Render
    port = int(os.getenv("PORT", 8080))
    print(f"🚀 Servidor HTTP iniciado na porta {port}")
    server = HTTPServer(("0.0.0.0", port), DummyHandler)
    server.serve_forever()