import asyncio
import shlex
from cowsay import list_cows, cowsay, cowthink

clients = {}
free_cows = list_cows()


async def chat(reader, writer):
    me = "UNAUTHORIZED:{}:{}".format(*writer.get_extra_info("peername"))
    print(me, "has connected")
    clients[me] = asyncio.Queue()
    send = asyncio.create_task(reader.readline())
    receive = asyncio.create_task(clients[me].get())
    quit_flag = False

    while not reader.at_eof():
        if quit_flag:
            break
        done, pending = await asyncio.wait([send, receive],
                                           return_when=asyncio.FIRST_COMPLETED)
        for q in done:
            if q is send:
                send = asyncio.create_task(reader.readline())
                message = q.result().decode().strip()

                if message == "who":
                    out = ""
                    for client in clients.keys():
                        if not client.startswith("UNAUTHORIZED"):
                            out += client + "\n"
                    if out == "":
                        out = "no logged in users\n"
                    writer.write(out.encode())
                elif message == "cows":
                    out = ""
                    for cow in free_cows:
                        out += cow + "\n"
                    if out == "":
                        out = "no free cows]n"
                    writer.write(out.encode())
                elif message == "quit":
                    quit_flag = True
                    break
                else:
                    message = shlex.split(message)
                    if message[0] == "login":
                        pass
                    elif message[0] == "say":
                        pass
                    elif message[0] == "yield":
                        pass
                    else:
                        writer.write("no such command\n".encode())
            elif q is receive:
                receive = asyncio.create_task(clients[me].get())
                writer.write(f"{q.result()}\n".encode())
                await writer.drain()
    send.cancel()
    receive.cancel()
    print(me, "DONE")
    del clients[me]
    if not me.startswith("UNAUTHORIZED"):
        free_cows.append(me)
        for key, out in clients.items():
            if not key.startswith("UNAUTHORIZED"):
                await out.put(f"SERVER: {me} logs out")
    writer.close()
    await writer.wait_closed()


async def main():
    server = await asyncio.start_server(chat, '0.0.0.0', 1337)
    async with server:
        await server.serve_forever()

asyncio.run(main())
