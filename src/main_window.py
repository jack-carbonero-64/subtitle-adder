from PyQt6.QtWidgets import QMainWindow, QLineEdit, QFileDialog
from PyQt6.uic import loadUi
from config import config
import os


class MainWindow(QMainWindow):
    """
    Represent the main window of the application
    """

    def __init__(self):
        """
        Initialize the instance of MainWindow
        """

        super().__init__()

        # Load the main window UI
        loadUi(os.path.join(config.UI_DIR, "main_window.ui"), self)

        # Retrieve the useful UI objects
        self.videoLineEdit = self.findChild(QLineEdit, "videoLineEdit")
        self.subtitlesLineEdit = self.findChild(QLineEdit, "subtitlesLineEdit")

    def onBrowsePushButtonClicked(self):
        """
        Display a file dialog to select a video or a subtitles file depending on the clicked button
        """

        senderName = self.sender().objectName()
        filePath = QFileDialog.getOpenFileName(self)[0]

        if "videoBrowse" in senderName:
            self.videoLineEdit.setText(filePath)

        elif "subtitlesBrowse" in senderName:
            self.subtitlesLineEdit.setText(filePath)
