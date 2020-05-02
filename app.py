from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt, QPoint, QObject
from PyQt5 import QtCore

import sys

from ctypes import CDLL, c_int, c_double, POINTER, c_uint32, Structure

CoreDisplay = CDLL("/System/Library/Frameworks/CoreDisplay.framework/CoreDisplay")
CoreDisplay.CoreDisplay_Display_SetUserBrightness.argtypes = [c_int, c_double]
CoreDisplay.CoreDisplay_Display_GetUserBrightness.argtypes = [c_int]
CoreDisplay.CoreDisplay_Display_GetUserBrightness.restype = c_double

class ProcessSerialNumber(Structure):
    _fields_ = [
        ('highLongOfPSN', c_uint32),
        ('lowLongOfPSN', c_uint32),
        ]


kNoProcess = 0
kSystemProcess = 1
kCurrentProcess = 2

kProcessTransformToForegroundApplication = 1
kProcessTransformToBackgroundApplication = 2
kProcessTransformToUIElementAppication = 4

ApplicationServices = CDLL('/System/Library/Frameworks/ApplicationServices.framework/ApplicationServices')
ApplicationServices.TransformProcessType.argtypes = [POINTER(ProcessSerialNumber), c_uint32]
ApplicationServices.SetFrontProcess.argtypes = [POINTER(ProcessSerialNumber)]

def become_foreground():
    psn = ProcessSerialNumber(0, kCurrentProcess)
    ApplicationServices.TransformProcessType(psn, kProcessTransformToForegroundApplication)
    ApplicationServices.SetFrontProcess(psn)

def become_background():
    psn = ProcessSerialNumber(0, kCurrentProcess)
    ApplicationServices.TransformProcessType(psn, kProcessTransformToUIElementAppication)

# this is based on undocumented MacOS APIs, unfortunately
# https://alexdelorenzo.dev/programming/2018/08/16/reverse_engineering_private_apple_apis.html
def set_brightness_coredisplay(display: int, brightness: int) -> int:
    brightness /= 100
    return CoreDisplay.CoreDisplay_Display_SetUserBrightness(display, brightness)

def get_brightness_coredisplay(display: int) -> int:
    return int(CoreDisplay.CoreDisplay_Display_GetUserBrightness(display) * 100)


def icon_from_base64(base64):
    pixmap = QPixmap()
    pixmap.loadFromData(QtCore.QByteArray.fromBase64(base64))
    icon = QIcon(pixmap)
    return icon

def quit():
    sys.exit(0)
        
def tray_click():
    # get the current brightness value
    brightness = get_brightness_coredisplay(0)

    # set the slider value
    slider.setValue(brightness)

    # move the dialog right next to the tray icon and show it
    become_foreground()
    rect = tray.geometry()
    dialog.move(rect.x(), rect.y())
    dialog.show()
    dialog.raise_()
   

def close_dialog(x):
    become_background()

def value_changed():
    set_brightness_coredisplay(0, slider.value())

