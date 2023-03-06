import socket
import sys
import tkinter as tk
import websockets
import json
import asyncio
import time


host = '192.168.89.129'
port = 29999
timeout = 5
connected = False

server = 'ws://localhost:4007'

#server = 'ws://vast-flies-stay-162-191-47-209.loca.lt'
#server = 'ws://10.5.100.136:4007'


unlock = "Unknown"
quit = "unknown"

#send all messages to the web socket
'''
pull the following once a second and send (possibly adjust time)
robotmode
polyscopeversion
safetystatus
is in remote control
get serial number
get robot model number

following are status sent but not updated ever XX time
Unlocking protective stop


The following are commands that can be sent to the robot
shutdown
power on
power off
brake release
unlock protective stop
restart safety
quit

the following is a command sent to initially connect to the roboto
robot must be powered on first
'''

#define the data part of the message to send
data = {
            "Connected": connected,
            "robotmode": "Unknown",
            "Polyscope Version": "Unknown",
            "SafetyStatus": "Unknown",
            "In Remote": "Unknown",
            "Serial": "Unknown",
            "model": "Unknown",
            "Unlocking Protective": "Unknown",
            "Quit": "Unknown"
            }
msg = {'msg': 'dashboardData', 'data': data}
 

async def getfeedback():
    global sock
    global connected
    collected = b''
    while True:
        part = sock.recv(1)
        if part != b"\n":
            collected += part
        elif part == b"\n":
            break
    #print(collected.decode("utf-8"))
    if collected.decode("utf-8") == "Disconnected":
        connected = False
    return collected.decode("utf-8")
    #    lconn_text.set("Disconnected")

async def sockconnect():
    global sock
    global connected
    connected = False
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(timeout)
    sock.connect((host,port))
    print(sock.recv(1096))
    connected = True
    print(connected)
    
async def producer():
    global sock
    global connected
    global data
    global msg
    global unlock
    global quit
    #connect to socket
    #await sockconnect()
    connected = False
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(timeout)
    sock.connect((host,port))
    print(sock.recv(1096))
    connected = True
    async with websockets.connect(server) as websocket:
        while True:
            try:
                # get all the data needed to send
                data['Connected'] = connected
                if connected:
                    sock.sendall(('robotmode\n').encode())
                    robotmode = await getfeedback()
                    #Polyscope Version
                    sock.sendall(('PolyscopeVersion\n').encode())
                    Polyscope = await getfeedback()
                    #safety Status
                    sock.sendall(('safetystatus\n').encode())
                    safetystat = await getfeedback()
                    #In Remote
                    sock.sendall(('is in remote control\n').encode())
                    remote = await getfeedback()
                    #Serial
                    sock.sendall(('get serial number\n').encode())
                    serial = await getfeedback()
                    #model
                    sock.sendall(('get robot model\n').encode())
                    model = await getfeedback()


                data['robotmode'] = robotmode
                data['Polyscope Version'] = Polyscope
                data['SafetyStatus'] = safetystat
                data['In Remote'] = remote
                data['Serial'] = serial
                data['model'] = model
                data['Unlocking Protective'] = unlock
                data['Quit'] = quit
                msg['data'] = data
                #print(msg)
                await websocket.send(json.dumps(msg))
                await asyncio.sleep(1)
            except websockets.exeptions.ConnectionClosed:
                print('Connection Closed')
                break
                
