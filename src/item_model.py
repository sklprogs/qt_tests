#!/usr/bin/python3

import PyQt5
import PyQt5.QtWidgets
import sys

cell = 'Общая лексика'


class Table(PyQt5.QtWidgets.QWidget):
    
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
    
    def fill(self):
        table_item = PyQt5.QtWidgets.QTableWidgetItem(cell)
        self.table.setItem(0,0,table_item)
        self.table.setSelectionBehavior(PyQt5.QtWidgets.QAbstractItemView.SelectRows)
    
    def set_gui(self):
        self.table = PyQt5.QtWidgets.QTableWidget()
        self.table.setRowCount(4)
        self.table.setColumnCount(4)
        self.layout = PyQt5.QtWidgets.QVBoxLayout()
        self.layout.addWidget(self.table) 
        self.setLayout(self.layout)
        self.set_bindings()
        self.hheader = self.table.horizontalHeader()
        self.hheader.setSectionResizeMode(PyQt5.QtWidgets.QHeaderView.ResizeToContents)
    
    def set_bindings(self):
        PyQt5.QtWidgets.QShortcut(PyQt5.QtGui.QKeySequence('Ctrl+Q'),self).activated.connect(self.close)
        PyQt5.QtWidgets.QShortcut(PyQt5.QtGui.QKeySequence('Esc'),self).activated.connect(self.close)


if __name__ == '__main__':
    f = 'controller.__main__'
    app = PyQt5.QtWidgets.QApplication(sys.argv)
    itable = Table()
    itable.set_gui()
    itable.fill()
    itable.showMaximized()
    sys.exit(app.exec())