icon_data = b"iVBORw0KGgoAAAANSUhEUgAAAEAAAABACAMAAACdt4HsAAAABGdBTUEAALGPC/xhBQAAAAFzUkdCAK7OHOkAAAKdUExURQAAAP///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////9LcIxoAAADedFJOUwD3/P3z8vHw7+71+/74BPYMT+30CCUvChIRaAb6lgfQHhVVC2Aa5uvKPig6fgNZsej5ObwqJD1QONjTXmbPBXK+XESwdxtM2mNU6tUBTm+qCVYxgt4WQrkOV+x1IJWbJhfZxOPnHdfbGBwNj7apAhkyNCzWSYFKK6hNgzDhDxNanI7CisiQwzeElI08kYUuk9+MM3xhwa+GkkDSQeLpnT9IpcB2l7JGX6G3p5jRJ4nlR5pb3FEUZKTkH8l7O0ViS8YQq8eua2lqbrWZgL0iWIfMZcWmbDWeUilDc2fNoB7zWrsAAAUZSURBVFjDpVf3XxNJFM8m2d3ZJBiUEIogRQEp0pSigIqigF0pVkDBdt7Zz94929l7P6/33nvvvfe7799yb3Y3YRM2u+cn74dk3sx737yZee/NNw6HtYzZ5IhPRvfG558CLIgLIB2YdXseqUGjNqrd5+sbapw5nWMDkPjGSYM2AqKIvw0T58ptdzQa3xSFlXFgDGPDavJ8HLHdwxnAlauPq+GRZQ/+1NWaDOArW4CvMQT4XhvPhuB0JqBM09pAS1f+x7lLSgZ+OE/Da4BPEFzAu6QED8GrSPjCFmAw3DJtHF0pjvebbgR7eoLXFs90BE4CMpPdaLUFqISficC07sSIhMq8DxCZB4W2AMkJFPPH+2YMWFjYC3i9Y2wB1jwP8TPzpXoZBan2uYhD2eHxil2FhfNWhNUpBzHK1Ge4cbfh3O9sm+gGifvSzkmhuVlrTN06s14sSa+pTP6Qxuu0qUETNpOvL8Hj4WeClYv1ilhHh7OnqnZwesnTWY+FAYaO5L8EIX/csrnaTOMqwMNkXVgS0D5CW3ll7Lh8v2r+TKA/mBnLwdx+J7B5qao/qN66QZgMrFWXXs0CnIKboWCQ8RRuoEKRFbi1yy+DX5GjRPHgLnUxwECmCXgh8hxL4KZAtSp6lFJGHiBMwpPq8kzanBunom+iDDIO6iVk5q8iTNYrnunRGCWQ5EM1H5QaTi8KIQmPc4ujcAmJZlV0Vr2RaVDkGKJAmcNtxiLXLJ3mH+OfTZDk2IISbnNhtHkS83sZXw4W259hUUA3jCUPIMkiAGoIg2O67irmn3daBcBDeIRb1c4b4H7/LfzCd9AM2VJwkx9jPf7tjHCvu0S5/QcNNsFrDZCBDWRWRea9F0Pec+qplvw+lkfjSdZHwA9hK5nlFMAD/JPOC/qdn6nbSVQsy9NIa6WWaiki9vFO0AeemCjYfsKx4yxVF6UO8jnAQnuARt51btJRKV5g90zSfu2mlkE3zCv5bjsA7R5TKVvoGH6rDdGQq/Qa+ZJptBEV1gAC+G0voR9nXacN19DxVwN4y0kst7tGlqYW3PXFS6MzoUXNsSfsEmk7t5r6Y8x8bIRoBSDhos2rkCa4rEJwZVgwlHvq+WemdTXuV4nLcVNGiOv8a7XTGROBeXEHt3kLQROA6fBV8e8tFh0Fz3GLbBeaB/qfgojXdSQWq6M1q0/jLTI9F+1fgwRFgFrmOe3mXVFB33q+vk01nRvpn038hyw0Qtaxm8jZgP0z5Ofp1I2/Qfg2AuAnmpREAZmqtnolXFFBKE6sUg+QepYgSoQw0uh/HJr49MhGXaUSNQTB6NnMHKrv1acb32voZ/6sy/uPfZpbnbx+ij4VfIpK1OuWZElyEz3E7A0hkpFXVd36+c7uyw1CmDU43txr4LrF+qDo4YlO7aecDzVt0yeL9xho9RLzx2FIf2jPTm2ZMKFlRz/1PSANs6VIwxZh5FHzpfMfQBxuC7CE86KuIhP+d4aTmB5bgI0QqNl5J78UiIir9JMKap1+VNoC8K7IqMOVJTpqC1PpFRyUeqLSkfIRZRqzfNlC8h7RCxH+12j4O6RlDQ3LZHzHS1ikBQnptgBvg/jPfI1rauQNWaqS9yXxKGyxBThMHodD9Jg3eRF1oY5DS5m2AGsxrTScE8T+mK8gfPe5+TpLspDx8pG0fu0CNXm09esLJnrsMmlvXUSLFZ1eIaKN1nXc3t/IK8CBuP655gHZ8f15nv5ynP/et061MfgPZaTJjdBA/OsAAAAASUVORK5CYII="

# create an application that does not shut down if there are no windows
app = QApplication([])
app.setQuitOnLastWindowClosed(False)

# create a small frameless popup dialog to contain the slider
dialog = QDialog()
dialog.setWindowFlags(Qt.WindowStaysOnTopHint | Qt.FramelessWindowHint | Qt.Popup)
dialog.resize(250, 0)
dialog.closeEvent = close_dialog

# create the brightness slider
slider = QSlider(Qt.Horizontal)
slider.valueChanged.connect(value_changed)


# Create the icon
#icon = QIcon("color.png")
icon = icon_from_base64(icon_data)

# create a simple layout with the slider, and add it to the dialog
layout = QVBoxLayout()
layout.addWidget(QLabel("Brightness:"))
layout.addWidget(slider)
dialog.setLayout(layout)

# Create the tray
tray = QSystemTrayIcon()
tray.setIcon(icon)
tray.setVisible(True)
tray.activated.connect(tray_click)

bottom_layout = QHBoxLayout()

quit_action = QPushButton("Quit")
quit_action.clicked.connect(quit)
bottom_layout.addWidget(QLabel("MacBright Brightness Widget\nCreated by Ron Reiter"))
bottom_layout.addWidget(quit_action)
layout.addLayout(bottom_layout)

tray_click()
become_background()
app.exec_()