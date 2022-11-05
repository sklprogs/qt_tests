#!/usr/bin/python3
# -*- coding: UTF-8 -*-

import PyQt5
import PyQt5.QtWidgets

from skl_shared_qt.localize import _
import skl_shared_qt.shared as sh


class TableModel(PyQt5.QtCore.QAbstractTableModel):
    
    def __init__(self,datain,parent=None,*args):
        PyQt5.QtCore.QAbstractTableModel.__init__(self,parent,*args)
        self.arraydata = datain

    def rowCount(self,parent):
        return len(self.arraydata)

    def columnCount(self,parent):
        return len(self.arraydata[0])

    def data(self,index,role):
        if not index.isValid():
            return PyQt5.QtCore.QVariant()
        if role == PyQt5.QtCore.Qt.DisplayRole:
            try:
                return PyQt5.QtCore.QVariant(self.arraydata[index.row()][index.column()])
            except Exception as e:
                mes = 'List out of bounds at row #{}, col #{}'.format(index.row(),index.column())
                print(mes)
                return PyQt5.QtCore.QVariant()
    
    def update(self,rowno,colno):
        index_ = self.index(rowno,colno)
        self.dataChanged.emit(index_,index_)



class App:
    
    def __init__(self):
        self.set_gui()
    
    def bind(self,hotkey,action):
        PyQt5.QtWidgets.QShortcut(PyQt5.QtGui.QKeySequence(hotkey),self.widget).activated.connect(action)
    
    def show(self):
        self.widget.showMaximized()
    
    def close(self):
        self.widget.close()
    
    def set_bindings(self):
        self.bind('Ctrl+Q',self.close)
        self.bind('Esc',self.close)
    
    def set_gui(self):
        self.widget = PyQt5.QtWidgets.QMainWindow()
        self.compound = PyQt5.QtWidgets.QWidget()
        self.layout = PyQt5.QtWidgets.QVBoxLayout()
        self.table = Table()
        self.panel = Panel()
        self.layout.addWidget(self.table.table)
        self.layout.addWidget(self.panel.widget)
        self.compound.setLayout(self.layout)
        self.widget.setCentralWidget(self.compound)
        self.set_bindings()



class Table:
    
    def __init__(self):
        self.set_gui()
        
    def set_gui(self):
        self.widget = PyQt5.QtWidgets.QWidget()
        self.layout = PyQt5.QtWidgets.QVBoxLayout()
        self.table = PyQt5.QtWidgets.QTableView()



class Panel:

    def __init__(self):
        self.set_values()
        self.set_gui()
    
    def set_gui(self):
        self.widget = PyQt5.QtWidgets.QWidget()
        self.layout = PyQt5.QtWidgets.QHBoxLayout()
        self.set_buttons()
        self.layout.addWidget(self.btn_trn.widget)
        self.layout.addWidget(self.btn_clr.widget)
        self.layout.addWidget(self.btn_ins.widget)
        self.layout.addWidget(self.btn_rp1.widget)
        self.layout.addWidget(self.btn_rp2.widget)
        self.layout.setContentsMargins(4,4,4,4)
        self.widget.setLayout(self.layout)
    
    def set_buttons(self):
        self.btn_trn = sh.Button (hint = _('Translate')
                                 ,inactive = self.icn_ret
                                 ,active = self.icn_ret
                                 )
        self.btn_clr = sh.Button (hint = _('Clear search field')
                                 ,inactive = self.icn_clr
                                 ,active = self.icn_clr
                                 )
        self.btn_ins = sh.Button (hint = _('Paste text from clipboard')
                                 ,inactive = self.icn_ins
                                 ,active = self.icn_ins
                                 )
        self.btn_rp1 = sh.Button (hint = _('Paste current request')
                                 ,inactive = self.icn_rp0
                                 ,active = self.icn_rp1
                                 )
        self.btn_rp2 = sh.Button (hint = _('Paste previous request')
                                 ,inactive = self.icn_r20
                                 ,active = self.icn_r21
                                 )
    
    def set_values(self):
        self.icn_ret = sh.objs.get_pdir().add ('..','resources','buttons'
                                              ,'go_search.png'
                                              )
        self.icn_clr = sh.objs.pdir.add ('..','resources','buttons'
                                        ,'clear_search_field.png'
                                        )
        self.icn_ins = sh.objs.pdir.add ('..','resources','buttons'
                                        ,'paste.png'
                                        )
        self.icn_rp0 = sh.objs.pdir.add ('..','resources','buttons'
                                        ,'repeat_sign_off.png'
                                        )
        self.icn_rp1 = sh.objs.pdir.add ('..','resources','buttons'
                                        ,'repeat_sign.png'
                                        )
        self.icn_r20 = sh.objs.pdir.add ('..','resources','buttons'
                                        ,'repeat_sign2_off.png'
                                        )
        self.icn_r21 = sh.objs.pdir.add ('..','resources','buttons'
                                        ,'repeat_sign2.png'
                                        )



if __name__ == '__main__':
    import sys
    exe = PyQt5.QtWidgets.QApplication(sys.argv)
    app = App()
    data = []
    for rowno in range(100):
        row = []
        for colno in range(10):
            mes = _('Row: {}. Column: {}').format(rowno,colno)
            row.append(mes)
        data.append(row)
    model = TableModel(data)
    app.table.table.setModel(model)
    app.show()
    sys.exit(exe.exec_())
