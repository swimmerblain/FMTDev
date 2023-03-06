import asyncio
import websockets
import logging
import json
import rtde_receive
import rtde_control
import rtde_io
import math
import ssl

#HOST = "192.168.1.100"
HOST = "192.168.89.129"

#server = 'wss://studies-warned-sofa-polar.trycloudflare.com'
server = 'wss://192.168.1.45:4007'

async def producer():
    async with websockets.connect(server, ssl=ssl.SSLContext(protocol=ssl.PROTOCOL_TLS)) as wsr:
        print("connected to websocket")
        recv = rtde_receive.RTDEReceiveInterface(HOST)
        while True:
            try: 
                init_q = recv.getActualQ()
                msg = {'msg': 'currentArmPosition', 'data': init_q}
                await wsr.send(json.dumps(msg))
                await asyncio.sleep(0.1)
            except websockets.exceptions.ConnectionClosed:
                print("Connection Closed")
                break

asyncio.get_event_loop().run_until_complete(producer())

