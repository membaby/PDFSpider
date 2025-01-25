from PyQt5.QtWidgets import QWidget, QGridLayout, QLabel, QLineEdit, QPushButton, QCheckBox, QFileDialog
from PyQt5.QtGui import QIntValidator
import threading

from PDFSpider import PDFSpider


class Interface(QWidget):

    def __init__(self, parent=None):
        self.info = 'Idle'
        self.running = False
        self.version = 'v4'
        super(Interface, self).__init__(parent)
        self.setWindowTitle(f"PDF Spider {self.version}")
        self.layout = QGridLayout()
        self.setLayout(self.layout)

        self.lbl_status = QLabel("Status: Idle")
        self.lbl_link = QLabel("Link:")
        self.lbl_directory = QLabel("Directory:")
        self.lbl_threads = QLabel("Threads:")
        self.lbl_depth = QLabel("Depth:")
        self.txt_link = QLineEdit('')
        self.txt_directory = QLineEdit('')
        self.txt_threads = QLineEdit('1')
        self.txt_depth = QLineEdit('1')
        self.txt_threads.setValidator(QIntValidator())
        self.txt_depth.setValidator(QIntValidator())
        self.cbx_domainOnly = QCheckBox("Traverse only within domain")
        self.btn_start = QPushButton("Start")
        self.btn_browse = QPushButton("Browse")
        self.btn_browse.clicked.connect(self.browse)
        self.btn_start.clicked.connect(self.start)

        self.layout.addWidget(self.lbl_status, 0, 0, 1, 3)
        self.layout.addWidget(self.lbl_link, 1, 0)
        self.layout.addWidget(self.txt_link, 1, 1, 1, 2)
        self.layout.addWidget(self.lbl_directory, 2, 0)
        self.layout.addWidget(self.txt_directory, 2, 1)
        self.layout.addWidget(self.btn_browse, 2, 2)
        self.layout.addWidget(self.lbl_threads, 3, 0)
        self.layout.addWidget(self.txt_threads, 3, 1, 1, 2)
        self.layout.addWidget(self.lbl_depth, 4, 0)
        self.layout.addWidget(self.txt_depth, 4, 1, 1, 2)
        self.layout.addWidget(self.cbx_domainOnly, 5, 0, 1, 3)
        self.layout.addWidget(self.btn_start, 6, 0, 1, 3)

    def start(self):
        self.running = True
        link = self.txt_link.text()
        directory = self.txt_directory.text()
        threads = int(self.txt_threads.text())
        depth = int(self.txt_depth.text())
        domainOnly = self.cbx_domainOnly.isChecked()
        spider = PDFSpider(link, directory, threads, depth, domainOnly, self)
        threading.Thread(target=spider.start_process).start()
        self.btn_start.setText("Stop")
        self.btn_start.clicked.connect(self.stop)
        self.lbl_status.setText("Status: Running")
    
    def stop(self):
        self.running = False
        self.btn_start.setText("Start")
        self.btn_start.clicked.connect(self.start)
        self.lbl_status.setText("Status: Stopped")

    def browse(self):
        directory = QFileDialog.getExistingDirectory(self, "Select Directory")
        self.txt_directory.setText(directory)