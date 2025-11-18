#Participantes : Emanuel Guimarães, Robson Junior e Samuel Assunção

import socket
import threading

# Configuração do servidor
HOST = '127.0.0.1'  # Endereço local onde o servidor irá escutar
PORT = 8000         # Porta utilizada para a comunicação

# Função responsável por atender cada cliente conectado ao servidor
# "conn" é o objeto da conexão e "addr" o endereço do cliente

def handle_client(conn, addr):
    print(f"[NOVA CONEXÃO] Cliente conectado: {addr}")
    
    # 'with' garante fechamento automático da conexão ao final
    with conn:
        while True:
            try:
                # Recebe até 1024 bytes e decodifica para string
                msg = conn.recv(1024).decode('utf-8')

                # Se 'msg' for vazia, significa que o cliente desconectou
                if not msg:
                    print(f"[DESCONECTADO] Cliente {addr}")
                    break

                # Remove espaços extras
                msg = msg.strip()

                # Valida mensagem vazia
                if msg == "":
                    resposta = "Mensagem vazia não permitida."
                else:
                    print(f"[{addr}] Mensagem recebida: {msg}")
                    resposta = "Mensagem recebida."

                # Envia resposta ao cliente
                conn.sendall(resposta.encode('utf-8'))
            
            # Captura desconexões abruptas (exemplo: cliente fechou sem avisar)
            except ConnectionResetError:
                print(f"[ERRO] Conexão com {addr} foi encerrada inesperadamente.")
                break

# Função inicial do servidor

def main():
    # Cria socket TCP IPv4
    servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Associa o servidor ao endereço e porta definidos
    servidor.bind((HOST, PORT))

    # Coloca o servidor em modo de escuta
    servidor.listen()
    print(f"[SERVIDOR ATIVO] Escutando em {HOST}:{PORT}")

    try:
        # Loop principal do servidor, sempre aguardando novas conexões
        while True:
            # Aceita nova conexão (retorna objeto de conexão e endereço)
            conn, addr = servidor.accept()

            # Cria uma nova thread para lidar com o cliente sem travar o servidor
            thread = threading.Thread(target=handle_client, args=(conn, addr))
            thread.start()
    
    # Caso o usuário pressione CTRL+C, o servidor fecha com segurança
    except KeyboardInterrupt:
        print("\n[ENCERRANDO] Servidor finalizado com segurança.")

    finally:
        # Fecha o socket do servidor
        servidor.close()

# Ponto de entrada do script
if __name__ == "__main__":
    main()