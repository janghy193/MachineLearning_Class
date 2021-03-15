from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import sys


class MainWindow(QMainWindow):

    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)

        self.setWindowTitle("My Awesome App")

        # 레이아웃
        layout = QVBoxLayout()
        self.widget = QWidget()
        self.widget.setLayout(layout)

        # 체크박스
        self.chkbox = QCheckBox()
        self.chkbox.setCheckState(Qt.PartiallyChecked)
        self.chkbox.stateChanged.connect(self.show_state)
        #self.setCentralWidget(widget)
        layout.addWidget(self.chkbox)

        # 래디오버튼
        self.rad1 = QRadioButton("1")
        self.rad2 = QRadioButton("2")
        self.rad1.toggled.connect(self.rad_change)
        self.stt_r = 'None'
        layout.addWidget(self.rad1)
        layout.addWidget(self.rad2)

        # 체크박스용 라벨 설정
        self.stt = Qt.Checked
        self.label = QLabel("CheckBox State: " + str(self.stt))
        self.label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.label)

        self.setCentralWidget(self.widget)

        # 라디오버튼용 라벨 설정
        self.label_r = QLabel("RadioButton State:"+str(self.stt_r)+" is Checked")
        layout.addWidget(self.label_r)

        # 툴바
        toolbar = QToolBar("My main toolbar")
        self.addToolBar(toolbar)

        # 버튼1
        button_action = QAction("확인", self)
        button_action.setStatusTip("Check Button")
        button_action.triggered.connect(self.show_state_2)
        toolbar.addAction(button_action)


    def rad_change(self):
        stt = self.rad1.isChecked()
        stt2 = self.rad2.isChecked()
        print(stt, stt2)
        if stt==True:
            self.stt_r = 1
        else:
            self.stt_r = 2
        self.label_r.setText("RadioButton State:"+str(self.stt_r)+" is Checked")
        self.label_r.repaint()
    def show_state_2(self):
        stt = self.chkbox.checkState()
        stt2 = self.chkbox.isChecked()
        self.label.setText("CheckBox State: " + str(stt)+ ','+ str(stt2))
        self.label.repaint()
    def show_state(self, s):
        print(s == Qt.Checked)
        print(s)


app = QApplication(sys.argv)

window = MainWindow()
window.show()

app.exec_()