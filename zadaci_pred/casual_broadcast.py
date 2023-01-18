import asyncio

NODES = 10   # simulirano slanje sa 10 nodova
sequences = [0] * NODES # [0, 0, 0 0, 0, 0, 0 ...]
buffer = {} # dictionary za spremanje


async def handler(reader, writer):
    print("Netko je ovdje")

    while data := await reader.readline():
        try:
            ldata = data.decode("utf8").split('/', maxsplit = 2) # umjesto zareza mora se koristiti / separator
            if len(ldata) != 3:
                raise Exception("Greška! Krivi format unosa.")
            # sender - int, deps - tuple odvojen "," , message - string
            sender, deps, msg = int(ldata[0]), tuple(map(int, ldata[1].split(','))), ldata[2].strip()
            print("Primljeno: ", sender, deps, msg)
            buffer[sender, deps] = msg

            def deliver():
                print(f"Status: {'-'.join(map(str, sequences))}")  # f-string
                for (n, x), msg in buffer.items():  # prolazi kroz items u buffer dictionary-u
                    # if true: za svaki node ukoliko je sequnces >= od dependencies na tom indexu
                    if all(sequences[i] >= x[i] for i in range(NODES)):

                        print("___ Isporuka: ", n, x, msg)
                        del buffer[n, x]
                        sequences[n] += 1
                        return True

            while deliver():
                pass

        except Exception as e:
            print(e)


async def main():
    server = await asyncio.start_server(handler, "127.0.0.1", 9000)
    print(server.sockets)
    async with server:
        print("Server započeo!")
        await server.serve_forever()

asyncio.run(main())