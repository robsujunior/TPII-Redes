#Participantes : Emanuel Guimarães, Robson Junior e Samuel Assunção

import socket

# Endereço do servidor
SERVER_HOST = "127.0.0.1"  # IP local
SERVER_PORT = 8001          # Porta usada pelo servidor UDP
MAX_SIZE = 65507        # Tamanho máximo suportado pelo UDP (aproximadamente 64 KB)

def main():
    # Cria o socket UDP (SOCK_DGRAM)
    cliente = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    # Define um tempo limite de 3 segundos para resposta do servidor
    cliente.settimeout(3)

    print("Cliente UDP iniciado. Digite mensagens para enviar.")
    print("Digite 'sair' para encerrar.\n")

    while True:
        # Recebe mensagem do usuário
        msg = input("Mensagem: ")

        # Encerra o cliente se for digitado "sair"
        if msg.lower() == "sair":
            print("Encerrando cliente...")
            break

        # Verifica se a mensagem excede o limite do UDP
        if len(msg.encode("utf-8")) > MAX_SIZE:
            print("ERRO: Mensagem muito grande para UDP (máx 64KB).")
            continue

        try:
            # Envia a mensagem para o servidor (sem conexão, UDP)
            cliente.sendto(msg.encode("utf-8"), (SERVER_HOST, SERVER_PORT))

            # Aguarda resposta do servidor
            resposta, _ = cliente.recvfrom(MAX_SIZE)

            # Exibe mensagem de eco do servidor
            print("Eco do servidor:", resposta.decode("utf-8"))
        
        # Caso o tempo limite de 3 segundos expire sem resposta
        except socket.timeout:
            print("Tempo limite: nenhuma resposta do servidor.")
        
        # Qualquer outro erro de comunicação
        except Exception as e:
            print(f"Erro de comunicação: {e}")

    # Fecha o socket
    cliente.close()

# Execução do programa
if __name__ == "__main__":
    main()