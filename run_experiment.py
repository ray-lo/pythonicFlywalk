import serial
import time
import sched
import sys
import re
import operator
import os
from timestamped_picam import timestamped_picam
import thread
import datetime as dt

def bytePow(base, power):
    ans = 1
    for x in range(0,power):
        ans = ans * base
    print (ans)
    return ans

args = sys.argv


if len(args) < 6:
    print('Include<save location> <trial duration> <intertrial duration> <event_seq_file_1> <number of repeats>...(optional more arguements for more than one event_seq file)')
    print(len(args))
    sys.exit()
event_seqs = []
event_locs = []
trial_repeats = []
for i in range(4, len(args)):
    print(i)
    if i % 2 == 0:
        event_seqs.append(args[i])
        event_locs.append(os.path.dirname(os.path.realpath(__file__)) + '/event_sequence_files/' + args[i])
    else:
        print('here')
        trial_repeats.append(int(args[i]))

print trial_repeats

save_loc = os.path.dirname(os.path.realpath(__file__)) + '/' + dt.datetime.now().strftime("%Y-%m-%d %H:%M") + '/' + args[1]
                                                                   
if not os.path.exists(os.path.dirname(save_loc)):
    os.makedirs(os.path.dirname(save_loc))
    
                                                                   
trial_duration = int(args[2])
break_time = int(args[3])

print(save_loc)
ser = serial.Serial('/dev/ttyACM0',9600)

scheduler = sched.scheduler(time.time, time.sleep)

#create the controller class
vidcontrol = timestamped_picam()
opened_ch = 0
vidcontrol.opened_ch = opened_ch
def print_event(name):
    print ('Event: ', time.time(), name)

def openChannel(number):
    print ('Open: ', time.time(), number)
    global opened_ch
    opened_ch = opened_ch | bytePow(2,int(number)-1)
    global vidcontrol
    vidcontrol.opened_ch = opened_ch
    ser.write(number)
def closeChannel(number):
    print ('Close: ', time.time(), number)
    global opened_ch
    opened_ch = opened_ch & ~bytePow(2,int(number)-1)
    global vidcontrol
    vidcontrol.opened_ch = opened_ch
    print (bin(opened_ch))
    
    number = str(chr(int(number)+96))
    print(number)
    
    ser.write(number)

def print_progress(trials_done):
    print("Performing Trial #" +str(trials_done))
#print (os.path.dirname(sys.argv[0])
       
dict = {}


total_trial_time = trial_duration + break_time

pat = '\t'

print (os.path.dirname(os.path.realpath(__file__)))
trials_done = 0
elapsed_time = 0
seq_number = 0
for el in event_locs:
    print(seq_number)
    for trial_number in range(1,trial_repeats[seq_number] + 1):
        print("e_t:" + str(elapsed_time))
        trials_done = trials_done + 1
        scheduler.enter(elapsed_time, 1, print_progress, (trials_done,))
        scheduler.enter(elapsed_time, 1, vidcontrol.par_run,((save_loc + "-" + event_seqs[seq_number] + "-" + str(trial_number)), trial_duration))
        with open(el) as f:
            endTime = 0
            lastOpenTime = 0
            for line in f:
                times = re.split(pat, line)
                for index, val in enumerate(times):
                    if index != 0 and (str.strip(val)).isdigit():
                        if index % 2 == 1:
                            lastOpenTime = val
                            scheduler.enter(elapsed_time + int(val)/1000.0,1,openChannel, (str((index+1)/2),))
                            print("dude:"  +str(elapsed_time+ int(val)/1000.0))
                               
                        else:
                            scheduler.enter(elapsed_time+ (int(val)+int(lastOpenTime))/1000.0,1,closeChannel, (str((index+1)/2),))
                            endTime = float(val)
                            print("yeah:"  +str(elapsed_time+ (int(val)+int(lastOpenTime))/1000.0))
        elapsed_time = elapsed_time + total_trial_time 
    ++seq_number

print('Start: ', time.time())

#start raspivid
print ('Starting Experiment')
scheduler.run()



