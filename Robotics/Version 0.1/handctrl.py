import asyncio
import websockets
import logging
import json
import rtde_receive
import math
from concurrent.futures import ThreadPoolExecutor


#logger = logging.getLogger(__name__)

server = 'ws://localhost:4007'

async def toDeg(values):
    for i in range(len(values)):
        values[i] = round(math.degrees(values[i]), 2)
        print(values[i])
    return values

async def ainput(prompt: str = "") -> str:
    with ThreadPoolExecutor(1, 'ainput') as executor:
        return (await asyncio.get_event_loop().run_in_executor(executor, input, prompt)).rstrip()


async def producer():
    async with websockets.connect(server) as websocket:
        while True:
            try:
                newPos = await ainput("New position 0-100: ")
                pos = max(min(100, int(round(float(newPos),1))),0)
                msg = {'msg': 'handPos', 'data': str(pos)}
                print(msg)
                await websocket.send(json.dumps(msg))
            except websockets.exceptions.ConnectionClosed:
                print('connection closed')
                break


async def consumer():
    async with websockets.connect(server) as websocket:
        while True:
            try:
                message = await websocket.recv()
                data = json.loads(message)
                if data['msg'] == "curHandPos":
                    print("Hand Position: ", str(data['data']))
                #print("Recieved msg", data)
            except websockets.exceptions.ConnectionClosed:
                #print('connection closed')
                break


async def async_processing():
    async with websockets.connect(server) as websocket:
        while True:
            try:
                message = await websocket.recv()
                #print(message)

            except websockets.exceptions.ConnectionClosed:
                print('connection closed')
                break

async def handle():
    consumer_task = asyncio.ensure_future(consumer())
    producer_task = asyncio.ensure_future(producer())
    done, pending = await asyncio.wait([consumer_task, producer_task], return_when = asyncio.FIRST_COMPLETED,)
    for task in pending:
        task.cancel()


asyncio.get_event_loop().run_until_complete(handle())
#asyncio.get_event_loop().run_until_complete(async_processing())