async def consumer():
    global unlock
    global quit
    async with websockets.connect(server) as websocket:
        while True:
            try:
                message = await websocket.recv()
                msgData = json.loads(message)
                msgdata2 = json.dumps(message)
                #print("data")
                #print(message)
                #print(msgData)
                #print(msgdata2)
                    
                if 'msg' in msgData:
                    print("msg recieved")
                    if msgData['msg'] == 'dashboardCMD':
                        print(msgData['data'])

                        if msgData['data'] == "shutdown":
                            sock.sendall(('shudown\n').encode())
                        elif str(msgData['data']) == "power off":
                            sock.sendall(('power off\n').encode())
                            await getfeedback()
                        elif str(msgData['data']) == "power on":
                            print("powered on")
                            sock.sendall(('power on\n').encode())
                            await getfeedback()
                        elif msgData['data'] == "brake release":
                            sock.sendall(('brake release\n').encode())
                            await getfeedback()
                        elif msgData['data'] == "unlock protective stop":
                            sock.sendall(('unlock protective stop\n').encode())
                            unlock = await getfeedback()
                        elif msgData['data'] == "restart safety":
                            sock.sendall(('restart safety\n').encode())
                            await getfeedback()
                        elif msgData['data'] == "quit":
                            sock.sendall(('quit\n').encode())
                            quit = await getfeedback()
                        else:
                            print("unknown command ", str(msgData['data']))


                    #print("True")
                    #Unlocking Protective
                    #sock.sendall(('unlock protective stop\n').encode())
                    #unlock = await getfeedback()
                    #Quit
                    #sock.sendall(('quit\n').encode())
                    #quit = await getfeedback()


            except websockets.exeptions.ConnectionClosed:
                print('Connection Closed')
                break
                
async def handle():
    consumer_task = asyncio.ensure_future(consumer())
    producer_task = asyncio.ensure_future(producer())
    done, pending = await asyncio.wait([consumer_task, producer_task], return_when = asyncio.FIRST_COMPLETED,)
    for task in pending:
        task.cancel()
        
asyncio.get_event_loop().run_until_complete(handle())


