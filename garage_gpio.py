import time
import RPi.GPIO as GPIO
import sys

class PiPin():
    CONST_PIN = 21
    SLEEP_SECONDS = 2.5
    def send_signal(self):
        self.setup()
        GPIO.output(self.CONST_PIN, GPIO.LOW)
        print("LOW")
        time.sleep(self.SLEEP_SECONDS)
        GPIO.output(self.CONST_PIN, GPIO.HIGH)
        print("HIGH")
        
    def setup(self):
        #GPIO.setmode(GPIO.BOARD)
        GPIO.setmode(GPIO.BCM) #BCM (numbers on breakout board) or BOARD (linear numbering of pins)
        GPIO.setup(self.CONST_PIN, GPIO.OUT, initial=GPIO.HIGH)

    def cleanup(self):
        GPIO.cleanup()
	    
if __name__ == "__main__":
    # execute only if run as a script
    pin = PiPin()
    try:
        pin.setup()
        GPIO.setup(20, GPIO.OUT)
        GPIO.setup(16, GPIO.OUT)
        GPIO.output(20, GPIO.HIGH)
        GPIO.output(16, GPIO.LOW)
        
        	
        while(True):
            print("Press any key to send signal.")
            sys.stdin.readline()
    
            pin.send_signal() 
            print("done.")
    
    except:
        pin.cleanup() 
        print("cleaned up after exception.")
