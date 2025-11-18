#Participantes : Emanuel Guimarães, Robson Junior e Samuel Assunção

# Antes de rodar este arquivo, instale a biblioteca "websockets":
# pip install websockets
#
# Se estiver usando WSL, pode ser:
# python3 -m pip install websockets

import asyncio
import websockets

# Aqui guardamos todos os clientes conectados no momento.
# Cada cliente é representado pelo objeto "ws".
CLIENTS = set()


async def register(ws): # esse ws sempre aparece como parâmetro, pois é um objeto da lib websockets. Cada ws vai representar um respectivo cliente
    CLIENTS.add(ws)


async def unregister(ws):
    CLIENTS.remove(ws)


async def broadcast(message):
    """
    Envia uma mensagem para TODOS os clientes conectados.
    Se não tiver ninguém no chat, não faz nada.
    """
    if CLIENTS:
        # asyncio.gather envia a mensagem para todo mundo ao mesmo tempo
        await asyncio.gather(
            *(client.send(message) for client in CLIENTS),
            return_exceptions=True  # evita crash caso algum cliente dê erro
        )


async def handler(ws, path):
    """
    Essa é a função principal do servidor.
    Ela é chamada toda vez que um cliente se conecta.
    """
    await register(ws)

    try:
        # Tentamos receber o nome do cliente logo que ele entra
        try:
            name = await asyncio.wait_for(ws.recv(), timeout=5)
            join_msg = f"*** {name} entrou no chat ***"
            await broadcast(join_msg)
        except asyncio.TimeoutError:
            # Se o cliente não enviar o nome rápido, damos um nome genérico
            name = "Desconhecido"
            await broadcast(f"*** Um cliente entrou no chat (nome não recebido) ***")

        # Loop principal recebendo mensagens do cliente
        async for message in ws:
            # Quando ele manda algo, repassamos para todos
            await broadcast(f"{name}: {message}")

    except websockets.ConnectionClosed:
        # Isso acontece quando o cliente fecha o chat
        pass

    finally:
        # Sempre removemos o cliente, mesmo se der erro
        await unregister(ws)
        await broadcast(f"*** {name} saiu do chat ***")


async def main():
    """
    Aqui iniciamos o servidor WebSocket.
    Ele fica ouvindo na porta 8765 e aceita conexões de qualquer lugar (0.0.0.0).
    """
    async with websockets.serve(handler, "0.0.0.0", 8765):
        print("Servidor WebSocket rodando em ws://0.0.0.0:8765")

        # Future() nunca completa sozinho. É só para manter o servidor rodando.
        await asyncio.Future()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nServidor parado pelo usuário")