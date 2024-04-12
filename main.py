from PyQt6.QtWidgets import QApplication
from src import MainWindow
import sys


def main():
    """
    Main function
    """

    # Create the application
    app = QApplication([])

    # Create the main window
    mainWindow = MainWindow()
    mainWindow.setFocus()
    mainWindow.show()

    # Start the application event loop
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
