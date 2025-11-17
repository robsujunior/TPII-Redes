import asyncio
import websockets
import sys

SERVER_URI = "ws://127.0.0.1:8765"

async def listen_messages(ws):
    try:
        async for msg in ws:
            print("\r" + msg)
            print("> ", end="", flush=True)
    except websockets.ConnectionClosed:
        print("\nConexão encerrada pelo servidor.")
        return

async def send_messages(ws):
    loop = asyncio.get_running_loop()
    while True:
        try:
            msg = await loop.run_in_executor(None, lambda: input("> "))
            if msg is None:
                continue
            msg = msg.strip()
            if msg == "":
                continue
            if msg.lower() in ("/quit", "/sair", "/exit"):
                await ws.close()
                return
            await ws.send(msg)
        except EOFError:
            await ws.close()
            return
        except websockets.ConnectionClosed:
            return

async def main():
    name = input("Seu nome: ").strip()
    if not name:
        name = "Anon"
    try:
        async with websockets.connect(SERVER_URI) as ws:
            await ws.send(name)
            print(f"Conectado em {SERVER_URI} como {name}. Digite /quit para sair.")
            listener = asyncio.create_task(listen_messages(ws))
            sender = asyncio.create_task(send_messages(ws))

            done, pending = await asyncio.wait(
                [listener, sender],
                return_when=asyncio.FIRST_COMPLETED,
            )

            for t in pending:
                t.cancel()
    except ConnectionRefusedError:
        print(f"Não foi possível conectar em {SERVER_URI}. Verifique se o servidor está rodando.")
    except KeyboardInterrupt:
        print("\nEncerrando cliente.")

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nCliente interrompido.")
