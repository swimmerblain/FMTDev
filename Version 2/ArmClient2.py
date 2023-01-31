import asyncio
import websockets
import logging
import json
import rtde_receive
import rtde_control
import rtde_io
import math


HOST = "192.168.1.100"

logger = logging.getLogger(__name__)

server = 'ws://localhost:4007'
msg1 = {'msg': 'setLiveSession', 'data': {'live': 'true'}}
HOMEPOSITION = [0.0, -90, 0.0, -180.0, -90.0, 0.0]
pos9 = [0.00, -50.41, 62.83, -220.58, -90, 0.00] #21 inches from base
pos11 = [-30.37, -7.6, 13.4, -66.6, -67.41, 70.18] #26 inches from base


async def producer():
    async with websockets.connect(server) as websocket:
        global recv 
        recv = rtde_receive.RTDEReceiveInterface(HOST)
        while True:
            try:
                init_q = recv.getActualQ()

                msg = {'msg': 'currentArmPosition', 'data' : init_q}
                await websocket.send(json.dumps(msg))
                await asyncio.sleep(1)
            except websockets.exceptions.ConnectionClosed:
                print('connection closed')
                break


async def consumer():
    x = 2

async def handle():
    consumer_task = asyncio.ensure_future(consumer())
    producer_task = asyncio.ensure_future(producer())
    done, pending = await asyncio.wait([consumer_task, producer_task], return_when = asyncio.FIRST_COMPLETED,)
    for task in pending:
        task.cancel()


asyncio.get_event_loop().run_until_complete(handle())
#asyncio.get_event_loop().run_until_complete(async_processing())
