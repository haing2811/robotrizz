from pybricks.hubs import PrimeHub
from pybricks.pupdevices import Motor, ColorSensor, UltrasonicSensor, ForceSensor
from pybricks.parameters import Button, Color, Direction, Port, Side, Stop
from pybricks.robotics import DriveBase
from pybricks.tools import wait, StopWatch, multitask, run_task
from pybricks.iodevices import PUPDevice

hub = PrimeHub()

s2 = ColorSensor(Port.D) 
s2raw = PUPDevice(Port.D)

async def Color_Print(c):
    if c==1: hub.light.on(Color.BLACK)
    elif c==2: hub.light.on(Color.BLUE)
    elif c==3: hub.light.on(Color.GREEN)
    elif c==4: hub.light.on(Color.YELLOW)
    elif c==5: hub.light.on(Color.RED)
    else: hub.light.on(Color.WHITE)
    
async def Color_Measure():
    r = 0; g = 0; b = 0; w = 0; h = 0; s = 0; v = 0
    while True:
        c = [0, 0, 0, 0, 0, 0, 0]
        for i in range(50):
            s2rgb = await s2raw.read(5)
            s2hsv = await s2.hsv()
            r = s2rgb[0]; g = s2rgb[1]; b = s2rgb[2]; w = s2rgb[3]
            h = s2hsv[0]; s = s2hsv[1]; v = s2hsv[2]
            
            if r+g+b < 10: c[0] = c[0] + 0.5                        #NONE
            elif r > 2*g: c[5] = c[5] + 1                           #RED
            elif r > 1.75*b: c[4] = c[4] + 1                        #YELLOW
            elif g > 1.5*r and 130 < h < 175: c[3] = c[3] + 1       #GREEN
            elif b > 1.8*r: c[2] = c[2] + 1                         #BLUE
            elif r < 50 and g < 50 and b < 50: c[1] = c[1] + 1      #BLACK
            else: c[6] = c[6] + 1                                   #WHITE

        i = 0; max = c[0]; best = 0 
        for i in range(7):  
            if c[i]>max: max = c[i]; best = i
        if best == 0: hub.light.off()
        if best != 0: await Color_Print(best)
        print("\r" + str(best), end="")
        await wait(250)