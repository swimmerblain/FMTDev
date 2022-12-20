import asyncio
import websockets
import logging
import json
import rtde_receive
import rtde_control
import math


HOST = "192.168.1.100"

logger = logging.getLogger(__name__)

server = 'ws://localhost:4007'
msg1 = {'msg': 'setLiveSession', 'data': {'live': 'true'}}

async def toDeg(values):
    for i in range(len(values)):
        values[i] = round(math.degrees(values[i]), 2)
        print(values[i])
    return values


async def producer():
    async with websockets.connect(server) as websocket:
        global recv 
        recv = rtde_receive.RTDEReceiveInterface(HOST)
        await websocket.send(json.dumps(msg1))
        while True:
            try:
                init_q = recv.getActualQ()
                for i in range(len(init_q)):
                    init_q[i] = round(math.degrees(init_q[i]), 3)

                msg = {'msg': 'currentArmPosition', 'data' : init_q}
                await websocket.send(json.dumps(msg))
                #get hand position and send
                #will get hand position from TXT file for now then send
                await asyncio.sleep(2)
            except websockets.exceptions.ConnectionClosed:
                print('connection closed')
                break


async def consumer():
    async with websockets.connect(server) as websocket:
        cont =  rtde_control.RTDEControlInterface(HOST)
        #recv2 = rtde_receive.RTDEReceiveInterface(HOST)
        odd_even = 0
        while True:
            try:
                message = await websocket.recv()
                msgData = json.loads(message)
                if msgData['msg'] == "newArmPosition":
                    init_q = recv.getActualQ()
                    print("Recieved msg" + str(msgData))
                    print(msgData['data'][1])
                    for i in range(len(msgData['data'])):
                        init_q[i] = round(math.radians(msgData['data'][i]),8)
                    cont.moveJ(init_q, 2, 0.5, True)
                if msgData['msg'] == "newHandPos":
                    with open('hand.txt', 'w') as f:
                        f.write(msgData['data'])
                    print(msgData['data'])

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
