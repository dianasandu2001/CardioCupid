from filefifo import Filefifo
from fifo import Fifo
from machine import UART, Pin, I2C, Timer, ADC
from ssd1306 import SSD1306_I2C
from machine import ADC
import time

i2c = I2C(1, scl=Pin(15), sda=Pin(14), freq=400000)
oled_width = 128
oled_height = 64
oled = SSD1306_I2C(oled_width, oled_height, i2c)
oled.fill(0)

adc_pin = Pin(26)
adc = ADC(adc_pin)

samples = Fifo(1000)
def read_input():
    samples.put(adc.read_u16())

c_val = 0
p_val = 0

DBP = 0
c_peak = 0
p_peak = 0

Interval = 0
Frequency = 0
PPI = 0
HR = 0

samples = Fifo(1000)

max_val = 0
min_val = 0

for i in range(1000):
    samples.put(adc.read_u16())
    c_val = samples.get()
#     print(c_val)
    if max_val <= c_val:
        max_val = c_val
    if min_val >= c_val or min_val == 0:
        min_val = c_val
    
#print()
#print("max:", max_val)
#print("min:", min_val)
#print()

ave = (min_val +  max_val)/2
threshold = ave*1

#print("threshold:", threshold)
flag = 0
while True:
    samples.put(adc.read_u16())
    c_val = samples.get()
    print("thresh", threshold, "current_value",c_val)
    DBP += 1
    
    if c_val >= threshold and flag == 0:
        flag = 1
        
        c_peak = DBP - p_peak
        p_peak = DBP

        Interval = c_peak/250
        if Interval !=0 :
            Frequency = 1/Interval
            PPI = DBP * Interval
            HR = 60 / (PPI/1000)
            print("HR",HR)
            
        DBP = 0
    elif c_val <= threshold:
        flag = 0
    
    oled.fill(0)
    oled.text(str(HR),0,0,1)
    oled.text(str(Interval),0,8,1)
    oled.text(str(Frequency),0,16,1)
    oled.show()
    
    
    time.sleep(0.1)


