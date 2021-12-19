from winrar import compress, decompress
import sys, os
from PyQt5.Qt import QDir
from PyQt5.QtWidgets import QApplication, QLabel, QWidget, QMainWindow, QPushButton, QInputDialog, QLineEdit, QFileDialog, QTabWidget,QVBoxLayout, QFileSystemModel
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtGui import QIcon
from PyQt5 import QtCore, QtWidgets

path = ""

class App(QMainWindow):

    def __init__(self): # В конструкторе класса описаны свойства окна и элементов UI
        super().__init__()
        self.title = 'Winrar'
        self.left = 10
        self.top = 10
        self.width = 840
        self.height = 680
        self.initUI()

    def initUI(self): # В методе описаны элементы UI
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

        self.setStyleSheet("background-color: pink;")

        self.table_widget = MyTableWidget(self)
        self.setCentralWidget(self.table_widget)
        
        self.show()
    


class MyTableWidget(QWidget):
    
    def __init__(self, parent):
        super(QWidget, self).__init__(parent)        
        self.layout = QVBoxLayout(self)
        
        # Initialize tab screen
        self.tabs = QTabWidget()
        self.tab1 = QWidget()
        self.tab2 = QWidget()
        self.tabs.resize(300,200)

        self.treeView = QtWidgets.QTreeView()
        self.treeView.clicked.connect(self.onClicked)
        self.fileSystemModel = QFileSystemModel(self.treeView)
        self.fileSystemModel.setReadOnly(False)

        self.fileSystemModel.setRootPath("C:")
        self.treeView.setModel(self.fileSystemModel)

        
        
        # Add tabs
        self.tabs.addTab(self.tab1,"Archiver")
        self.tabs.addTab(self.tab2,"Info")

        self.archButton = QPushButton('Архивировать', self) # Кнопка архивациии
        self.archButton.setMinimumWidth(200)
        self.archButton.setMinimumHeight(50)
        self.archButton.move(80,200)
        self.archButton.clicked.connect(self.click_compress)

        self.dearchButton = QPushButton('Деархивировать', self) # Кнопка деархивациии
        self.dearchButton.setMinimumWidth(200)
        self.dearchButton.setMinimumHeight(50)
        self.dearchButton.move(350,200)
        self.dearchButton.clicked.connect(self.click_decompress)
        
        # Create first tab
        self.tab1.layout = QVBoxLayout(self)

        self.tab1.layout.addWidget(self.archButton)
        self.tab1.layout.addWidget(self.dearchButton)
        self.tab1.setLayout(self.tab1.layout)

        self.tab2.layout = QVBoxLayout(self)
        self.label = QLabel("Создатель Даниил Оборин ПОИТ 1. \n\n\n\n\n Архивация крупных обьектов возможно потребует большого количества времени, полностью зависит от вашего железа. \n\n\n Архивация обЪектов вроде *EXE* и прочих не поддерживается сжатию.", self)
        self.tab2.layout.addWidget(self.label)
        self.tab2.setLayout(self.tab2.layout)
        
        # Add tabs to widget
        self.layout.addWidget(self.tabs)
        self.tab1.layout.addWidget(self.treeView)
        self.setLayout(self.layout)

    def onClicked(self, index):
        global path
        self.sender() == self.treeView
        self.sender().model() == self.fileSystemModel
        path = self.sender().model().filePath(index)


    def openFileNameDialog(self): # Описание окошка для выбора файлов
        global path
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog

        '''self.dirModel = QFileSystemModel()
        self.dirModel.setFilter(
            # ... |
            QDir.AllDirs | 
            QDir.Files | 
            QDir.Hidden     # <--- Список скрытых файлов (в Unix файлы начинаются с ".").
        )'''
        
        fileName = path #QFileDialog.getOpenFileName(self,"Выберите файл", "","All Files (*);;Text Files (*.txt)", options=options)
        if fileName:
            return fileName


    @pyqtSlot() # Хендлер события
    def click_compress(self): # Функция сжатия файла
        try:
            compress(self.openFileNameDialog())
        except Exception:
            pass

    @pyqtSlot()
    def click_decompress(self): # Функция деархивации файла
        try:
            decompress(self.openFileNameDialog())
        except Exception:
            pass

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())