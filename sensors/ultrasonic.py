from collections import deque
import event

class Ultrasonic(event.EventEmitter):
    def __init__(self, ev, port="COM9"):
        self.serial_arduino = serial.Serial(port, 57600, timeout=1)
        self.trayLength = 30 # in cm
        self.history = deque() # history of reads
        self.historyLength = 20 # history length
        self.emitThreshold = 18 
        super(Ultrasonic, self).__init__(ev)

    def run(self):
        while self.run_flag.is_set():
            self.history.append(self.cupInTray())
            if len(self.history) == self.historyLength + 1:
                self.history.popleft()
                if self.history.count(False) > self.emitThreshold:
                    self.emit('no_cups_on_tray')
        
    def cupInTray():
        duration = ''
        while duration == '': # sometimes a null read is made, make another one
            duration = self.serial_arduino.readline().strip() # read duration in ms for sound to travel to first object and back    
        cm = int(duration) / 29 / 2 # convert to cm
        if cm < self.trayLength:
            return True
        return False
