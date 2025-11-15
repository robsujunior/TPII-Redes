import socket
import threading

# Configuração do servidor
HOST = '127.0.0.1'  # Endereço local
PORT = 61         # Porta de comunicação

# Função para lidar com cada cliente conectado
def handle_client(conn, addr):
    print(f"[NOVA CONEXÃO] Cliente conectado: {addr}")
    with conn:
        while True:
            try:
                msg = conn.recv(1024).decode('utf-8')
                if not msg:
                    print(f"[DESCONECTADO] Cliente {addr}")
                    break

                msg = msg.strip()
                if msg == "":
                    resposta = "Mensagem vazia não permitida."
                else:
                    print(f"[{addr}] Mensagem recebida: {msg}")
                    resposta = "Mensagem recebida."

                conn.sendall(resposta.encode('utf-8'))
            except ConnectionResetError:
                print(f"[ERRO] Conexão com {addr} foi encerrada inesperadamente.")
                break

# Inicialização do servidor
def main():
    servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    servidor.bind((HOST, PORT))
    servidor.listen()
    print(f"[SERVIDOR ATIVO] Escutando em {HOST}:{PORT}")

    try:
        while True:
            conn, addr = servidor.accept()
            thread = threading.Thread(target=handle_client, args=(conn, addr))
            thread.start()
    except KeyboardInterrupt:
        print("\n[ENCERRANDO] Servidor finalizado com segurança.")
    finally:
        servidor.close()

if __name__ == "__main__":
    main()
