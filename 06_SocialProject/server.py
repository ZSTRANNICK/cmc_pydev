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
                if message == "":
                    continue
                message = message.split(' ', 1)
                id = message[0]
                message = message[1]

                if message == "who":
                    out = ""
                    for client in clients.keys():
                        if not client.startswith("UNAUTHORIZED"):
                            out += client + "\n"
                    if out == "":
                        out = "no logged in users\n"
                    out = id + " " + out
                    writer.write(out.encode())
                elif message == "cows":
                    out = ""
                    for cow in free_cows:
                        out += cow + "\n"
                    if out == "":
                        out = "no free cows\n"
                    out = id + " " + out
                    writer.write(out.encode())
                elif message == "quit":
                    quit_flag = True
                    break
                else:
                    message = shlex.split(message)
                    if message[0] == "login":
                        if len(message) > 2:
                            writer.write((id + " too many arguments\n").encode())
                            continue
                        if len(message) < 2:
                            writer.write((id + " not enough arguments\n").encode())
                            continue
                        if not message[1] in free_cows:
                            writer.write((id +
                                " no free cows with that name\n".encode()))
                            continue

                        receive.cancel()
                        del clients[me]
                        free_cows.remove(message[1])

                        print(me, "logs in as", message[1])
                        for key, out in clients.items():
                            if not key.startswith("UNAUTHORIZED"):
                                if not me.startswith("UNAUTHORIZED"):
                                    await out.put(f"0 SERVER: {me} logs out")
                                await out.put(f"0 SERVER: {message[1]} logs in")

                        me = message[1]
                        clients[me] = asyncio.Queue()
                        receive = asyncio.create_task(clients[me].get())
                    elif message[0] == "say":
                        if len(message) > 3:
                            writer.write((id + " too many arguments\n").encode())
                            continue
                        if len(message) < 3:
                            writer.write((id + " not enough arguments\n").encode())
                            continue
                        if not message[1] in clients.keys():
                            writer.write((id + " no user with that name\n").encode())
                            continue
                        if me.startswith("UNAUTHORIZED"):
                            writer.write((id + 
                                " you should be authorized "
                                "to do that\n").encode())
                            continue
                        if message[1].startswith("UNAUTHORIZED"):
                            writer.write((id +
                                " you can't send messages"
                                "to unauthorized users\n").encode())
                            continue
                        await clients[message[1]].put("0 " + cowthink(message[2],
                                                               cow=me))
                        await clients[me].put("0 " + cowthink(message[2], cow=me))
                    elif message[0] == "yield":
                        if len(message) > 2:
                            writer.write((id + " too many arguments\n").encode())
                            continue
                        if len(message) < 2:
                            writer.write((id + " not enough arguments\n").encode())
                            continue
                        if me.startswith("UNAUTHORIZED"):
                            writer.write((id + 
                                " you should be authorized "
                                "to do that\n").encode())
                            continue
                        for key, out in clients.items():
                            if not key.startswith("UNAUTHORIZED"):
                                await out.put("0 " + cowsay(message[1], cow=me))
                    else:
                        writer.write((id + " no such command\n").encode())
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
