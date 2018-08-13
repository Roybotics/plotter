import serial
import time
import random

class XYPlotter:

    ser = None

    def connect(self):
      try:
        self.ser = serial.Serial('/dev/ttyUSB0', 1000000)
      except:
        try:
          self.ser = serial.Serial('/dev/ttyUSB1', 1000000)
        except:
          self.ser = serial.Serial('/dev/ttyUSB2', 1000000)

      print(self.ser.name)


    def waittofinish(self):
        while self.ser.inWaiting()<4:
          time.sleep(0.000)
        #print(self.ser.inWaiting())
        return self.ser.read(self.ser.inWaiting()) == b"done"

    def gotozero(self):
        self.ser.write(b'0\r')
        return self.waittofinish()
    def gotoxy(self,x,y,dt=400,smooth=0):
        self.ser.write(b'G %3.6f %3.6f %d %3.6f\r' % (x,y,int(dt),smooth))
        return self.waittofinish()
    def movexy(self,dx,dy,dt=400,smooth=0):
        self.ser.write(b'M %3.6f %3.6f %d %3.6f\r' % (dx,dy,int(dt),smooth))
        return self.waittofinish()

    def line(self,ax, ay, bx, by, dt=400):
        self.ser.write(b'L %3.6f %3.6f %3.6f %3.6f %d\r' % (ax, ay, bx, by, int(dt)))
        return self.waittofinish()
    def linemove(self,dx, dy, dt=400):
        self.ser.write(b'V %3.6f %3.6f %d\r' % (dx, dy, int(dt)))
        return self.waittofinish()
    def rectangle(self,rx, ry, w, h, dt=400):
        self.ser.write(b'R %3.6f %3.6f %3.6f %3.6f %d\r' % (rx, ry, w, h, int(dt)))
        return self.waittofinish()
    def bezier(self, x1, x2, x3, x4, y1, y2, y3, y4, dt=400):
        self.ser.write(b'B %3.6f %3.6f %3.6f %3.6f %3.6f %3.6f %3.6f %3.6f %d\r' % (x1, x2, x3, x4, y1, y2, y3, y4, int(dt)))
        return self.waittofinish()
    def circle(self, cx, cy, r, a=0, b=0, sides=0, dt=400):
        self.ser.write(b'C %3.6f %3.6f %3.6f %3.6f %3.6f %d %d\r' % (cx, cy, r, a, b, int(sides), int(dt)))
        return self.waittofinish()
    def spiral(self, cx, cy, r1, r2, a=0, b=0, revs=10, sides=0, dt=400):
        self.ser.write(b'S %3.6f %3.6f %3.6f %3.6f %3.6f %3.6f %d %d %d\r' % (cx, cy, r1, r2, a, b, int(revs), int(sides), int(dt)))
        return self.waittofinish()

    def penup(self):
        self.ser.write(b'U\r')
        return self.waittofinish()
    def pendown(self):
        self.ser.write(b'D\r')
        return self.waittofinish()
    def penoff(self):
        self.ser.write(b'O\r')
        return self.waittofinish()
    
    def pento(self, angle, nbiter=7):
        self.ser.write(b'P %d %d\r' % (angle,nbiter))
        return self.waittofinish()