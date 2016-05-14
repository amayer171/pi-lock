import time
import RPi.GPIO as GPIO

class PiServo():
    CONST_PIN = 21
    CONST_SUCCESS = "success"
    CONST_ERROR = "error"	
    OPEN_DC = 7 
    CLOSE_DC = 1.5 
    FREQ = 50 #Hz 
    SLEEP_SECONDS = 1.5
    def unlock(self):
        pin = self.setup()
        self.open(pin)
        self.endAction(pin)
    
    def lock(self):
        pin = self.setup()
        self.close(pin)
        self.endAction(pin) 
   
    def open(self, pin):
        pin.start(self.OPEN_DC)
        pin.ChangeFrequency(self.FREQ)
        pin.ChangeDutyCycle(self.OPEN_DC) 
        time.sleep(self.SLEEP_SECONDS)
        pin.stop()
        print("Open")

    def close(self, pin):
        pin.start(self.CLOSE_DC)
        pin.ChangeFrequency(self.FREQ)
        pin.ChangeDutyCycle(self.CLOSE_DC) 
        time.sleep(self.SLEEP_SECONDS)
        pin.stop()
        print("Closed")

    def endAction(self, pin):
        pin.stop()
        GPIO.cleanup()
        return self.CONST_SUCCESS

    def setup(self):
        #GPIO.setmode(GPIO.BOARD)
        GPIO.setmode(GPIO.BCM) #BCM (numbers on breakout board) or BOARD (linear numbering of pins)
        GPIO.setup(self.CONST_PIN, GPIO.OUT)
		
        pin = GPIO.PWM(self.CONST_PIN, self.FREQ) #channel=CONST_PIN, frequency=50Hz
        return pin

if __name__ == "__main__":
    # execute only if run as a script
    servo = PiServo()
    pin = servo.setup()
    try:	
        while(True):
            time.sleep(2)
            print("Opening...")
            servo.open(pin)
            time.sleep(2)
            print("Closing...")
            servo.close(pin)
    
    except KeyboardInterrupt:
        servo.endAction(pin) 
        print ("\nKeyboard Interrupt detected\n")
