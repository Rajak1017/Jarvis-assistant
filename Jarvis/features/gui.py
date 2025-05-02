from PyQt5 import QtCore, QtGui, QtWidgets
import sys
import time


class EmittingStream(QtCore.QObject):
    textWritten = QtCore.pyqtSignal(str)

    def write(self, text):
        self.textWritten.emit(str(text))

    def flush(self):
        pass  # This method is intentionally left empty to override sys.stdout behavior


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("Jarvis")
        MainWindow.resize(1440, 900)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        # Background label
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(0, 0, 1440, 900))
        self.label.setText("")
        self.label.setPixmap(QtGui.QPixmap("images\\program_load.gif"))
        self.label.setScaledContents(True)
        self.label.setObjectName("label")

        # Run button
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(1180, 800, 101, 51))
        self.pushButton.setStyleSheet("""
            QPushButton {
                background-color: rgb(0, 170, 255);
                font: 75 18pt "MS Shell Dlg 2";
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: rgb(0, 150, 230);
            }
            QPushButton:pressed {
                background-color: rgb(0, 130, 200);
            }
        """)
        self.pushButton.setObjectName("pushButton")
        self.pushButton.setText("Run")

        # Connect button click directly to zoom animation
        self.pushButton.clicked.connect(lambda: self.animate_button_zoom(self.pushButton))

        # Exit button
        self.pushButton_2 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_2.setGeometry(QtCore.QRect(1310, 800, 101, 51))
        self.pushButton_2.setStyleSheet("""
            QPushButton {
                background-color: rgb(255, 0, 0);
                font: 75 18pt "MS Shell Dlg 2";
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: rgb(200, 0, 0);
            }
            QPushButton:pressed {
                background-color: rgb(150, 0, 0);
            }
        """)
        self.pushButton_2.setObjectName("pushButton_2")
        self.pushButton_2.setText("Exit")

        # Connect button click directly to zoom animation
        self.pushButton_2.clicked.connect(lambda: self.animate_button_zoom(self.pushButton_2))

        # Other widgets
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(10, 10, 401, 91))
        self.label_2.setText("")
        self.label_2.setPixmap(QtGui.QPixmap("images\\initiating.gif"))
        self.label_2.setObjectName("label_2")

        self.textBrowser = QtWidgets.QTextBrowser(self.centralwidget)
        self.textBrowser.setGeometry(QtCore.QRect(640, 30, 291, 61))
        self.textBrowser.setStyleSheet("""
            font: 75 16pt "MS Shell Dlg 2";
            background-color: transparent;
            color: black;
            border-radius: none;
        """)
        self.textBrowser.setObjectName("textBrowser")

        self.textBrowser_2 = QtWidgets.QTextBrowser(self.centralwidget)
        self.textBrowser_2.setGeometry(QtCore.QRect(930, 30, 291, 61))
        self.textBrowser_2.setStyleSheet("""
            font: 75 16pt "MS Shell Dlg 2";
            background-color: transparent;
            color: black;
            border-radius: none;
        """)
        self.textBrowser_2.setObjectName("textBrowser_2")

        self.textBrowser_3 = QtWidgets.QTextBrowser(self.centralwidget)
        self.textBrowser_3.setGeometry(QtCore.QRect(1000, 500, 431, 281))
        self.textBrowser_3.setStyleSheet("""
            font: 11pt "MS Shell Dlg 2";
            background-color: light-gray;
            color: white;
        """)
        self.textBrowser_3.setObjectName("textBrowser_3")

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1440, 26))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        # Redirect stdout to the textBrowser_3
        sys.stdout = EmittingStream(textWritten=self.updateTextBrowser)

    def updateTextBrowser(self, text):
        self.textBrowser_3.append(text)

    def animate_button_zoom(self, button):
        """Creates a zoom effect for the given button."""
        if hasattr(button, '_animating') and button._animating:
            return  # Prevent overlapping animations

        # Set a flag to mark the button as animating
        button._animating = True
        
        # Save the original size and position
        original_geometry = button.geometry()
        zoomed_geometry = original_geometry.adjusted(-10, -10, 10, 10)  # Slightly enlarge the button

        # Step 1: Zoom In
        animation = QtCore.QPropertyAnimation(button, b"geometry")
        animation.setDuration(100)  # Duration of zoom
        animation.setStartValue(original_geometry)
        animation.setEndValue(zoomed_geometry)
        animation.setEasingCurve(QtCore.QEasingCurve.OutQuad)
        animation.start()

        # Step 2: Zoom Out (after a small delay)
        def zoom_out():
            reset_animation = QtCore.QPropertyAnimation(button, b"geometry")
            reset_animation.setDuration(100)  # Duration of reset
            reset_animation.setStartValue(zoomed_geometry)
            reset_animation.setEndValue(original_geometry)
            reset_animation.setEasingCurve(QtCore.QEasingCurve.OutQuad)
            reset_animation.start()

            # Once the zoom-out is finished, reset the animating flag
            reset_animation.finished.connect(lambda: setattr(button, '_animating', False))

        # Delay the zoom-out action
        QtCore.QTimer.singleShot(150, zoom_out)  # Wait 150ms before zooming out

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()

    sys.exit(app.exec_())