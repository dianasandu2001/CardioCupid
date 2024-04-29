from filefifo import Filefifo
from fifo import Fifo
from machine import UART, Pin, I2C, Timer, ADC
from ssd1306 import SSD1306_I2C
from machine import ADC
import time
from piotimer import Piotimer

#debugger
import micropython
micropython.alloc_emergency_exception_buf(200)


i2c = I2C(1, scl=Pin(15), sda=Pin(14), freq=400000)
oled_width = 128
oled_height = 64
oled = SSD1306_I2C(oled_width, oled_height, i2c)
oled.fill(0)

adc_pin = Pin(27)
adc = ADC(adc_pin)

sample = Fifo(500)
def read_input(tid):
    sample.put(adc.read_u16())

tmr = Piotimer(mode = Piotimer.PERIODIC, freq = 250, callback = read_input)

c_val = 0
p_val = 0

DBP = 0
peak = 0

Interval = 0
Frequency = 0
PPI = 0
HR = 0

max_val = 0
min_val = 0
    
#print()
#print("max:", max_val)
#print("min:", min_val)
#print()


#print("threshold:", threshold)
flag = 0
while True:
    while not sample.empty():
    #while True:
        c_val = sample.get()
        #c_val = adc.read_u16()
        
        #Finding the min and max
        if c_val < 0:
            break
        if max_val <= c_val:
            max_val = c_val
        if min_val >= c_val or min_val == 0:
            min_val = c_val
        
        #Finding the threshold
        ave = (min_val +  max_val)/2
        threshold = ave*1.1 ######################## add value to tweek ######################
        
        print("thresh", threshold, "current_value",c_val,"DBD",DBP)##################################################### print
        
        #Detecting peaks
        DBP += 1
        if c_val >= threshold and flag == 0:
            flag = 1
            peak = DBP
            
            PPI = peak * 4 #since we sample one sample every 4 miliseconds
            if PPI < 300 or PPI > 1200:
                break
            HR = 60 / (PPI/1000)
            print("HR",HR, "PPI", PPI) ###################################################################### print
            
            DBP = 0
        elif c_val <= threshold:
            flag = 0
        
        
        #oled.fill(0)
        #oled.text(str(HR),0,0,1)
        #oled.text(str(Interval),0,8,1)
        #oled.text(str(Frequency),0,16,1)
        #oled.show()
            