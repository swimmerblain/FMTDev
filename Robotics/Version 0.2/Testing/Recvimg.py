import time
import asyncio
import websockets
import json
import cv2
import base64
import numpy as np

HOST = "ws://localhost:4008"



async def start():
    async with websockets.connect(HOST) as rgbSocket:
        print("connected!")
        while True:

            message = await rgbSocket.recv()
            #print(message.size())
            #message = await rgbSocket.recv()
            #test1 = int.from_bytes(message)
            #print(test1)
            #header, data = encoded_image.split(',',1)
            #image_data = base64.b64decode(message)
            #image_data = int(message
            #print(image_data)
            shape = (384,216)
            #print(np_array)
            np_array = np.frombuffer(message, dtype=np.uint8)
            #np_array = np.fromstring(message, dtype=np.uint8)
            if (len(np_array) > 1):
                #print(np_array.shape)
                
                #imagep = cv2.imdecode(np_array, cv2.IMREAD_UNCHANGED)
                imagep = cv2.imdecode(np_array, flags=1)
                #print(imagep)
                #cv2.imshow('rgb3', imagep
                test1 = cv2.resize(imagep, (384, 216), interpolation=cv2.INTER_AREA)
                cv2.imshow('rgb4', test1)
                cv2.waitKey(10)
            #print(message)

async def main():
    videoTask = asyncio.create_task(start())
    while True:
        await asyncio.sleep(0.001)



asyncio.run(main())
