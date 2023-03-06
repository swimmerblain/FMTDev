import os
from multiprocessing import Process
import time
from datetime import datetime

#function to get dashboard in formation from rover.  Robot should be in remote mode before using these
def dashboardstr():
    os.system("python dashboard.py")

def controlstr():
    os.system("python ArmCTRL.py")
   
if __name__ == '__main__':
    #general run.  goes to false to stop the program
    run = True
    
    #create dashboard process to read data from arm
    dashboard = Process(target = dashboardstr)
    dashboard.start()
    dashFailCnt = 0
    lastDashFailCnt = 0

    #create Arm Control process to send arm/hand position
    control = Process(target = controlstr)
    control.start()
    ctrlFailCnt = 0
    lastctrlFailCnt = 0
    
    while run:
        
        #check if dashboard has failed and restart 
        #write fail count to log
        if dashboard.is_alive() == False:
            print("dashboard has failed")
            dashboard.terminate()
            del dashboard
            dashboard = Process(target = dashboardstr)
            dashboard.start()
            dashFailCnt += 1
            with open("log.txt", 'a') as log:
                log.write("dashfail count ")
                log.write(str(datetime.now()))
                log.write(" : " + str(dashFailCnt))
                log.write('\n')

        #check if control has failed and restart 
        #write fail count to log
        if control.is_alive() == False:
            print("control has failed")
            control.terminate()
            del control
            control = Process(target = controlstr)
            control.start()
            ctrlFailCnt += 1
            with open("log.txt", 'a') as log:
                log.write("control count ")
                log.write(str(datetime.now()))
                log.write(" : " + str(ctrlFailCnt))
                log.write('\n')
            
    
