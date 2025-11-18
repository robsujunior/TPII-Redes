#Participantes : Emanuel Guimarães, Robson Junior e Samuel Assunção

import socket
import threading

# Endereço e porta onde o servidor irá escutar
HOST = "127.0.0.1"
PORT = 8002

# Lista que armazena as conexões dos clientes conectados
clientes = []


def encaminhar(mensagem, remetente):
    """Envia a mensagem para todos os clientes, exceto para quem a enviou.
    Isso faz o servidor funcionar como um "repassador" (relay) de mensagens.
    """
    for c in clientes:
        if c != remetente:
            try:
                # Envia a mensagem para o cliente correspondente
                c.sendall(mensagem)
            except:
                # Caso algum cliente desconecte inesperadamente
                pass


def lidar_com_cliente(conn, addr):
    """Função executada por uma thread para cada cliente conectado.
    Ela recebe mensagens do cliente e encaminha para o outro cliente.
    """
    print(f"[CONECTADO] Cliente: {addr}")

    while True:
        try:
            # Aguarda mensagem do cliente
            msg = conn.recv(1024)

            # Se a mensagem vier vazia, o cliente desconectou
            if not msg:
                break

            # Envia a mensagem para o outro cliente
            encaminhar(msg, conn)

        except:
            # Se houver qualquer erro (como desconexão abrupta)
            break

    print(f"[DESCONECTADO] {addr}")

    # Remove o cliente da lista e encerra sua conexão
    clientes.remove(conn)
    conn.close()


def main():
    # Cria socket TCP do servidor
    servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Associa o servidor ao endereço configurado
    servidor.bind((HOST, PORT))

    # Coloca o servidor em modo de escuta (máximo 2 clientes)
    servidor.listen(2)

    print("[SERVIDOR ATIVO] Aguardando 2 clientes...")

    # Servidor aceita exatamente dois clientes
    while len(clientes) < 2:
        conn, addr = servidor.accept()

        # Armazena o cliente conectado
        clientes.append(conn)

        # Cria thread para tratar esse cliente
        thread = threading.Thread(target=lidar_com_cliente, args=(conn, addr))
        thread.start()

    print("[CHAT INICIADO] Dois clientes conectados. Mensagens serão repassadas.")


# Execução principal
if __name__ == "__main__":
    main()
