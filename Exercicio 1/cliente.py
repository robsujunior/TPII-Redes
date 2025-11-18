import socket

# Endereço IP do servidor ao qual o cliente tentará se conectar
HOST = '127.0.0.1'  # Mesmo endereço do servidor
# Porta onde o servidor está ouvindo conexões
PORT = 8000         # Mesma porta do servidor

def main():
    # Cria um socket TCP (AF_INET = IPv4, SOCK_STREAM = TCP)
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as cliente:
        try:
            # Tenta estabelecer conexão com o servidor
            cliente.connect((HOST, PORT))
            print(f"Conectado ao servidor em {HOST}:{PORT}")
            
            while True:
                # Solicita que o usuário digite uma mensagem
                msg = input("Digite uma mensagem (ou 'sair' para encerrar): ").strip()
                
                # Se o usuário digitar 'sair', encerra o loop e desconecta
                if msg.lower() == 'sair':
                    print("Encerrando conexão...")
                    break
                
                # Impede que mensagens vazias sejam enviadas
                if msg == "":
                    print("Mensagem vazia não permitida.")
                    continue

                # Envia a mensagem codificada em UTF-8 para o servidor
                cliente.sendall(msg.encode('utf-8'))
                
                # Recebe a resposta do servidor (até 1024 bytes) e decodifica
                resposta = cliente.recv(1024).decode('utf-8')
                print(f"Servidor respondeu: {resposta}")

        except ConnectionRefusedError:
            # Tratamento caso o servidor não esteja ativo ou rejeite a conexão
            print("Não foi possível conectar ao servidor. Verifique se ele está em execução.")

# Ponto de entrada do programa
if __name__ == "__main__":
    main()
