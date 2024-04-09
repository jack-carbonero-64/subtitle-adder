from PyQt6.QtWidgets import QMainWindow, QLineEdit, QFileDialog
from PyQt6.uic import loadUi
from config import config
import os
import subprocess


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

    def onApplyPushButtonClicked(self):
        """
        Add the subtitles to the video
        """

        # Retrieve input values
        videoInputPath = self.videoLineEdit.text().strip()
        subtitlesPath = self.subtitlesLineEdit.text().strip()

        subtitlesPath = "\\:".join(subtitlesPath.split(":"))

        # Ask user the video output path
        videoOutputPath = QFileDialog.getSaveFileName()[0]

        # Execute the command to add the subtitles
        if videoOutputPath != "":
            command = f"ffmpeg -y -i \"{videoInputPath}\" -vf \"subtitles='{subtitlesPath}':si=0\" \"{videoOutputPath}\""
            subprocess.run(command)
