import asyncio
import websockets
import json
import rtde_receive
import math

HOST = "192.168.89.129"

server = 'ws://localhost:4007'

async def producer():
    async with websockets.connect(server) as websocket:
        global recv
        recv = rtde_receive.RTDEReceiveInterface(HOST)
        
        while True:
            try:
                init_q = recv.getActualQ()
                
                msg = {'msg': 'currentArmPosition', 'data': init_q}

                await websocket.send(json.dumps(msg))
                await asyncio.sleep(1)
            except websockets.exceptions.ConnectionClosed:
                print('connectionclosed')
                break

asyncio.get_event_loop().run_until_complete(producer())
