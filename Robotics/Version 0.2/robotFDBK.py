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
#server = 'wss://192.168.1.45:4007'
server = 'ws://localhost:4007'


RobotFeedback = {
    'ActualCurrent' : "",
    'ActualDigitalInputbits': "",
    'ActualDigitalOutputBits' : "",
    'ActualExecutionTime' : "",
    'ActualJointVoltage' : "",
    'ActualMainVoltage' : "",
    'ActualMomentum' : "",
    'ActualQ' : "",
    'ActualQd' : "",
    'ActualRobotcurrent' : "",
    'ActualRobotVoltage' : "",
    'ActualTCPForce' : "",
    'ActualTCPPose' : "",
    'ActualTCPSpeed' : "",
    'ActualToolAccelerometer' : "",
    'DigitalOutState' : "",
    'FtRawWrench' : "",
    'JointControlOutput' : "",
    'JointMode' : "",
    'JointTemperatures' : "",
    'OutputDoubleRegister' : "",
    'OutputIntRegister' : "",
    'Payload' : "",
    'PayloadCog' : "",
    'PayloadInertia' : "",
    'RobotMode' : "",
    'RobotStatus' : "",
    'RuntimeState' : "",
    'SafetyMode' : "",
    'SafetyStatusBits' : "",
    'SpeedScaling' : "",
    'SpeedScalingCombined' : "",
    'StandardAnalogInput0' : "",
    'StandardAnalogInput1' : "",
    'StandardAnalogOutput0' : "",
    'StandardAnalogOutput1' : "",
    'TargetCurrent' : "",
    'TargetMoment' : "",
    'TargetQ' : "",
    'TargetQd' : "",
    'TargetQdd' : "",
    'TargetSpeedFraction' : "",
    'TargetTCPPose' : "",
    'TargetTCPSpeed' : "",
    'Timestamp' : "",
    'initPeriod' : "",
    'Connected' : "",
    'EmergencyStopped': "",
    'ProtectiveStopped' : ""
}

async def producer():    
    # when using SSL you ned to run the top async text to essentially ignore the ssl protocol
    #async with websockets.connect(server, ssl=ssl.SSLContext(protocol=ssl.PROTOCOL_TLS)) as websocket:
    
    # run this line when you have no SSL when running on local host
    async with websockets.connect(server) as websocket:
        print("connected to websocket")
        recv = rtde_receive.RTDEReceiveInterface(HOST)
        while True:
            try: 
                RobotFeedback['ActualCurrent'] = recv.getActualCurrent()
                RobotFeedback['ActualDigitalInputbits'] = recv.getActualDigitalInputBits()
                RobotFeedback['ActualDigitalOutputBits'] = recv.getActualDigitalOutputBits()
                RobotFeedback['ActualExecutionTime'] = recv.getActualExecutionTime()
                RobotFeedback['ActualJointVoltage'] = recv.getActualJointVoltage()
                RobotFeedback['ActualMainVoltage'] = recv.getActualMainVoltage()
                RobotFeedback['ActualMomentum'] = recv.getActualMomentum()
                RobotFeedback['ActualQ'] = recv.getActualQ()
                RobotFeedback['ActualQd'] = recv.getActualQd()
                RobotFeedback['ActualRobotCurrent'] = recv.getActualRobotCurrent()
                RobotFeedback['ActualRobotVoltage'] = recv.getActualRobotVoltage()
                RobotFeedback['ActualTCPForce'] = recv.getActualTCPForce()
                RobotFeedback['ActualTCPPose'] = recv.getActualTCPPose()
                RobotFeedback['ActualTCPSpeed'] = recv.getActualTCPSpeed()
                RobotFeedback['ActualToolAccelerometer'] = recv.getActualToolAccelerometer()
                #RobotFeedback['DigitalOutState'] = recv.getDigitalOutState()
                RobotFeedback['FtRawWrench'] = recv.getFtRawWrench()
                RobotFeedback['JointControlOutput'] = recv.getJointControlOutput()
                RobotFeedback['JointMode'] = recv.getJointMode()
                RobotFeedback['JointTemperatures'] = recv.getJointTemperatures()
                #RobotFeedback['OutputDoubleRegister'] = recv.getOutputDoubleRegister()
                #RobotFeedback['OutputIntRegister'] = recv.getOutputIntRegister()
                RobotFeedback['Payload'] = recv.getPayload()
                RobotFeedback['PayloadCog'] = recv.getPayloadCog()
                RobotFeedback['PayloadInertia'] = recv.getPayloadInertia()
                RobotFeedback['RobotMode'] = recv.getRobotMode()
                RobotFeedback['RobotStatus'] = recv.getRobotStatus()
                RobotFeedback['RuntimeState'] = recv.getRuntimeState()
                RobotFeedback['SafetyMode'] = recv.getSafetyMode()
                RobotFeedback['SafetyStatusBits'] = recv.getSafetyStatusBits()
                RobotFeedback['SpeedScaling'] = recv.getSpeedScaling()
                RobotFeedback['SpeedScalingCombined'] = recv.getSpeedScalingCombined()
                RobotFeedback['StandardAnalogInput0'] = recv.getStandardAnalogInput0()
                RobotFeedback['StandardAnalogInput1'] = recv.getStandardAnalogInput1()
                RobotFeedback['StandardAnalogOutput0'] = recv.getStandardAnalogOutput0()
                RobotFeedback['StandardAnalogOutput1'] = recv.getStandardAnalogOutput1()
                RobotFeedback['TargetCurrent'] = recv.getTargetCurrent()
                RobotFeedback['TargetMoment'] = recv.getTargetMoment()
                RobotFeedback['TargetQ'] = recv.getTargetQ()
                RobotFeedback['TargetQd'] = recv.getTargetQd()
                RobotFeedback['TargetQdd'] = recv.getTargetQdd()
                RobotFeedback['TargetSpeedFraction'] = recv.getTargetSpeedFraction()
                RobotFeedback['TargetTCPPose'] = recv.getTargetTCPPose()
                RobotFeedback['TargetTCPSpeed'] = recv.getTargetTCPSpeed()
                RobotFeedback['Timestamp'] = recv.getTimestamp()
                RobotFeedback['initPeriod'] = str(recv.initPeriod())
                RobotFeedback['Connected'] = recv.isConnected()
                RobotFeedback['EmergencyStopped'] = recv.isEmergencyStopped()
                RobotFeedback['ProtectiveStopped'] = recv.isProtectiveStopped()
                
                #init_q = recv.getActualQ()
                msg = {'msg': 'robotFDBK', 'data': (RobotFeedback)}
                #print(json.dumps(msg, indent=2))
                await websocket.send(json.dumps(msg))
                await asyncio.sleep(0.1)
            except websockets.exceptions.ConnectionClosed:
                print("Connection Closed")
                break

asyncio.get_event_loop().run_until_complete(producer())

