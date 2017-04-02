import time
import RPi.GPIO as GPIO

class PiPin():
    CONST_PIN = 21
    SLEEP_SECONDS = 1.5
    def send_signal(self):
        self.setup()
        GPIO.output(self.CONST_PIN, GPIO.HIGH)
        time.sleep(self.SLEEP_SECONDS)
        GPIO.output(self.CONST_PIN, GPIO.LOW)
        GPIO.cleanup()
        
    def setup(self):
        #GPIO.setmode(GPIO.BOARD)
        GPIO.setmode(GPIO.BCM) #BCM (numbers on breakout board) or BOARD (linear numbering of pins)
        GPIO.setup(self.CONST_PIN, GPIO.OUT, initial=GPIO.LOW)
	    
if __name__ == "__main__":
    # execute only if run as a script
    pin = PiPin()
    try:	
        while(True):
            time.sleep(2)
            print("signaling...")
            pin.send_signal() 
            print("done.")
    
    except KeyboardInterrupt:
        GPIO.cleanup() 
        print ("\nKeyboard Interrupt detected\n")
