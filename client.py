"""
Qu'est-ce qu'un service web ? https://fr.wikipedia.org/wiki/Service_web
Une API REST, qu'est-ce que c'est ? https://www.redhat.com/fr/topics/api/what-is-a-rest-api
Qu'est ce qu'une FastAPI? https://en.wikipedia.org/wiki/FastAPI

"""
from PyQt5.QtWidgets import (
    QApplication,
    QWidget,
    QMainWindow,
    QPushButton,
    QLineEdit,
    QLabel,
    QMessageBox,
)
from PyQt5.Qt import QUrl, QDesktopServices
import requests
import sys
import webbrowser  


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Client")
        self.setFixedSize(400, 400)
        self.label1 = QLabel("Enter your IP:", self)
        self.text1 = QLineEdit(self)
        self.text1.move(10, 30)
        self.label1.move(10, 10)
        self.label2 = QLabel("Enter your API key:", self)
        self.text2 = QLineEdit(self)
        self.text2.move(10, 90)
        self.label2.move(10, 70)
        self.label3 = QLabel("Enter the host adress:", self)
        self.text3 = QLineEdit(self)
        self.text3.move(10, 150)
        self.label3.move(10, 130)
        self.label4 = QLabel("Answer:", self)
        self.label4.move(10, 180)
        self.button = QPushButton("Send", self)
        self.button.move(10, 220)

        self.button.clicked.connect(self.on_click)
        self.button.pressed.connect(self.on_click)

        self.show()

    def on_click(self):
        ip = self.text1.text()
        api = self.text2.text()
        hostname = self.text3.text()
        if ip == "":
            QMessageBox.about(self, "Error", "Please fill the ip field")
        if api == "":
            QMessageBox.about(self, "Error", "Please fill the api field")
        if hostname == "":
            QMessageBox.about(self, "Error", "Please fill the hostname field")
        else:
            res = self.__query(hostname,ip,api)
            if res:
                self.label4.setText("Answer: %s, %s, %s " % (res["Country"],res["Region"],res["City"]))
                self.label4.adjustSize()
                url= "https://www.openstreetmap.org/?mlat=%s&mlon=%s#map=12" %(res["Lat"],res["Long"])
                webbrowser.open(url) 
                self.show()

    def __query(self, hostname,ip,api):
        url = "http://%s/ip/%s?key=%s" % (hostname,ip,api) #http://127.0.0.1:8000/ip/<ip>?key=<api key>
        r = requests.get(url)
        if r.status_code == requests.codes.NOT_FOUND:
            QMessageBox.about(self, "Error", "IP not found or API key wrong or somethings else")
        if r.status_code == requests.codes.OK:
            return r.json()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    main = MainWindow()
    app.exec_()