import socket
import sys
import tkinter as tk

host = '192.168.89.129'
port = 29999
timeout = 5
connected = False

def getfeedback(labelup):
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
    labelup.set(collected.decode("utf-8"))
    if collected.decode("utf-8") == "Disconnected":
        connected = False
    #    lconn_text.set("Disconnected")



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

