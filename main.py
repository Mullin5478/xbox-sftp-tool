import sys
from PyQt5.QtWidgets import QApplication
from file_explorer import FileExplorer

if __name__ == "__main__":
    app = QApplication(sys.argv)
    explorer = FileExplorer()
    explorer.show()
    sys.exit(app.exec_())
