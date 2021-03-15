import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
import numpy as np
from ball import *
from gym import *
import time

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.label = QLabel()

        canvas = QPixmap(400, 300)
        self.label.setPixmap(canvas)
        self.setCentralWidget(self.label)

        self.redBall = Ball(0, 0, 20, 8.0, Qt.red, 0, 3)
        self.whtBall = Ball(200, 250, 20, 20, Qt.white, 0, 0)
        self.init_ball()
        self.explosion = False

        self.exp_img = QImage('exp.png')
        #self.collide = False
        self.timer = None
        self.exp_pos = QPointF(0.0, 0.0)

        self.firing = False

        self.timer_start()

    def draw(self):
        painter = QPainter(self.label.pixmap())
        painter.fillRect(0, 0, 400, 300, QBrush(Qt.black))

        self.redBall.draw(painter)
        self.whtBall.draw(painter)

        if self.firing:
            painter.setPen(Qt.yellow)   # 빔 발사
            painter.drawLine(self.whtBall.x+10, 380, self.whtBall.x+10, 0)

        if self.redBall.y > 300:
            self.init_ball()

        if self.explosion:
            self.sprite_anim(painter)

        self.label.repaint()

        if self.collide:
            return

        # Collision Detection
        if self.firing:
            if (self.whtBall.x-10 < self.redBall.x) and (self.whtBall.x+10 > self.redBall.x):
                #print('명중')
                self.firing = False
                self.collide = True
                if not self.explosion:
                    self.explosion = True
                    self.exp_pos.x = self.redBall.x - 20  # 폭발 위치
                    self.exp_pos.y = self.redBall.y - 20
                    self.init_ball()
            else:
                self.firing = False

    def init_ball(self):
        self.redBall.x = np.random.uniform(low=0, high=380, size=1)
        self.redBall.y = 0
        self.whtBall.y = 280
        self.whtBall.speedy = 0
        self.collide = False
        print('init_ball()')

    def timer_start(self):
        self.timer = QTimer()
        self.timer.setInterval(30)
        self.timer.timeout.connect(self.draw)
        self.timer.start()

    def timer_stop(self):
        self.timer.stop()

    def keyPressEvent(self, evt):
        if evt.key()==Qt.Key_Space:
            self.fire()
        if evt.key()==Qt.Key_Right:
            self.move_right()
        elif evt.key()==Qt.Key_Left:
            self.move_left()

    def sprite_anim(self, painter):
        s = 62
        target = QRectF(self.exp_pos.x, self.exp_pos.y, s, s)
        source = QRectF(0, 0, s, s)  # 폭발 스프라이트의 1 프레임
        painter.drawImage(target, self.exp_img, source)
        self.explosion = False

    def move_right(self):
        self.whtBall.x += 10

    def move_left(self):
        self.whtBall.x -= 10

    def fire(self):
        self.firing = True


app = QApplication(sys.argv)
window = MainWindow()
window.show()
app.exec_()