import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel
from PyQt5.QtCore import Qt, QTimer, QThread, pyqtSignal
from PyQt5.QtGui import QFont, QPixmap, QImage
import cv2
import RPi.GPIO as GPIO
import time



camera_name_dict = {0: 'Front',
               1: 'Back',
               2: 'Left',
               3: 'Right'}

camera_ip_dict = {0: 'rtsp://admin:admin@192.168.1.188:554/live/main',
               1: 'rtsp://admin:admin@192.168.1.189:554/live/main',
               2: 'rtsp://admin:admin@192.168.1.190:554/live/main',
               3: 'rtsp://admin:admin@192.168.1.191:554/live/main'}


class worker0(QThread):
    imageUpdate = pyqtSignal(QImage)

    def run(self):
        global current_camera_id
        self.ThreadActive = True
        Capture = cv2.VideoCapture(camera_ip_dict[0])
        while self.ThreadActive:
            ret, frame = Capture.read()
            if ret:
                pic = QImage(frame.data, frame.shape[1], frame.shape[0], QImage.Format.Format_RGB888).scaled(640, 480, Qt.KeepAspectRatio)
                self.imageUpdate.emit(pic)

    def stop(self):
        self.ThreadActive = False
        self.quit()
        
class worker1(QThread):
    imageUpdate = pyqtSignal(QImage)

    def run(self):
        global current_camera_id
        self.ThreadActive = True
        Capture = cv2.VideoCapture(camera_ip_dict[1])
        while self.ThreadActive:
            ret, frame = Capture.read()
            if ret:
                pic = QImage(frame.data, frame.shape[1], frame.shape[0], QImage.Format.Format_RGB888).scaled(640, 480, Qt.KeepAspectRatio)
                self.imageUpdate.emit(pic)

    def stop(self):
        self.ThreadActive = False
        self.quit()
        
class worker2(QThread):
    imageUpdate = pyqtSignal(QImage)

    def run(self):
        global current_camera_id
        self.ThreadActive = True
        Capture = cv2.VideoCapture(camera_ip_dict[2])
        while self.ThreadActive:
            ret, frame = Capture.read()
            if ret:
                pic = QImage(frame.data, frame.shape[1], frame.shape[0], QImage.Format.Format_RGB888).scaled(640, 480, Qt.KeepAspectRatio)
                self.imageUpdate.emit(pic)

    def stop(self):
        self.ThreadActive = False
        self.quit()
        
class worker3(QThread):
    imageUpdate = pyqtSignal(QImage)

    def run(self):
        global current_camera_id
        self.ThreadActive = True
        Capture = cv2.VideoCapture(camera_ip_dict[3])
        while self.ThreadActive:
            ret, frame = Capture.read()
            if ret:
                pic = QImage(frame.data, frame.shape[1], frame.shape[0], QImage.Format.Format_RGB888).scaled(640, 480, Qt.KeepAspectRatio)
                self.imageUpdate.emit(pic)

    def stop(self):
        self.ThreadActive = False
        self.quit()

class app_window(QMainWindow):
    def __init__(self, *args, **kwargs):
        QMainWindow.__init__(self, *args, **kwargs)

        global current_camera_id
        current_camera_id = 0

        self.initUI()

        self.worker0 = worker0()       
        self.worker0.imageUpdate.connect(self.imageUpdateSlot0)
        self.worker0.start()
        
        self.worker1 = worker1()       
        self.worker1.imageUpdate.connect(self.imageUpdateSlot1)
        self.worker1.start()
        
        self.worker2 = worker2()       
        self.worker2.imageUpdate.connect(self.imageUpdateSlot2)
        self.worker2.start()
        
        self.worker3 = worker3()       
        self.worker3.imageUpdate.connect(self.imageUpdateSlot3)
        self.worker3.start()
        
        self.initGPIO()
        self.initTimer()

    def imageUpdateSlot0(self, image):
        if current_camera_id == 0:
            image = image.scaled(self.width, self.height-80)
            self.pic.setPixmap(QPixmap.fromImage(image))
        
    def imageUpdateSlot1(self, image):
        if current_camera_id == 1:
            image = image.scaled(self.width, self.height-80)
            self.pic.setPixmap(QPixmap.fromImage(image))
            
    def imageUpdateSlot2(self, image):
        if current_camera_id == 2:
            image = image.scaled(self.width, self.height-80)
            self.pic.setPixmap(QPixmap.fromImage(image))
            
    def imageUpdateSlot3(self, image):
        if current_camera_id == 3:
            image = image.scaled(self.width, self.height-80)
            self.pic.setPixmap(QPixmap.fromImage(image))
        

    def initTimer(self):
        self.timer = QTimer()
        self.timer.timeout.connect(self.timer_interrupt)
        self.timer.start(30)
        
    def initGPIO(self):
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(26, GPIO.IN)
        self.button_previous_state = 0

    def initUI(self):
        self.setWindowTitle('Cameras stream')
        self.camera_lbl = QLabel('Camera: ' + str(current_camera_id+1), self)
        self.camera_lbl.setFont(QFont('Arial', 18, QFont.Bold))
        self.camera_lbl.resize(self.camera_lbl.sizeHint())

        self.desktop = QApplication.desktop()
        self.screenRect = self.desktop.screenGeometry()
        self.height = self.screenRect.height()
        self.width = self.screenRect.width()

        self.camera_lbl.move(int(self.width/2)-80, 10)

        self.pic = QLabel(self)
        #self.pic.setPixmap(QPixmap('temp_pic.jpg').scaled(self.width, self.height-80))
        self.pic.resize(self.width, self.height-80)
        self.pic.move(0, 80)
        
        self.showMaximized()

    def timer_interrupt(self):
        global current_camera_id
        current_state = GPIO.input(26)
        if self.button_previous_state == 0 and current_state == 1:
            current_camera_id += 1
            if current_camera_id > 3:
                current_camera_id = 0
            self.camera_lbl.setText('Camera: ' + str(current_camera_id+1))
        self.button_previous_state = current_state

    
if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = app_window()
    sys.exit(app.exec_())