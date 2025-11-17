import asyncio
import websockets

CLIENTS = set()

async def register(ws):
    CLIENTS.add(ws)

async def unregister(ws):
    CLIENTS.remove(ws)

async def broadcast(message):
    if CLIENTS:
        await asyncio.gather(*(client.send(message) for client in CLIENTS), return_exceptions=True)

async def handler(ws, path):
    await register(ws)
    try:
        try:
            name = await asyncio.wait_for(ws.recv(), timeout=5)
            join_msg = f"*** {name} entrou no chat ***"
            await broadcast(join_msg)
        except asyncio.TimeoutError:
            name = "Desconhecido"
            await broadcast(f"*** Um cliente entrou no chat (nome não recebido) ***")

        async for message in ws:
            await broadcast(f"{name}: {message}")

    except websockets.ConnectionClosed:
        pass
    finally:
        await unregister(ws)
        await broadcast(f"*** {name} saiu do chat ***")

async def main():
    async with websockets.serve(handler, "0.0.0.0", 8765):
        print("Servidor WebSocket rodando em ws://0.0.0.0:8765")
        await asyncio.Future()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nServidor parado pelo usuário")
