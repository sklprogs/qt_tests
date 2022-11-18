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
        #self.bind()
    
    def bind_rep(self):
        print('BOUND ENTRY!')
    
    def bind(self):
        PyQt5.QtWidgets.QShortcut(PyQt5.QtGui.QKeySequence('Ctrl+J'),self).activated.connect(self.bind_rep)
    
    def keyPressEvent(self,event):
        print('Triggered')
        if event.key() == PyQt5.QtCore.Qt.Key_V and event.modifiers() \
        & PyQt5.QtCore.Qt.ControlModifier:
            print('Catch hotkey')
        super(PyQt5.QtWidgets.QLineEdit,self).keyPressEvent(event)
    
    '''
    def eventFilter(self,widget,event):
        #key_event = PyQt5.QtCore.QEvent(event)
        #key_event.modifiers().testFlag(PyQt5.QtCore.Qt.ControlModifier)
        if event.modifiers() == PyQt5.QtCore.Qt.ControlModifier and \
        event.key() == 'V':
            print('Catch hotkey')
            return True
        #return PyQt5.QtWidgets.QLineEdit().eventFilter(widget,event)
        return super().eventFilter(widget,event)
    '''
            
    
    '''
    def event(self,event):
        if event.type() == PyQt5.QtCore.QEvent.KeyPress:
            key = event.key()
            if key == PyQt5.QtCore.Qt.Key_Left:
                print('Key_Left')
                return True
            
            elif key == PyQt5.QtGui.QKeySequence.MoveToEndOfDocument:
                print('move to end')
                return True
        return False
    '''



class Top(PyQt5.QtWidgets.QWidget):

    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.add_entry()
        self.bind()
    
    def add_entry(self):
        self.ent = Entry()
        layout = PyQt5.QtWidgets.QVBoxLayout()
        layout.addWidget(self.ent)
        self.setLayout(layout)
        self.ent.setFocus()
        #ent.installEventFilter(self)
    
    def bind_rep(self):
        print('BOUND!')
    
    def bind(self):
        PyQt5.QtWidgets.QShortcut(PyQt5.QtGui.QKeySequence('Ctrl+O'),self).activated.connect(self.bind_rep)
    
    



if __name__ == '__main__':
    sh.com.start()
    top = Top()
    #sh.objs.get_root().installEventFilter(top.ent)
    top.show()
    sh.com.end()
