import websockets
import sys
import tkinter as tk
import websockets
import json
import asyncio
import time
import threading
from concurrent.futures import ThreadPoolExecutor

server = 'ws://localhost:4007'

async def ainput(prompt: str = "") -> str:
    with ThreadPoolExecutor(1, 'ainput') as executor:
        return (await asyncio.get_event_loop().run_in_executor(executor, input, prompt)).rstrip()

async def producer():
    async with websockets.connect(server) as websocket:
        last_msg = {'msg': 'Armpos', 'data': "Unknown"}
        while True:
            try:
                #allows you to select 1 of 10 different posistions
                # in the future will add variable position selection
                newPos = await ainput("New Command 1-10: ")
                match newPos:
                    case "1":
                        msg = {'msg': 'dashboardCMD', 'data': "shutdown"}
                    case "2":
                        msg = {'msg': 'dashboardCMD', 'data': 'power off'}
                    case "3":
                        msg = {'msg': 'dashboardCMD', 'data': "power on"}
                    case "4":
                        msg = {'msg': 'dashboardCMD', 'data': "brake release"}
                    case "5":
                        msg = {'msg': 'dashboardCMD', 'data': "unlock protective stop"}
                    case "6":
                        msg = {'msg': 'dashboardCMD', 'data': "restart safety"}
                    case "7":
                        msg = {'msg': 'dashboardCMD', 'data': "quit"}
                    case "8":
                        msg = {'msg': 'Casual Test', 'data': "None"}
                    case "9":
                        msg = {'msg': 'dashboardCMD', 'data': "None"}
                    case "10":
                        msg = {'msg': 'dashboardCMD', 'data': "None"}
                    case "11":
                        msg = {'msg': 'dashboardCMD', 'data': "None"}
                    
                if last_msg != msg:
                    print(json.dumps(msg))
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
                if 'msg' in data:
                    if data['msg'] == "dashboardData":
                        #display current hand position
                        #would like to add more logic here to 
                        print("dashboardData: ", str(data['data']))
                #print("Recieved msg", data)
            except websockets.exceptions.ConnectionClosed:
                #print('connection closed')
                break

async def handle():
    consumer_task = asyncio.ensure_future(consumer())
    producer_task = asyncio.ensure_future(producer())
    done, pending = await asyncio.wait([consumer_task, producer_task], return_when = asyncio.FIRST_COMPLETED,)
    for task in pending:
        task.cancel()


asyncio.get_event_loop().run_until_complete(handle())

