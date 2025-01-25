import sys
from Interface import Interface
from PyQt5.QtWidgets import QApplication

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = Interface()
    window.show()
    sys.exit(app.exec_())