import serial
import time
import sched
import sys
import re
import operator
import os
from raspividcontroller import RaspiVidController 


args = sys.argv

if len(args) != 4:
    print('Include <event file location> <save location> <experiment duration>')
    print(len(args))
    sys.exit()


event_loc = os.path.dirname(os.path.realpath(__file__)) + '/' + args[1]
save_loc = os.path.dirname(os.path.realpath(__file__)) + '/' + args[2]
print(save_loc)
ser = serial.Serial('/dev/ttyACM0',9600)

scheduler = sched.scheduler(time.time, time.sleep)

def print_event(name):
    print ('Event: ', time.time(), name)

def openChannel(number):
    print ('Open: ', time.time(), number)
    ser.write(number)
def closeChannel(number):
    print ('Close: ', time.time(), number)
    number = str(chr(int(number)+96))
    print(number)
    ser.write(number)

#print (os.path.dirname(sys.argv[0])
       
dict = {}

lastOpenTime = 0
pat = '\t'
endTime = 0
print (os.path.dirname(os.path.realpath(__file__)))
print (event_loc)
with open(event_loc) as f:
    for line in f:
        times = re.split(pat, line)
        for index, val in enumerate(times):
            if index != 0 and (str.strip(val)).isdigit():
                if index % 2 == 1:
                    lastOpenTime = val
                    scheduler.enter(int(val)/1000,1,openChannel, (str((index+1)/2),))
                   
                else:
                    scheduler.enter((int(val)+int(lastOpenTime))/1000,1,closeChannel, (str((index+1)/2),))
                    endTime = int(val)
                

print('Start: ', time.time())
scheduler.run()
#create the controller class
vidcontrol = RaspiVidController(save_loc, args[3]*1000, False)

#start raspivid
vidcontrol.start()

#DO SOME STUFF

#stop raspivid 
vidcontrol.stopController()

