#Participantes : Emanuel Guimarães, Robson Junior e Samuel Assunção

# Antes de rodar este arquivo, instale a biblioteca "websockets":
# pip install websockets
#
# Se estiver usando WSL, pode ser:
# python3 -m pip install websockets

import asyncio
import websockets
import sys

# Endereço onde o servidor está rodando.
# Aqui está como "localhost" (127.0.0.1), então só funciona na mesma máquina. Para rodar em redes diferentes, daria pra usar o ngrok por exemplo
SERVER_URI = "ws://127.0.0.1:8765"


async def listen_messages(ws):
    """
    Essa função fica esperando mensagens que chegam do servidor.
    Sempre que chega algo, a gente imprime na tela.
    """
    try:
        async for msg in ws:  # Loop que recebe cada mensagem enviada pelo servidor
            print("\r" + msg)  # \r só ajuda a não bagunçar a linha onde o usuário está digitando
            print("> ", end="", flush=True)  # Reexibe o símbolo de digitação depois de receber mensagem
    except websockets.ConnectionClosed:
        print("\nConexão encerrada pelo servidor.")
        return


async def send_messages(ws):
    """
    Essa função cuida de enviar mensagens para o servidor.
    A parte do run_in_executor é só para rodar o input() sem travar o programa.
    """
    loop = asyncio.get_running_loop()

    while True:
        try:
            # input() é bloqueante (travaria o programa), então rodamos ele num executor
            msg = await loop.run_in_executor(None, lambda: input("> "))

            if msg is None:
                continue

            msg = msg.strip()

            # Ignora mensagens vazias
            if msg == "":
                continue

            # Comandos de saída
            if msg.lower() in ("/quit", "/sair", "/exit"):
                await ws.close()
                return

            # Envia a mensagem para o servidor
            await ws.send(msg)

        except EOFError:
            # Isso acontece quando o usuário aperta Ctrl+D
            await ws.close()
            return

        except websockets.ConnectionClosed:
            return


async def main():
    """
    Essa é a função principal do cliente.
    Aqui a gente conecta ao servidor, manda o nome do usuário
    e inicia duas tarefas ao mesmo tempo:
      - Uma para ouvir mensagens
      - Outra para enviar mensagens
    """
    name = input("Seu nome: ").strip()
    if not name:
        name = "Anon"

    try:
        # Tenta conectar ao servidor
        async with websockets.connect(SERVER_URI) as ws:
            await ws.send(name)  # Envia o nome do usuário para o servidor

            print(f"Conectado em {SERVER_URI} como {name}. Digite /quit para sair.")

            # Cria duas tarefas: uma ouvindo e outra enviando
            listener = asyncio.create_task(listen_messages(ws))
            sender = asyncio.create_task(send_messages(ws))

            # Espera até uma delas terminar (ex: usuário saiu)
            done, pending = await asyncio.wait(
                [listener, sender],
                return_when=asyncio.FIRST_COMPLETED,
            )

            # Cancela a que sobrou
            for t in pending:
                t.cancel()

    except ConnectionRefusedError:
        # Acontece quando o servidor não está ligado
        print(f"Não foi possível conectar em {SERVER_URI}. Verifique se o servidor está rodando.")

    except KeyboardInterrupt:
        # Se o usuário der Ctrl+C no terminal
        print("\nEncerrando cliente.")


# Parte que garante que o programa só roda quando chamado diretamente
if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nCliente interrompido.")