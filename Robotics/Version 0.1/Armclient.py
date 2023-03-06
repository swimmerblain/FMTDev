import asyncio
import websockets
import logging
import json
import rtde_receive
import rtde_control
import rtde_io
import math


#HOST = "192.168.1.100"
HOST = "192.168.89.129"

logger = logging.getLogger(__name__)

#server = 'ws://localhost:4007'
server = 'wss://fat-samoa-skilled-arrivals.trycloudflare.com'
#server = 'ws://192.168.1.45:4007'
msg1 = {'msg': 'setLiveSession', 'data': {'live': 'true'}}
HOMEPOSITION = [0.0, -90, 0.0, -180.0, -90.0, 0.0]
pos9 = [0.00, -50.41, 62.83, -220.58, -90, 0.00] #21 inches from base
pos11 = [-30.37, -7.6, 13.4, -66.6, -67.41, 70.18] #26 inches from base


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
        handPosFBK = ""
        while True:
            try:
                init_q = recv.getActualQ()
                #for i in range(len(init_q)):
                #    init_q[i] = round(math.degrees(init_q[i]), 3)

                msg = {'msg': 'currentArmPosition', 'data' : init_q}
                await websocket.send(json.dumps(msg))
                #get hand position and send
                #will get hand position from TXT file for now then send
                #with open('curhand.txt', 'r') as f:
                #    handPosFBK = f.readline()
                #msg = {'msg': 'currentHandPos', 'data' : handPosFBK}
                await asyncio.sleep(0.1)
            except websockets.exceptions.ConnectionClosed:
                print('connection closed')
                break


async def consumer():
    async with websockets.connect(server) as websocket:
        cont =  rtde_control.RTDEControlInterface(HOST)
        recv2 = rtde_receive.RTDEReceiveInterface(HOST)
        io_ = rtde_io.RTDEIOInterface(HOST)
        io_.setStandardDigitalOut(0, True)
        odd_even = 0
        while True:
            try:
                message = await websocket.recv()
                msgData = json.loads(message)
                if recv2.isEmergencyStopped():
                    io_.setStandardDigitalOut(1, True)
                    io_.setStandardDigitalOut(2, False)
                    io_.setStandardDigitalOut(3, False)
                elif recv2.isProtectiveStopped():
                    io_.setStandardDigitalOut(1, True)
                    io_.setStandardDigitalOut(2, False)
                    io_.setStandardDigitalOut(3, False)
                elif (msgData['msg'] == 'lightColor'):
                    if msgData['data'] == 'red':
                        io_.setStandardDigitalOut(1, True)
                        io_.setStandardDigitalOut(2, False)
                        io_.setStandardDigitalOut(3, False)
                    elif msgData['data'] == 'yellow':
                        io_.setStandardDigitalOut(1, False)
                        io_.setStandardDigitalOut(2, True)
                        io_.setStandardDigitalOut(3, False)
                    elif msgData['data'] == 'green':
                        io_.setStandardDigitalOut(1, False)
                        io_.setStandardDigitalOut(2, False)
                        io_.setStandardDigitalOut(3, True)
                    
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
                if msgData['msg'] == "armPushButton":
                    with open('hand.txt', 'w') as f:
                        f.write('0')
                    pb1 = recv.getActualQ()
                    pb2 = recv.getActualQ()
                    pb3 = recv.getActualQ()
                    pb1[0] = HOMEPOSITION[0]
                    pb1[1] = HOMEPOSITION[1]
                    pb1[2] = HOMEPOSITION[2]
                    pb1[3] = HOMEPOSITION[3]
                    pb1[4] = HOMEPOSITION[4]
                    pb1[5] = HOMEPOSITION[5]
                    pb2[0] = pos9[0]
                    pb2[1] = pos9[1]
                    pb2[2] = pos9[2]
                    pb2[3] = pos9[3]
                    pb2[4] = pos9[4]
                    pb2[5] = pos9[5]
                    pb3[0] = pos11[0]
                    pb3[1] = pos11[1]
                    pb3[2] = pos11[2]
                    pb3[3] = pos11[3]
                    pb3[4] = pos11[4]
                    pb3[5] = pos11[5]
                    speed = [0,0, -0.1, 0, 0,0]
                    
                    cont.moveJ(pb1, 2, .5, False)
                    cont.moveJ(pb2, 2, .5, False)
                    #use if the hand needs to go out farther to push the button
                    #cont.moveJ(pb3, 2, .5, False)
                    cont.moveUntilContact(speed)
                    
                    #use if the hand needs to go out farther to push the button
                    #cont.moveJ(pb3, 2, .5, False)
                    cont.moveJ(pb2, 2, .5, False)

            except websockets.exceptions.ConnectionClosed:
                print('connection closed')
                io_.setStandardDigitalOut(1, True)
                io_.setStandardDigitalOut(2, False)
                io_.setStandardDigitalOut(3, False)
                break


async def handle():
    consumer_task = asyncio.ensure_future(consumer())
    producer_task = asyncio.ensure_future(producer())
    done, pending = await asyncio.wait([consumer_task, producer_task], return_when = asyncio.FIRST_COMPLETED,)
    for task in pending:
        task.cancel()


asyncio.get_event_loop().run_until_complete(handle())
#asyncio.get_event_loop().run_until_complete(async_processing())
