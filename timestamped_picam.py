import picamera
import datetime
import threading

class timestamped_picam(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.opened_ch = 0
        self.cam = picamera.PiCamera() 
       
        self.cam.resolution = (1280,720)
        self.cam.framerate = 30
       # self.cam.start_preview()
        self.cam.annotate_text = 'not recording'
        self.cam.annotate_frame_num = True
        
        
    def millis(self):
        dt = datetime.datetime.now() - self.start_time
        ms = (dt.days *24 *60 * 60 + dt.seconds) * 1000 + dt.microseconds / 1000.0
        return ms

    def run(self, name, runtime):
        print("recording stuff")
        self.cam.start_recording(name + '.h264')
        self.tsFile = open(name + '.ts.csv','w')
        self.start_time = datetime.datetime.now()
        
        while self.millis() < (runtime * 1000):
            self.cam.annotate_text = str(round(self.millis(),0)) + ', ' + str(bin(self.opened_ch))[2:].zfill(8)
            self.tsFile.write(self.cam.annotate_text)
            self.tsFile.write(',')
            self.tsFile.write(str(self.cam.frame.index))
            self.tsFile.write('\n')
            #self.cam.wait_recording(0) #this will raise an exception if encoding exception occurs
        self.cam.stop_recording()

    def par_run(self, name,runtime):
        print("in par run")
        threading.Thread(target = self.run,args = (name, runtime)).start()
