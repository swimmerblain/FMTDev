import serial
import time
import json

connection = serial.Serial(port="COM3", baudrate=9600)
connection.reset_input_buffer()
data2 ={}
data2["msg"] = "Aux commands"
data3 ={}
data3["Fan Power"] = 1
data3["PC reset"] = 1
data3["Switch Power"] = 1
data3["Rover Power"] = 1
data3["Hand Power"] = 1
data3["Relay 6"] = 1
data3["Arm On"] = 1
data3["Arm Off"] = 1
data3["Red Light"] = 1
data3["Green Light"] = 1
data3["Blue Light"] = 1
data3["Yellow Light"] = 1
data3["Relay 13"] = 1
data3["Relay 14"] = 1
data3["Relay 15"] = 1
data3["Relay 16"] = 1


data2["data"] = data3
data2 = json.dumps(data2)

while True:
    connection.write(data2.encode('ascii'))
    connection.flush()
    data = connection.readline().decode("utf-8")
    print("data Recieved")
    print(data)
    #try:
    #    dict_json = json.loads(data)
    #    print(dict_json)
    #except json.JSONDecodeError as e:
    #    print("JSON", e)
    connection.flush()
    time.sleep(0.1)
    
