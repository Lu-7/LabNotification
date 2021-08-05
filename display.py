#!/usr/bin/env python
# -*- coding: utf-8 -*-
import time
 
import Adafruit_GPIO.SPI as SPI
import Adafruit_SSD1306
 
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
 
import subprocess

class display:
    def __init__(self):
        RST = None     # on the PiOLED this pin isnt used
        self.disp = Adafruit_SSD1306.SSD1306_128_64(rst=RST, i2c_address=0x3C)
        self.width = self.disp.width
        self.height = self.disp.height
        self.image = Image.new('1', (self.width, self.height))
        self.draw = ImageDraw.Draw(self.image)
        self.setup()
        self.testShow()

    def setup(self):
        
        self.disp.begin()
        self.disp.clear()
        self.disp.display()
        self.draw.rectangle((0,0,self.width,self.height), outline=0, fill=0)
        

    def testShow(self):
            x = 0
            padding = -2
            top = padding
            bottom = self.height-padding
            font = ImageFont.load_default()

            self.draw.rectangle((0,0,self.width,self.height), outline=0, fill=0)

            cmd = "hostname -I | cut -d\' \' -f1"
            IP = subprocess.check_output(cmd, shell = True )
            cmd = "top -bn1 | grep load | awk '{printf \"CPU Load: %.2f\", $(NF-2)}'"
            CPU = subprocess.check_output(cmd, shell = True )
            cmd = "free -m | awk 'NR==2{printf \"Mem: %s/%sMB %.2f%%\", $3,$2,$3*100/$2 }'"
            MemUsage = subprocess.check_output(cmd, shell = True )
            cmd = "df -h | awk '$NF==\"/\"{printf \"Disk: %d/%dGB %s\", $3,$2,$5}'"
            Disk = subprocess.check_output(cmd, shell = True )
        
        
            self.draw.text((x, top),       "IP: " + str(IP),  font=font, fill=255)
            self.draw.text((x, top+8),     str(CPU), font=font, fill=255)
            self.draw.text((x, top+16),    str(MemUsage),  font=font, fill=255)
            self.draw.text((x, top+25),    str(Disk),  font=font, fill=255)
        
            # Display image.
            self.disp.image(self.image)
            self.disp.display()
            time.sleep(.1)


    def show(self,number,status):
            x = 0
            padding = -2
            top = padding
            bottom = self.height-padding
            FONT_SANS_30 = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 30)
            FONT_SANS_20 = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 20)
            self.draw.rectangle((0,0,self.width,self.height), outline=0, fill=0)
    
            self.draw.text((x, top),       number,  font=FONT_SANS_20, fill=255)
            self.draw.text((x, top+30),       status,  font=FONT_SANS_30, fill=255)

            # Display image.
            self.disp.image(self.image)
            self.disp.display()
            time.sleep(.1)
        
