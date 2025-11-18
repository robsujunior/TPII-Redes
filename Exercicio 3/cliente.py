#Participantes : Emanuel Guimarães, Robson Junior e Samuel Assunção

import socket
import threading

# Endereço e porta do servidor TCP
HOST = "127.0.0.1"  # Endereço local
PORT = 8002          # Porta usada para o chat


def receber_msg(conexao):
    """Thread que fica continuamente ouvindo mensagens do servidor.
    Enquanto o servidor enviar dados, eles serão exibidos no terminal.
    """
    while True:
        try:
            # Aguarda dados enviados pelo servidor
            msg = conexao.recv(1024).decode("utf-8")

            # Se a mensagem vier vazia, a conexão foi encerrada
            if not msg:
                break

            # Exibe a mensagem recebida
            print(f"\nMensagem: {msg}")

        except:
            # Qualquer erro encerra a thread de recebimento
            break


def main():
    # Cria um socket TCP para o cliente
    cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Conecta ao servidor no endereço e porta especificados
    cliente.connect((HOST, PORT))

    print("Conectado ao servidor. Digite mensagens para enviar.")
    print("Digite 'sair' para encerrar.\n")

    # Inicia a thread responsável por receber mensagens do servidor
    thread_recv = threading.Thread(target=receber_msg, args=(cliente,), daemon=True)
    thread_recv.start()

    # Loop principal para envio de mensagens
    while True:
        msg = input()

        # Encerrar chat
        if msg.lower() == "sair":
            cliente.close()  # Fecha a conexão com o servidor
            print("Chat encerrado.")
            break

        # Envia a mensagem para o servidor
        cliente.sendall(msg.encode("utf-8"))


# Execução principal
if __name__ == "__main__":
    main()
