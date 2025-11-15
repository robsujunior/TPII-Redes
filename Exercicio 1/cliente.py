import socket

HOST = '127.0.0.1'  # Mesmo endereço do servidor
PORT = 61         # Mesma porta do servidor

def main():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as cliente:
        try:
            cliente.connect((HOST, PORT))
            print(f"Conectado ao servidor em {HOST}:{PORT}")
            
            while True:
                msg = input("Digite uma mensagem (ou 'sair' para encerrar): ").strip()
                if msg.lower() == 'sair':
                    print("Encerrando conexão...")
                    break
                
                if msg == "":
                    print("❌ Mensagem vazia não permitida.")
                    continue

                cliente.sendall(msg.encode('utf-8'))
                resposta = cliente.recv(1024).decode('utf-8')
                print(f"Servidor respondeu: {resposta}")

        except ConnectionRefusedError:
            print("❌ Não foi possível conectar ao servidor. Verifique se ele está em execução.")

if __name__ == "__main__":
    main()
