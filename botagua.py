import os
import time
import requests
from dotenv import load_dotenv

# Carrega as variáveis secretas do arquivo .env
load_dotenv()

# Credenciais lidas do ambiente (.env)
TOKEN = os.getenv("TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

# Escolha o intervalo (ex: 15 ou 20 minutos)
INTERVALO_MINUTOS = 20  

def enviar_aviso_telegram(mensagem):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    dados = {"chat_id": CHAT_ID, "text": mensagem, "parse_mode": "Markdown"}
    try:
        resposta = requests.post(url, data=dados)
        if resposta.status_code == 200:
            print("✅ Lembrete enviado com sucesso no Telegram!")
        else:
            print(f"❌ Erro ao enviar. Verifique o Token ou o Chat ID. Código: {resposta.status_code}")
    except Exception as e:
        print(f"❌ Erro de conexão: {e}")

print("💧 Robô de hidratação iniciado na nuvem!")
print(f"⏰ Você será avisado a cada {INTERVALO_MINUTOS} minutos.")

try:
    while True:
        print(f"Aguardando {INTERVALO_MINUTOS} minutos...")
        # Dorme pelo tempo escolhido (minutos convertidos em segundos)
        time.sleep(INTERVALO_MINUTOS * 60)
        
        # Dispara a mensagem
        mensagem = "💧 *Hora de beber água!* Dê uma pausa rápida e hidrate-se!"
        enviar_aviso_telegram(mensagem)

except KeyboardInterrupt:
    print("🛑 Robô de água encerrado.")