'''
def sockconnect():
    global sock
    global connected
    connected = False
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(timeout)
    sock.connect((host,port))
    print(sock.recv(1096))
    connected = True
    print(connected)
    lconn_text.set("Connected")

def sockclose():
    global sock
    global connected
    print(connected)
    if connected == True:
        sock.sendall(('quit\n').encode())
        getfeedback(lconn_text)
    print(connected)

def sockrun():
    global sock
    global connected
    if connected:
        print('here')
        sock.sendall(('running\n').encode())
        getfeedback(lrun_text)

def sockshut():
    global sock
    global connected
    if connected:
        sock.sendall(('shutdown\n').encode())
        getfeedback(lrun_text)


def sockmode():
    global sock
    global connected
    if connected:
        sock.sendall(('robotmode\n').encode())
        getfeedback(lmode_text)
    win.after(1000, sockmode)


def sockver():
    global sock
    global connected
    if connected:
        sock.sendall(('PolyscopeVersion\n').encode())
        getfeedback(lver_text)

def sockon():
    global sock
    global connected
    if connected:
        sock.sendall(('power on\n').encode())
        getfeedback(lon_text)

def sockoff():
    global sock
    global connected
    if connected:
        sock.sendall(('power off\n').encode())
        getfeedback(loff_text)

def sockbrake():
    global sock
    global connected
    if connected:
        sock.sendall(('brake release\n').encode())
        getfeedback(lbrake_text)

def socksafe():
    global sock
    global connected
    if connected:
        sock.sendall(('safetystatus\n').encode())
        getfeedback(lsafe_text)

def sockunlockprotective():
    global sock
    global connected
    if connected:
        sock.sendall(('unlock protective stop\n').encode())
        getfeedback(lunlockprotective_text)

def sockrestartsafe():
    global sock
    global connected
    if connected:
        sock.sendall(('restart safety\n').encode())
        getfeedback(lrestartsafe_text)


def sockremote():
    global sock
    global connected
    if connected:
        sock.sendall(('is in remote control\n').encode())
        getfeedback(lremote_text)

def sockserial():
    global sock
    global connected
    if connected:
        sock.sendall(('get serial number\n').encode())
        getfeedback(lserial_text)

def sockmodel():
    global sock
    global connected
    if connected:
        sock.sendall(('get robot model\n').encode())
        getfeedback(lmodel_text)


win = tk.Tk()
win.geometry("500x550")
bconn = tk.Button(win, text="Connect", command=sockconnect)
bconn.grid(row = 1, column = 1)
lconn_text = tk.StringVar()
lconn_text.set("Disconnected")
lconn = tk.Label(win, textvariable=lconn_text)
lconn.grid(row = 1, column = 3)
bclose = tk.Button(win, text="Close", command=sockclose)
bclose.grid(row = 1,  column = 2)

brun = tk.Button(win, text="Running", command=sockrun)
brun.grid(row=2, column =1)
lrun_text = tk.StringVar()
lrun_text.set("Unknown")
lrun = tk.Label(win, textvariable = lrun_text)
lrun.grid(row=2, column=3)

bshut = tk.Button(win, text="Shutdown", command=sockshut)
bshut.grid(row=3, column =1)
lshut_text = tk.StringVar()
lshut_text.set("Unknown")
lshut = tk.Label(win, textvariable = lshut_text)
lshut.grid(row=3, column=3)

bmode = tk.Button(win, text="Robot Mode", command=sockmode)
bmode.grid(row=4, column =1)
lmode_text = tk.StringVar()
lmode_text.set("Unknown")
lmode = tk.Label(win, textvariable = lmode_text)
lmode.grid(row=4, column=3)

bver = tk.Button(win, text="Polyscope Version", command=sockver)
bver.grid(row=5, column =1)
lver_text = tk.StringVar()
lver_text.set("Unknown")
lver = tk.Label(win, textvariable = lver_text)
lver.grid(row=5, column=3)

bon = tk.Button(win, text="Power On", command=sockon)
bon.grid(row=6, column =1)
lon_text = tk.StringVar()
lon_text.set("Unknown")
lon = tk.Label(win, textvariable = lon_text)
lon.grid(row=6, column=3)

boff = tk.Button(win, text="Power Off", command=sockoff)
boff.grid(row=7, column =1)
loff_text = tk.StringVar()
loff_text.set("Unknown")
loff = tk.Label(win, textvariable = loff_text)
loff.grid(row=7, column=3)

bbrake = tk.Button(win, text="Brake Release", command=sockbrake)
bbrake.grid(row=8, column =1)
lbrake_text = tk.StringVar()
lbrake_text.set("Unknown")
lbrake = tk.Label(win, textvariable = lbrake_text)
lbrake.grid(row=8, column=3)

bsafe = tk.Button(win, text="Safety Status", command=socksafe)
bsafe.grid(row=9, column =1)
lsafe_text = tk.StringVar()
lsafe_text.set("Unknown")
lsafe = tk.Label(win, textvariable = lsafe_text)
lsafe.grid(row=9, column=3)

bunlockprotective = tk.Button(win, text="unlock protective", command=sockunlockprotective)
bunlockprotective.grid(row=10, column =1)
lunlockprotective_text = tk.StringVar()
lunlockprotective_text.set("Unknown")
lunlockprotective = tk.Label(win, textvariable = lunlockprotective_text)
lunlockprotective.grid(row=10, column=3)

brestartsafe = tk.Button(win, text="Restart Safety", command=sockrestartsafe)
brestartsafe.grid(row=11, column =1)
lrestartsafe_text = tk.StringVar()
lrestartsafe_text.set("Unknown")
lrestartsafe = tk.Label(win, textvariable = lrestartsafe_text)
lrestartsafe.grid(row=11, column=3)

bremote = tk.Button(win, text="Robot In Remote?", command=sockremote)
bremote.grid(row=12, column =1)
lremote_text = tk.StringVar()
lremote_text.set("Unknown")
lremote = tk.Label(win, textvariable = lremote_text)
lremote.grid(row=12, column=3)

bserial = tk.Button(win, text="Serial Number", command=sockserial)
bserial.grid(row=13, column =1)
lserial_text = tk.StringVar()
lserial_text.set("Unknown")
lserial = tk.Label(win, textvariable = lserial_text)
lserial.grid(row=13, column=3)

bmodel = tk.Button(win, text="Robot Model", command=sockmodel)
bmodel.grid(row=14, column =1)
lmodel_text = tk.StringVar()
lmodel_text.set("Unknown")
lmodel = tk.Label(win, textvariable = lmodel_text)
lmodel.grid(row=14, column=3)







win.mainloop()

sock.sendall(('is in remote control' + '\n').encode())
collected = b''
while True:
    part = sock.recv(1)
    if part != b"\n":
        collected += part
    elif part == b"\n":
        break
print(collected.decode("utf-8"))
sock.close()

'''
