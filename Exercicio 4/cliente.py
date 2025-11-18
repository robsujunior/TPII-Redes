import socket

# Endereço e porta do servidor que fornece a hora
HOST = "127.0.0.1"  # Servidor local
PORT = 8003          # Porta onde o servidor estará ouvindo

def main():
    try:
        # Criação do socket TCP
        cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # Conexão ao servidor
        cliente.connect((HOST, PORT))

        # Envia comando solicitando a hora
        cliente.sendall(b"hora")

        # Aguarda resposta do servidor (até 1024 bytes)
        hora = cliente.recv(1024).decode("utf-8")

        # Exibe a hora recebida
        print(f"Hora recebida do servidor: {hora}")

        # Encerra a conexão
        cliente.close()

    except ConnectionRefusedError:
        # Caso o servidor não esteja rodando
        print("Não foi possível conectar ao servidor.")
    except Exception as e:
        # Captura qualquer outro erro inesperado
        print("Erro:", e)


# Execução principal
if __name__ == "__main__":
    main()