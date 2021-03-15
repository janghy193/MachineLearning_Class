import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
import numpy as np
from ball import *

# Ball 클래스
class Ball():
    def __init__(self, x, y, w, h, c, speedx, speedy):
        super().__init__()

        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.c = c
        self.speedx = speedx
        self.speedy = speedy

    def draw(self, painter):
        self.x += self.speedx
        self.y += self.speedy

        painter.setBrush(self.c)
        painter.setPen(self.c)
        painter.drawEllipse(QRectF(self.x, self.y, self.w, self.h))

# Line 클래스
class Line():
    def __init__(self, ix, iy, c, angle):
        # 선의 시작점(흰 공의 중심)
        self.sx = ix + 10
        self.sy = iy + 10
        self.c = c
        self.angle = angle

    def draw(self, painter):
        # 선 방정식 구하기
        if self.angle == 0:
            self.tx = 0
            self.ty = 290
        elif self.angle != 90:
            self.a = np.tan(self.angle / 180 * np.pi)  # 기울기
            self.b = self.sy - self.a * self.sx  # 절편

            if self.a > 0:  # 기울기가 양수일 때
                # 선이 벽과 만나는 점의 좌표값
                self.tx = max(-1 * self.b / self.a, 0)
                self.ty = max(self.b, 0)

            elif self.a < 0:  # 기울기가 음수일 때
                # 선과 벽이 만나는 점의 좌표값
                self.tx = min(-1 * self.b / self.a, 400)
                self.ty = max(0, 400 * self.a + self.b)

        else:  # 각이 90도 -> 기울기 무한대
            self.tx = 210
            self.ty = 0
            self.a = 9999
            self.b = 0

        painter.setPen(self.c)
        painter.drawLine(self.sx, self.sy, self.tx, self.ty)

# Game Class
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.label = QLabel()

        canvas = QPixmap(400, 300)
        self.label.setPixmap(canvas)
        self.setCentralWidget(self.label)

        self.redBall = Ball(0, 0, 10, 10, Qt.red, 0, 0)
        self.whtBall = Ball(200, 250, 20, 20, Qt.white, 0, 0)
        self.shtLine = Line(200, 280, Qt.cyan, 90)

        self.timecounter = 0
        self.init_ball()
        self.explosion = False

        self.exp_img = QImage('exp.png')
        # self.collide = False
        self.timer = None
        self.exp_pos = QPointF(0.0, 0.0)

        self.firing = False

        self.timer_start()

    def draw(self):
        self.timecounter += 1
        painter = QPainter(self.label.pixmap())
        painter.fillRect(0, 0, 400, 300, QBrush(Qt.black))

        self.shtLine.draw(painter)
        self.redBall.draw(painter)
        self.whtBall.draw(painter)

        if self.firing:
            painter.setPen(Qt.red)  # 빔 발사
            painter.drawLine(self.shtLine.sx, self.shtLine.sy, self.shtLine.tx, self.shtLine.ty)

        if self.timecounter % 90 == 0:
            self.init_ball()

        if self.explosion:
            self.sprite_anim(painter)

        self.label.repaint()

        if self.collide:
            return

        # Collision Detection
        if self.firing:
            # 명중 조건 - 조준선과 빨간볼 중심 사이의 거리가 빨간공 반지름보다 작거나 같을 때
            if np.abs(self.shtLine.a * (self.redBall.x+self.redBall.w/2) -\
                    self.redBall.y+self.redBall.h/2+ self.shtLine.b)/np.sqrt(
                self.shtLine.a**2 + 1) <= self.redBall.w/2:
                #print('명중')
                #print('빨간공 위치(%d, %d), 선 각도 %d, 기울기 %f, 절편 %f' % (self.redBall.x, self.redBall.y,
                #                                                  self.shtLine.angle, self.shtLine.a, self.shtLine.b))
                self.timecounter = 0
                self.firing = False
                self.collide = True
                if not self.explosion:
                    self.explosion = True
                    self.exp_pos.x = self.redBall.x - 20  # 폭발 위치
                    self.exp_pos.y = self.redBall.y - 20
                    self.init_ball()
            else:
                # print('불발')
                # print('빨간공 위치(%d, %d), 선 각도 %d, 기울기 %f, 절편 %f' % (self.redBall.x, self.redBall.y,
                #                                                  self.shtLine.angle, self.shtLine.a, self.shtLine.b))
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

    def timer_anim_start(self):
        self.timer2 = QTimer()
        self.timer2.setInterval(30)
        self.timer2.timeout.connect(self.draw)
        self.timer2.start()

    def timer_stop(self):
        self.timer.stop()

    def keyPressEvent(self, evt):
        if evt.key() == Qt.Key_Space:
            self.fire()
        if evt.key() == Qt.Key_Right:
            self.move_right()
        elif evt.key() == Qt.Key_Left:
            self.move_left()

    def sprite_anim(self, painter):
        s = 62
        target = QRectF(self.exp_pos.x, self.exp_pos.y, 62.0, 62.0)
        source = QRectF(0, 0, 62.0, 62.0)  # 폭발 스프라이트의 첫 프레임만 표시한다
        painter.drawImage(target, self.exp_img, source)

        self.explosion = False

    def move_right(self):
        self.shtLine.angle += 1
        # print(self.shtLine.angle)

    def move_left(self):
        self.shtLine.angle -= 1
        # print(self.shtLine.angle)

    def fire(self):
        self.firing = True


app = QApplication(sys.argv)
window = MainWindow()
window.show()
app.exec_()