from PyQt6.QtWidgets import QMainWindow
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
