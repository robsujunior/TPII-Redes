import socket
import threading
from datetime import datetime

# Endereço e porta do servidor
HOST = "127.0.0.1"  # Servidor local
PORT = 8003          # Porta utilizada para fornecer a hora

def log(msg):
    """Função simples de log para exibir mensagens formatadas."""
    print(f"[LOG] {msg}")


def atender_cliente(conn, addr):
    """Thread responsável por atender um cliente individualmente.
    Recebe a solicitação e envia a hora atual.
    """
    log(f"Cliente conectado: {addr}")

    try:
        while True:
            # Recebe solicitação do cliente (até 1024 bytes)
            requisicao = conn.recv(1024)

            # Se nada for recebido, o cliente desconectou
            if not requisicao:
                break

            # Obtém a hora atual formatada
            hora_atual = datetime.now().strftime("%H:%M:%S")
            log(f"Solicitação de {addr} atendida com hora: {hora_atual}")

            # Envia a hora atual ao cliente
            conn.sendall(hora_atual.encode("utf-8"))

    except Exception as e:
        # Caso ocorra algum erro inesperado
        log(f"Erro com cliente {addr}: {e}")

    finally:
        # Fecha conexão com segurança
        log(f"Cliente desconectado: {addr}")
        conn.close()


def main():
    # Cria o socket TCP do servidor
    servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Associa o socket ao endereço e porta configurados
    servidor.bind((HOST, PORT))

    # Coloca o servidor em modo de escuta (aceita conexões)
    servidor.listen()

    log(f"Servidor de Hora ativo em {HOST}:{PORT}")

    while True:
        try:
            # Aguarda um cliente se conectar
            conn, addr = servidor.accept()

            # Cria e inicia uma thread para esse cliente
            thread = threading.Thread(target=atender_cliente, args=(conn, addr))
            thread.start()

        except Exception as e:
            # Caso ocorra erro geral no servidor
            log(f"Erro no servidor: {e}")


# Execução principal
if __name__ == "__main__":
    main()