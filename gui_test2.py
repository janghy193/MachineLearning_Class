from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import sys


class MainWindow(QMainWindow):
    i = 0
    def __init__(self, *args, **kwargs):

        super(MainWindow, self).__init__(*args, **kwargs)

        self.setWindowTitle("My Awesome App")

        self.label = QLabel("YOU CLICKED THE BUTTON " + str(self.i)+" TIMES")
        self.label.setAlignment(Qt.AlignCenter)

        self.setCentralWidget(self.label)

        toolbar = QToolBar("My main toolbar")
        self.addToolBar(toolbar)

        def count():
            self.i = self.i + 1
            self.label.setText("YOU CLICKED THE BUTTON " + str(self.i)+" TIMES")
            #self.label.repaint()

        # 버튼1
        button_action = QAction(QIcon("1.gif"),"Your button", self)
        button_action.setStatusTip("Count Button")
        button_action.triggered.connect(self.onMyToolBarButtonClick)
        button_action.triggered.connect(count)
        #button_action.setCheckable(True)

        # 버튼2
        button_action2 = QAction(QIcon("2.bmp"), "Your button", self)
        button_action2.setStatusTip("Count Button")
        button_action2.triggered.connect(self.onMyToolBarButtonClick)
        button_action2.triggered.connect(count)

        # 버튼3
        button_action3 = QAction(QIcon("3.bmp"), "Your button", self)
        button_action3.setStatusTip("Count Button")
        button_action3.triggered.connect(self.onMyToolBarButtonClick)
        button_action3.triggered.connect(count)

        toolbar.addAction(button_action)
        menu = self.menuBar() # 이미 존재함 - 객체화만 수행해서 사용

        file_menu = menu.addMenu("&File")
        file_menu.addAction(button_action)
        file_menu.addSeparator()  # 구분선 추가
        file_menu.addAction(button_action2)

        file_submenu = file_menu.addMenu("서브메뉴")
        file_submenu.addAction(button_action3)

        # button_action1 숏컷 추가
        button_action.setShortcut(QKeySequence("Ctrl+p"))

        # 레이아웃
        layout = QVBoxLayout()

        widgets = [QCheckBox,
                   QComboBox,
                   QDateEdit,
                   QDateTimeEdit,
                   QDial,
                   QDoubleSpinBox,
                   QFontComboBox,
                   QLCDNumber,
                   QLabel,
                   QLineEdit,
                   QProgressBar,
                   QPushButton,
                   QRadioButton,
                   QSlider,
                   QSpinBox,
                   QTimeEdit]

        for w in widgets:
            layout.addWidget(w())
        widget = QWidget()

        widget.setLayout(layout)

        self.setCentralWidget(widget)

        self.setStatusBar(QStatusBar(self))  # 상태바 추가
    def show_state(self, s):
        print(s==Qt.Checked)
        print(s)
    def onMyToolBarButtonClick(self, s):
        print("click", s)


app = QApplication(sys.argv)

window = MainWindow()
window.show()

app.exec_()