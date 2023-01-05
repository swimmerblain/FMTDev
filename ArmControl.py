import asyncio
import websockets
import logging
import json
import rtde_receive
import math
from concurrent.futures import ThreadPoolExecutor

HOST = "192.168.1.100"
pos1 = [0.0,  -90.0,   0.0, -90.0,  0.0,   0.0]
pos2 = [0.0,  -70.0,   4.0,   0.0, 80.0,   1.0]
pos3 = [0.0,   -8.16,  0.0,   0.0, 90.0, -90.0]
pos4 = [52.907, -56.805, 39.295, 16.797, 89.96, -90.00]
pos5 = [52.915, -56.507, 39.126, -60.050, 90, -90.00]
pos6 = [39.754, -29.589, 39.166, -80.251, -42.868, -90.88]
pos7 = [-75.153, -60.235, 39.129, -70.233, -5.303, -90.88]
pos8 = [-74.346, -29.249, 55.004, -47.16, -57.866, -140.305]
pos9 = [0.00, -50.41, 62.83, -220.58, -90, 0.00]
pos10 = [0.0, -90, 0.0, -180.0, -90.0, 0.0]

#logger = logging.getLogger(__name__)

server = 'ws://localhost:4007'
#msg1 = {'msg': 'setLiveSession', 'data': {'live': 'true'}}

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
        last_msg = {'msg': 'Armpos', 'data': pos1}
        while True:
            try:
                #allows you to select 1 of 10 different posistions
                # in the future will add variable position selection
                newPos = await ainput("New position 1-10: ")
                match newPos:
                    case "1":
                        msg = {'msg': 'ArmPosition', 'data': pos1}
                    case "2":
                        msg = {'msg': 'ArmPosition', 'data': pos2}
                    case "3":
                        msg = {'msg': 'ArmPosition', 'data': pos3}
                    case "4":
                        msg = {'msg': 'ArmPosition', 'data': pos4}
                    case "5":
                        msg = {'msg': 'ArmPosition', 'data': pos5}
                    case "6":
                        msg = {'msg': 'ArmPosition', 'data': pos6}
                    case "7":
                        msg = {'msg': 'ArmPosition', 'data': pos7}
                    case "8":
                        msg = {'msg': 'ArmPosition', 'data': pos8}
                    case "9":
                        msg = {'msg': 'ArmPosition', 'data': pos9}
                    case "10":
                        msg = {'msg': 'ArmPosition', 'data': pos10}
                    case "11":
                        msg = {'msg': 'armPushButton', 'data': 'armPushButton'}
                    
                if last_msg != msg:
                    print(msg)
                    await websocket.send(json.dumps(msg))
                    last_msg = msg
                #msg = {'msg': 'ArmPosition', 'data' : init_q}
                #await websocket.send(json.dumps(msg))
                #await asyncio.sleep(2)
            except websockets.exceptions.ConnectionClosed:
                print('connection closed')
                break


async def consumer():
    async with websockets.connect(server) as websocket:
        while True:
            try:
                message = await websocket.recv()
                data = json.loads(message)
                if data['msg'] == "curArmPosition":
                    #display current hand position
                    #would like to add more logic here to 
                    print("Current position: ", str(data['data']))
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
