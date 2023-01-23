import os
from multiprocessing import Process
import time
from datetime import datetime

#function to get dashboard in formation from rover.  Robot should be in remote mode before using these
def dashboardstr():
    os.system("dashboard.py")
   
if __name__ == '__main__':
    #general run.  goes to false to stop the program
    run = True
    
    #create dashboard process to read data from arm
    dashboard = Process(target = dashboardstr)
    dashboard.start()
    dashFailCnt = 0
    lastDashFailCnt = 0
    
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
            with ('log.txt', 'a') as log:
                log.write("dashfail count ")
                log.write(datetime.now())
                log.write(" : ", dashFailCnt)
            
    
