#!/usr/bin/python3
# -*- coding: UTF-8 -*-

import PyQt5
import PyQt5.QtWidgets


class MyTableModel(PyQt5.QtCore.QAbstractTableModel):
    
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
            return PyQt5.QtCore.QVariant(self.arraydata[index.row()][index.column()])
    
    def update(self):
        self.layoutChanged.emit()



class CustomDelegate(PyQt5.QtWidgets.QStyledItemDelegate):
    
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.rowno = 0
        self.colno = 0
        color = PyQt5.QtGui.QColor('red')
        self.pen = PyQt5.QtGui.QPen(color,2)
    
    def paint(self,painter,option,index):
        options = PyQt5.QtWidgets.QStyleOptionViewItem(option)
        self.initStyleOption(options,index)
    
        if options.widget:
            style = options.widget.style()
        else:
            style = PyQt5.QtWidgets.QApplication.style()
    
        style.drawControl(PyQt5.QtWidgets.QStyle.CE_ItemViewItem,options,painter)
    
        if index.row() == self.rowno and index.column() == self.colno:
            painter.setPen(self.pen)
            painter.drawRect(option.rect)



class Table(PyQt5.QtWidgets.QTableView):
    
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.set_gui()
    
    def eventFilter(self,widget,event):
        # Qt accepts boolean at output, but not NoneType
        if event.type() != PyQt5.QtCore.QEvent.MouseMove:
            return False
        pos = event.pos()
        colno = self.columnAt(pos.x())
        rowno = self.rowAt(pos.y())
        if rowno == self.delegate.rowno and colno == self.delegate.colno:
            return False
        self.delegate.rowno = rowno
        self.delegate.colno = colno
        #NOTE: The model should be assigned from the controller
        self.model.update()
        return True
    
    def set_gui(self):
        self.delegate = CustomDelegate()
        self.setItemDelegate(self.delegate)



class App(PyQt5.QtWidgets.QMainWindow):
    
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
    
    def show(self):
        self.showMaximized()
    
    def create_layout(self):
        self.parent = PyQt5.QtWidgets.QWidget()
        self.layout = PyQt5.QtWidgets.QVBoxLayout()
    
    def set_layout(self):
        self.layout.addWidget(self.table)
        self.parent.setLayout(self.layout)
    
    def set_gui(self):
        self.create_layout()
        self.table = Table()
        self.set_layout()
        self.setCentralWidget(self.parent)



if __name__ == '__main__':
    import sys
    exe = PyQt5.QtWidgets.QApplication(sys.argv)
    app = App()
    app.set_gui()
    
    data = []
    for i in range(20):
        row = []
        for j in range(20):
            mes = 'Row: {}. Column: {}'.format(i,j)
            row.append(mes)
        data.append(row)
    
    tablemodel = MyTableModel(data)
    app.table.setModel(tablemodel)
    app.table.model = tablemodel
    exe.installEventFilter(app.table)
    app.show()
    sys.exit(exe.exec_())
