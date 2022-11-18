#!/usr/bin/python3
# -*- coding: UTF-8 -*-

import sys
import PyQt5
import PyQt5.QtWidgets
from skl_shared_qt.localize import _
import skl_shared_qt.shared as sh


class Entry(PyQt5.QtWidgets.QLineEdit):
    
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
    
    def keyPressEvent(self,event):
        if event.key() == PyQt5.QtCore.Qt.Key_V and event.modifiers() \
        & PyQt5.QtCore.Qt.ControlModifier:
            print('Catch hotkey')
        super(PyQt5.QtWidgets.QLineEdit,self).keyPressEvent(event)



class Top(PyQt5.QtWidgets.QWidget):

    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.add_entry()
    
    def add_entry(self):
        self.ent = Entry()
        layout = PyQt5.QtWidgets.QVBoxLayout()
        layout.addWidget(self.ent)
        self.setLayout(layout)
        self.ent.setFocus()


if __name__ == '__main__':
    sh.com.start()
    top = Top()
    top.show()
    sh.com.end()
