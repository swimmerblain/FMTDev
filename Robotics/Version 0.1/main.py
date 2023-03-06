import os
from multiprocessing import Process
import time
from datetime import datetime

#call Producer function // future function
#Producer function sends all feedback to the main server
#this includes current arm position, current hand position and state of outputs
#def Producer():
#    os.system("ArmHandFeedback.py")

#call Consumer function // future fuction
#Consumer fuction reads the data send from the server and send it to the hand/arm respectivly 
#this would be for digital outputs, arm position, and hand position
#def Consumer():
#    os.system("ArmHandControl.py")

#call arm Client // original function
# client will read arm and hand position from the server and move the arm and hand where they need to go
# client will also send the feedback positions to the server
def Client():
    os.system("Armclient.py")

def handpro():
    os.system("/qbsofthand_industry_api_1.0.3/build/qbsofthand_industry_api_example")

if __name__ == '__main__':
    #due to process randomly failing we will create processes for each function.  if the process is no longer alive we can start it again
    # also want to count how many times the process fails
    
    #future function call
    #prod = Process(target = Producer)

    #future fuction call
    #con = Process(target = Consumer)
    
    #SNA demo function call
    client = Process(target = Client)

    hand = Process(target = handpro)

    #start the different processes
    #if the IP address is not currently reachable this will initially fail but the keep alive will start it again
    #prod.start()
    #con.start()
    client.start()
    hand.start()

    #run is use if we want to stop the process's set run to false
    run = True
    # failCNT count how many times the service fails
    #will want to output these to a log file
    prodFailCnt = 0
    conFailCnt = 0
    clientFailCnt = 0
    handFailCnt = 0

    #last fail cnt is used for logging. if the fail count is different than last fail count write the time and date to log file and update last fail count
    lastProdFailCnt = 0
    lastConFailCnt = 0
    lastClientFailCnt = 0
    lastHandFailCnt = 0 

    while run:
        """future
        #write date time and fail count to log if failed
        if prodFailCnt != lastProdFailCnt:
            with ('log.txt', 'a') as log:
                log.write("Produced fail count ")
                log.write(datetime.now())
                log.write(" : ", prodFailCnt)
            lastProdFailCnt = prodFailCnt
        """
        """future    
        #write date time and fail count to log if failed
        if conFailCnt != lastConFailCnt:
            with ('log.txt', 'a') as log:
                log.write("Consumed fail count ")
                log.write(datetime.now())
                log.write(" : ", conFailCnt)
            lastConFailCnt = conFailCnt
        """    
        #write date time and fail count to log if failed
        if clientFailCnt != lastClientFailCnt:
            with ('log.txt', 'a') as log:
                log.write("Client fail count ")
                log.write(datetime.now())
                log.write(" : ", clientFailCnt)
            lastClientFailCnt = clientFailCnt
        #write date time and fail count to log if failed
        if handFailCnt != lastHandFailCnt:
            with ('log.txt', 'a') as log:
                log.write("Hand fail count ")
                log.write(datetime.now())
                log.write(" : ", handFailCnt)
            lastHandFailCnt = handFailCnt
        """future
        #check if alive if not increase fail count, terminate process, delete process and start again
        if prod.is_alive() == False:
            print("Produced program faulted")
            prod.terminate()
            del prod
            prod = Process(target = Producer)
            prod.start()
            prodFailCnt += 1
        """
        """future
        #check if alive if not increase fail count, terminate process, delete process and start again
        if con.is_alive() == False:
            print("Consumer program faulted")
            con.terminate()
            del con
            con = Process(target = Consumer)
            con.start()
            conFailCnt += 1
        """
        #check if alive if not increase fail count, terminate process, delete process and start again
        if client.is_alive() == False:
            print("client program faulted")
            client.terminate()
            del client
            client = Process(target = Client)
            client.start()
            clientFailCnt += 1
        #check if alive if not increase fail count, terminate process, delete process and start again
        if hand.is_alive() == False:
            print("hand program faulted")
            hand.terminate()
            del hand
            hand = Process(target = handpro)
            hand.start()
            handFailCnt += 1
        


        
        



