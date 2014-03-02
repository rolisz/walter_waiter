from collections import deque
import serial
import event

class Ultrasonic(event.EventEmitter):
    # def __init__(self, ev, port="COM9"):
    def __init__(self, ev, port="/dev/ttyACM0"):
        self.serial_arduino = serial.Serial(port, 57600, timeout=1)
        self.trayLength = 30 # in cm
        self.history = deque() # history of reads
        self.historyLength = 20 # history length
        self.emitThreshold = 18
        self.ev = ev
        super(Ultrasonic, self).__init__(ev)

    def run(self):
        print self.ev.run_flag.is_set()
        while self.ev.run_flag.is_set():
            self.history.append(self.cupInTray())
            if len(self.history) == self.historyLength + 1:
                self.history.popleft()
                if self.history.count(False) > self.emitThreshold:
                    print 'no_cups_on_tray'
                    self.emit('no_cups_on_tray')

    def cupInTray(self):
        duration = ''
        for i in range(10): # sometimes a null read is made, make another one
            duration = self.serial_arduino.readline().strip() # read duration in ms for sound to travel to first object and back
            if duration != '':
                break
        if duration == '':
            return False
        try:
            cm = int(duration) / 29 / 2 # convert to cm
        except ValueError:
            return False
        if cm < self.trayLength:
            return True
        return False
