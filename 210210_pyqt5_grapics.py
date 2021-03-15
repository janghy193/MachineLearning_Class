import sys
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *

class Ball():
    def __init__(self,x,y,w,h,c,s):
        super().__init__()

        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.c = c
        self.s = s

    def draw(self,painter):
        rect = QRectF(self.x, self.y, self.w, self.h)
        col = self.c
        painter.setBrush(col)
        painter.drawEllipse(rect)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.x1 = 0
        self.y1 = 0

        self.white_ball = Ball(175,275,50,50,Qt.white,-10)

        self.timer = QTimer()
        self.timer2 = QTimer()

        # 캔버스
        self.label = QLabel()
        canvas = QPixmap(400,300)
        self.label.setPixmap(canvas)
        self.setCentralWidget(self.label)
        self.draw_something()

        # 툴바
        toolbar = QToolBar("My main toolbar")
        self.addToolBar(toolbar)

        # 툴바 버튼 - 1픽셀 이동
        button_action = QAction("1px 이동", self)
        button_action.setStatusTip("Button")
        button_action.triggered.connect(self.move_1)
        toolbar.addAction(button_action)

        # 툴바 버튼 - 5픽셀 이동
        button_action2 = QAction("5px 이동", self)
        button_action2.setStatusTip("Button")
        button_action2.triggered.connect(self.move_5)
        toolbar.addAction(button_action2)

        # 툴바 버튼 - 50픽셀 - 1픽셀씩 이동
        button_action3 = QAction("자동이동", self)
        button_action3.setStatusTip("Button")
        button_action3.triggered.connect(self.move_auto)
        toolbar.addAction(button_action3)

        # 툴바 버튼 - 자동이동 정지
        button_action3 = QAction("정지", self)
        button_action3.setStatusTip("Button")
        button_action3.triggered.connect(self.move_end)
        toolbar.addAction(button_action3)

        # 툴바 버튼 - 초기위치로
        button_action3 = QAction("원위치", self)
        button_action3.setStatusTip("Button")
        button_action3.triggered.connect(self.move_init)
        toolbar.addAction(button_action3)

    # 키 입력으로 함수 실행
    def keyPressEvent(self,evt):
        if evt.key()==Qt.Key_Space:
            print('Fire')
            self.init_white_ball()
            self.timer2.setInterval(15)
            self.timer2.timeout.connect(self.move_fire)
            self.timer2.start()

        if evt.key()==Qt.Key_Right:
            self.move_right()

        if evt.key()==Qt.Key_Left:
            self.move_left()

        if evt.key()==Qt.Key_Down:
            self.move_down()

        if evt.key()==Qt.Key_Up:
            self.move_up()

    def move_fire(self):
        self.white_ball.y += self.white_ball.s
        self.draw_something()
        self.label.repaint()

    def move_right(self):
        self.x1 += 6

        self.draw_something()
        self.label.repaint()

    def move_left(self):
        self.x1 += -6

        self.draw_something()
        self.label.repaint()

    def move_down(self):
        self.y1 += 6

        self.draw_something()
        self.label.repaint()

    def move_up(self):
        self.y1 += -6

        self.draw_something()
        self.label.repaint()

    def init_white_ball(self):
        self.white_ball.x = 175
        self.white_ball.y = 375

    def move_init(self):
        self.x1 = 0
        self.y1 = 0
        self.white_ball.x = 175
        self.white_ball.y = 375

        self.draw_something()
        self.label.repaint()
        self.timer.stop()
        self.timer2.stop()
    def move_end(self):
        self.timer.stop()
        self.timer2.stop()

    def move_auto(self):
        self.timer.setInterval(15)
        self.timer.timeout.connect(self.move_1)
        self.timer.start()

    def move_1(self):
        if not(self.x1+60>=400 or self.y1+120>=300):
            self.x1 += 1
            self.y1 += 1

            self.draw_something()
            self.label.repaint()
        else:
            self.timer.stop()

    def move_5(self):
        if not (self.x1 + 60 >= 400 or self.y1 + 120 >= 300):
            self.x1 += 5
            self.y1 += 5

            self.draw_something()
            self.label.repaint()
        else:
            self.timer.stop()

    def draw_something(self):
        # 캔버스 초기화
        self.label = QLabel()
        canvas = QPixmap(400,300)
        self.label.setPixmap(canvas)
        self.setCentralWidget(self.label)

        painter = QPainter(self.label.pixmap())
        col = QColor(255, 255, 0)
        painter.setBrush(col)
        #col.setNamedColor('#ff0000')
        painter.drawRect(100,10,50,50)

        # 원1
        col = QColor(78,180,255)
        painter.setBrush(col)
        painter.drawRoundedRect(QRectF(208,15,150,150),75,75)

        # 원2
        rect = QRectF(self.x1,self.y1, 120.0, 120.0)
        #stt_angle = 10*16
        #end_angle = 180*16
        col = QColor(0,255,0)
        painter.setBrush(col)
        painter.drawEllipse(rect)

        # 원3 : white_ball
        rect = QRectF(self.white_ball.x, self.white_ball.y, self.white_ball.w, self.white_ball.h)
        col = self.white_ball.c
        painter.setBrush(col)
        painter.drawEllipse(rect)
        painter.end()

app = QApplication(sys.argv)
window = MainWindow()
window.show()
app.exec_()