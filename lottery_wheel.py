from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *


# overriding the key press and key release events to emit a signal only when "c" is pressed
class KeyboardWidget(QWidget):
    keyPressed = pyqtSignal()
    keyReleased = pyqtSignal()

    def keyPressEvent(self, keyEvent):
        if keyEvent.text() == "c" and not keyEvent.isAutoRepeat():
            self.keyPressed.emit()

    def keyReleaseEvent(self, keyEvent):
        if keyEvent.text() == "c" and not keyEvent.isAutoRepeat():
            self.keyReleased.emit()

class LotteryWheel(QObject):
    lottery_result = pyqtSignal(str)  # will emit the colour of the pane the wheel lands on

    def __init__(self, window):
        super(LotteryWheel, self).__init__()
        self.window = window

        self.rotation_timer = QTimer()
        self.rotation_timer.timeout.connect(self.rotate_image)
        self.rotation_timer.timeout.connect(self.increase_speed)  # increases the speed as the "c" key is held

        self.spin_speed = 200  # initialising speed, this is the timer length
        self.max_spin_speed = 30

        self.rotation_count = 0  # used to determine where the wheel lands
        self.rotation_angle = 90  # the image will be rotated by 90 degrees each time

        self.wheel_result = ""

    # as in the original expt, the wheel spins quicker the longer you hold it down
    # this is to give participants the feeling that the outcome was truly stochastic
    # and that they can somewhat control the outcome
    def increase_speed(self):
        if self.spin_speed <= self.max_spin_speed:
            self.spin_speed = self.max_spin_speed
        else:
            self.spin_speed -= 10  # the quicker the timer times out, the faster it spins
            self.start_timer()

    def rotate_image(self):
        pixmap = self.window.lbl_wheel.pixmap()
        pixmap_rotated = pixmap.transformed(QTransform().rotate(self.rotation_angle))
        self.window.lbl_wheel.setPixmap(pixmap_rotated)
        self.rotation_count += 1

    def start_timer(self):
        self.rotation_timer.start(self.spin_speed)

    def stop_timer(self):
        self.rotation_timer.stop()
        self.reset_wheel()
        self.get_wheel_result()

    def reset_wheel(self):
        self.spin_speed = 200
        self.window.setFocus()  # to stop the user from spinning again I am shifting the focus back to main window

    def get_wheel_result(self):
        # since we are rotation by 90 degrees, based on the image if we rotate by 180 or 360 we will land
        # on colour, otherwise it lands on white
        if self.rotation_count % 4 == 0 or self.rotation_count % 2 == 0:
            lottery_result = "colour"
        else:
            lottery_result = "white"
        self.lottery_result.emit(lottery_result)




