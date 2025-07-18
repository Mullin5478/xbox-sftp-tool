import sys
from PyQt5.QtWidgets import QApplication
from wizard import SetupWizard
from file_explorer import FileExplorer

if __name__ == "__main__":
    app = QApplication(sys.argv)
    wizard = SetupWizard()
    if wizard.exec_() == 1:
        explorer = FileExplorer()
        explorer.show()
        sys.exit(app.exec_())
