from PyQt6.QtWidgets import QMainWindow, QLineEdit, QFileDialog, QMessageBox
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

        # Check the inputs
        textualInputs = {
            "Video input path": videoInputPath,
            "Subtitles path": subtitlesPath
        }

        invalidInputDescriptions = self.checkInputValues(textualInputs)

        if len(invalidInputDescriptions) > 0:
            self.showInvalidInputsMessage(invalidInputDescriptions)
            return

        # Check the output video path
        defaultOutputVideoPath = self.getDefaultOutputVideoPath(videoInputPath)
        videoOutputPath = QFileDialog.getSaveFileName(directory=defaultOutputVideoPath)[0]

        if videoOutputPath == "":
            return

        if os.path.isfile(videoOutputPath) and os.path.samefile(videoInputPath, videoOutputPath):
            QMessageBox.critical(self, "Error - Output file", "You can't overwrite the input file")
            return

        # Execute the command to add the subtitles
        command = f"ffmpeg -y -i \"{videoInputPath}\" -vf \"subtitles='{subtitlesPath}':si=0\" \"{videoOutputPath}\""
        subprocess.run(command)

    def checkInputValues(self, textualInputs):
        """
        Check inputs to ensure they are valid

        Args:
            textualInputs (dict[str, str]): A dictionary containing textual inputs where keys represent descriptions
                                            of the inputs and values represent the corresponding input values

        Returns:
            list[str]: A list of descriptions indicating why the input is invalid. Each description specifies which
                       input is invalid using the keys from textualInputs
        """

        invalidInputDescriptions = []

        for (description, value) in textualInputs.items():
            if value == "":
                invalidInputDescriptions.append(description + " shouldn't be empty")

        return invalidInputDescriptions

    def showInvalidInputsMessage(self, invalidInputDescriptions):
        """
        Show a message box indicating which inputs are invalid and why

        Args:
            invalidInputDescriptions (list[str]): A list of descriptions indicating why the specified input is invalid
        """

        messageText = "Following inputs are invalid:\n"

        for desc in invalidInputDescriptions:
            messageText += f"    - {desc}\n"

        QMessageBox.critical(self, "Error - Invalid inputs", messageText)

    def getDefaultOutputVideoPath(self, videoInputPath):
        """
        Construct the default path for when the user selects the output video path

        Args:
            videoInputPath (str): Path of the input video

        Returns:
            str: Default path that will be given to the user for the output video
        """

        splittedPath = os.path.split(videoInputPath)

        videoName = splittedPath[1].split(".")
        videoName[0] += "_subbed"
        videoName = ".".join(videoName)

        return os.path.join(splittedPath[0], videoName)
