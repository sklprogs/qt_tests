#!/usr/bin/python3
# Based on https://gis.stackexchange.com/questions/385616/qtexttable-insert-a-line-in-a-cell

import sys
import PyQt5
import PyQt5.QtWidgets


#PyQt5.QtWidgets.QWidget
class Table(PyQt5.QtWidgets.QTextEdit):

    def __init__(self):
        super().__init__()
        self.set_gui()

    def set_gui(self):
        doc = PyQt5.QtGui.QTextDocument()
        doc.setPlainText('Hello World')
        #doc.setHtml('<b>Hello World</b>')
        #PyQt5.QtGui.QTextTable(doc)
        '''
        edit = PyQt5.QtWidgets.QTextEdit()
        self.addWidget(edit)
        edit.setDocument(doc)
        '''


if __name__ == '__main__':
    app = PyQt5.QtWidgets.QApplication(sys.argv)
    itable = Table()
    itable.show()
    app.exec_()
