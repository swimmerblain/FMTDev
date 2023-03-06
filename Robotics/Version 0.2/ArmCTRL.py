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

#server = 'wss://fat-samoa-skilled-arrivals.trycloudflare.com'
server = 'ws://localhost:4007'

#server = 'wss://192.168.1.45:4007'

async def consumer():
    # when using SSL you ned to run the top async text to essentially ignore the ssl protocol
    #async with websockets.connect(server, ssl=ssl.SSLContext(protocol=ssl.PROTOCOL_TLS)) as websocket:
    
    # run this line when you have no SSL when running on local host
    async with websockets.connect(server) as websocket:
        print("connected")
        cont = rtde_control.RTDEControlInterface(HOST)
        recv = rtde_receive.RTDEReceiveInterface(HOST)  
        init_q = recv.getActualQ()
        print(init_q)
        while True:
            try:
                message = await websocket.recv()
                msgData = json.loads(message)
                if msgData['msg'] == 'preMotions':
                    print(msgData['data'])
                    data = msgData['data']
                    for moves in data['moves']:
                        for i in range(len(moves)):
                            #init_q[i] = round(math.radians(moves[i]),8)
                            init_q[i] = moves[i]
                        cont.moveJ(init_q, 2, 3, False)
                        print(moves)
                if msgData['msg'] == 'newArmPosition':
                    for i in range(len(msgData['data'])):
                        init_q[i] = msgData['data'][i]
                    cont.moveJ(init_q, 2, 3, True)
                    print(init_q)

            except websockets.exceptions.ConnectionClosed:
                print("Connection Closed")
                break
        
asyncio.get_event_loop().run_until_complete(consumer())




