import serial
import time
import sched
import sys
import re
import operator

args = sys.argv

if len(args) != 2:
    print('Include first arguement as event sequence file path, second arguement as video save path')
   # sys.exit()


#event_loc = args[0]
#save_loc = args[1] 

ser = serial.Serial('/dev/ttyACM0',9600)

scheduler = sched.scheduler(time.time, time.sleep)

def print_event(name):
    print ('Event: ', time.time(), name)

def openChannel(number):
    ser.write(number)
def closeChannel(number):
    ser.write(number)
dict = {}

print ('Cue 1,1 On'.isdigit())

lastOpenTime = 0
pat = '\t'
with open('/home/pi/Desktop/DC_4000ms_single.txt') as f:
    for line in f:
        times = re.split(pat, line)
        for index, val in enumerate(times):
            if index != 0 and (str.strip(val)).isdigit():
                if index % 2 == 1:
                    lastOpenTime = val
                    print index , val
                else:
                    print index, int(val)+int(lastOpenTime)
            
ser.write('3')
print('Start: ', time.time())
scheduler.enter(2,1,print_event, ('1',))
scheduler.enter(2,1,print_event, ('2',))
scheduler.enter(5,1,openChannel, ('3',))

scheduler.run()


