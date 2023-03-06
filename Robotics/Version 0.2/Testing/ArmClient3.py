import asyncio
import websockets
import logging
import json
import rtde_receive
import math


HOST = "192.168.89.129"

logger = logging.getLogger(__name__)

#server = 'ws://localhost:4007'
server = 'ws://172.27.208.1:4007'
msg1 = {'msg': 'setLiveSession', 'data': {'live': 'true'}}
HOMEPOSITION = [0.0, -90, 0.0, -180.0, -90.0, 0.0]
pos9 = [0.00, -50.41, 62.83, -220.58, -90, 0.00] #21 inches from base
pos11 = [-30.37, -7.6, 13.4, -66.6, -67.41, 70.18] #26 inches from base


def producer():
    print("here i am")
    print("here i am")
    global recv 
    recv = rtde_receive.RTDEReceiveInterface(HOST)
    while True:
        try:
            init_q = recv.getActualQ()
            msg = {'msg': 'currentArmPosition', 'data' : init_q}

        except websockets.exceptions.ConnectionClosed:
            print('connection closed')
            break



producer()
#loop = asyncio.get_event_loop()
#loop.run_until_complete(handle())

#loop = asyncio.new_event_loop()
#asyncio.set_event_loop(loop)
#loop.run_until_complete(handle())
#asyncio.run(handle())
#asyncio.get_running_loop().run_until_complete(handle())
#asyncio.get_event_loop().run_until_complete(async_processing())
