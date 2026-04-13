import asyncio

# fila compartilhada entre produtor e consumidor
queue = asyncio.Queue()

async def produtor():
    for i in range(5):
        await asyncio.sleep(1)  # simula trabalho (ex: chamada de API)
        await queue.put(i)      # coloca o valor na fila
        print(f"produziu: {i}")

async def consumidor():
    while True:
        dado = await queue.get()  # trava aqui até ter algo na fila
        print(f"consumiu: {dado}")
        queue.task_done()         # marca o item como processado

async def main():
    # roda produtor e consumidor ao mesmo tempo
    await asyncio.gather(
        produtor(),
        consumidor()
    )

asyncio.run(main())  # inicia o event loop