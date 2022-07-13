from PyQt5 import QtGui, QtCore
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QFont
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
import sys
import pyqtgraph as pg
from pyqtgraph import Color

from Visualization import Visualization


class MplCanvas(FigureCanvasQTAgg):

    def __init__(self, parent=None, width=5, height=4, dpi=100):
        self.visualization = Visualization(width=5, height=4, dpi=100)
        super(MplCanvas, self).__init__(self.visualization.fig)


class Window(QMainWindow):
    def __init__(self):
        super().__init__()
        # setting title
        self.setWindowTitle("PyQtGraph")
        # self.app.setStyle('Fusion')
        self.palette = QtGui.QPalette()
        self.palette.setColor(QtGui.QPalette.Window, QtGui.QColor(53, 53, 53))
        self.palette.setColor(QtGui.QPalette.WindowText, QtCore.Qt.white)
        self.palette.setColor(QtGui.QPalette.Base, QtGui.QColor(15, 15, 15))
        self.palette.setColor(QtGui.QPalette.AlternateBase, QtGui.QColor(53, 53, 53))
        self.palette.setColor(QtGui.QPalette.ToolTipBase, QtCore.Qt.white)
        self.palette.setColor(QtGui.QPalette.ToolTipText, QtCore.Qt.white)
        self.palette.setColor(QtGui.QPalette.Text, QtCore.Qt.white)
        self.palette.setColor(QtGui.QPalette.Button, QtGui.QColor(53, 53, 53))
        self.palette.setColor(QtGui.QPalette.ButtonText, QtCore.Qt.white)
        self.palette.setColor(QtGui.QPalette.BrightText, QtCore.Qt.red)
        self.palette.setColor(QtGui.QPalette.Highlight,
                              QtGui.QColor(142, 45, 197).lighter())

        self.setPalette(self.palette)
        # setting geometry
        self.setGeometry(100, 100, 800, 800)

        # calling method
        self.UiComponents()

        # showing all the widgets
        self.show()

    # method for components
    def UiComponents(self):
        # creating a push button object
        btn = QPushButton('Push Button')

        # creating a line edit widget
        text = QLineEdit("Line Edit")

        # creating a check box widget
        check = QCheckBox("Check Box")

        # Add plot
        sc = MplCanvas(self, width=5, height=4, dpi=100)
        layout = QGridLayout()
        layout.addWidget(btn, 0, 0)
        layout.addWidget(sc, 1, 1)
        layout.addWidget(text, 0, 1)
        layout.setColumnStretch(0, 1)
        layout.setColumnStretch(1, 3)
        layout.setRowStretch(0, 3)
        layout.setRowStretch(1, 1)

        # creating a widget object
        widget = QWidget()

        # setting this layout to the widget
        widget.setLayout(layout)

        # setting this widget as central widget of the main window
        self.setCentralWidget(widget)


if __name__ == '__main__':
    # create pyqt5 app
    App = QApplication(sys.argv)
    App.setStyle("Fusion")

    # create the instance of our Window
    window = Window()

    # start the app
    sys.exit(App.exec())

"""

"""
