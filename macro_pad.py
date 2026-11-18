
import os
import time
import webbrowser
import logging
import serial
from serial.tools import list_ports
import pyautogui


# CONFIGURAÇÕES DO MACROPAD
NOME_PROJETO = "MacroPad"

BAUD_RATE = 9600
TEMPO_RECONEXAO = 2

GITHUB_REPOSITORIO = ("https://github.com/PEUENG/PEUENGMACROPAD")

VIDS_ARDUINO = {0x2341, 0x2A03, 0x1A86, 0x10C4}

# CONFIGURAÇÃO DE LOG
PASTA_LOG = os.path.join(
    os.environ.get("LOCALAPPDATA", os.path.expanduser("~")),
    NOME_PROJETO
)

os.makedirs(PASTA_LOG, exist_ok=True)

ARQUIVO_LOG = os.path.join(PASTA_LOG,"status.log")

logging.basicConfig(filename=ARQUIVO_LOG,level=logging.INFO,format="%(asctime)s - %(levelname)s - %(message)s",encoding="utf-8")

pyautogui.PAUSE = 0.05
# FUNÇÕES DOS BOTÕES
def executar_acao(comando):

    try:
        if comando == "1":
            print("Botão 1: f13")
            pyautogui.press("f13")

        elif comando == "2":
            print("Botão 2: f14")
            pyautogui.press("f14")

        elif comando == "3":
            print("Botão 3: f15")
            pyautogui.press("f15")

        elif comando == "4":
            print("Botão 4: f16")
            pyautogui.press("f16")

        elif comando == "5":
            print("Botão 5: f17")
            pyautogui.press("f17")

        else:
            logging.warning(f"Comando desconhecido: {comando}")

    except Exception as erro:
        print(f"Erro ao executar ação: {erro}")
        logging.error(f"Erro na ação {comando}: {erro}")

# DETECÇÃO DO ARDUINO
def detectar_arduino():

    portas = list_ports.comports()

    for porta in portas:

        descricao = ((porta.description or "") + " " + (porta.manufacturer or "") + " " + (porta.product or "")).lower()

        vid = porta.vid
        reconhecido = (vid in VIDS_ARDUINO if vid is not None else False)

        palavras_chave = ["arduino","ch340","usb serial","cp210"]
        if reconhecido or any(palavra in descricao for palavra in palavras_chave):
            return porta.device
    return None

# CONEXÃO SERIAL
def conectar_arduino():
    porta = detectar_arduino()
    if porta is None:
        return None

    try:
        conexao = serial.Serial(port=porta,baudrate=BAUD_RATE,timeout=1)
        time.sleep(2)
        conexao.reset_input_buffer()
        print(f"Arduino conectado na porta {porta}")
        logging.info(f"Arduino conectado na porta {porta}")
        return conexao

    except serial.SerialException as erro:
        print(f"Erro ao conectar: {erro}")
        logging.error(f"Erro de conexão: {erro}")
        return None

# PROGRAMA PRINCIPAL
def iniciar_macropad():
    print("MACROPAD INICIADO")
    logging.info("MacroPad iniciado")
    conexao = None

    try:
        while True:
            # Tenta conectar ao Arduino
            if conexao is None:
                print("Procurando Arduino...")
                conexao = conectar_arduino()
                if conexao is None:
                    time.sleep(TEMPO_RECONEXAO)
                    continue

            try:
                # Lê os comandos enviados pelo Arduino
                if conexao.in_waiting > 0:
                    comando = (conexao.readline().decode("utf-8", errors="ignore").strip())
                    if comando:
                        executar_acao(comando)

            except (
                serial.SerialException,
                OSError
            ) as erro:
                print("Arduino desconectado!")
                logging.error(
                    f"Conexão perdida: {erro}"
                )
                try:
                    conexao.close()
                except Exception:
                    pass
                conexao = None
                time.sleep(TEMPO_RECONEXAO)

    except KeyboardInterrupt:
        print("\nEncerrando MacroPad...")
        logging.info("MacroPad encerrado pelo usuário")

    finally:
        if conexao is not None:
            try:
                conexao.close()
            except Exception:
                pass
        print("MacroPad encerrado.")

if __name__ == "__main__":
    iniciar_macropad()