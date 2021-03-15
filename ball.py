from PyQt5.QtCore import *

class Ball():
    def __init__(self,x,y,w,h,c,speedx,speedy):
        super().__init__()

        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.c = c
        self.speedx = speedx
        self.speedy = speedy

    def draw(self,painter):
        self.x += self.speedx
        self.y += self.speedy

        painter.setBrush(self.c)
        painter.drawEllipse(QRectF(self.x, self.y, self.w, self.h))