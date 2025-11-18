import socket

# Endereço do servidor (0.0.0.0 permite receber mensagens de qualquer IP)
HOST = "0.0.0.0"
# Porta utilizada para comunicação UDP
PORT = 8001
# Tamanho máximo de mensagem suportado pelo UDP
MAX_SIZE = 65507

def main():
    # Criação do socket UDP
    servidor = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    # Liga o socket ao endereço e porta
    servidor.bind((HOST, PORT))

    # Define timeout de 1 segundo para permitir detectar Ctrl+C durante o loop
    servidor.settimeout(1)

    print(f"[SERVIDOR UDP] Escutando em {HOST}:{PORT}")

    try:
        while True:
            try:
                # Aguarda mensagem do cliente
                msg, addr = servidor.recvfrom(MAX_SIZE)

                # Exibe a mensagem recebida e o IP de origem
                print(f"[RECEBIDO de {addr}] {msg.decode('utf-8')}")

                # Envia o mesmo conteúdo de volta (eco)
                servidor.sendto(msg, addr)

            except socket.timeout:
                # Timeout ocorre para não travar o servidor e permitir interrupção
                continue

    except KeyboardInterrupt:
        # Finalização segura ao pressionar Ctrl+C
        print("\n[SERVIDOR] Fechando com segurança...")

    finally:
        # Fecha o socket antes de encerrar
        servidor.close()

# Execução principal
if __name__ == "__main__":
    main()