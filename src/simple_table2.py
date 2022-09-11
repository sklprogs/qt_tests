#!/usr/bin/python3

import PyQt5
import PyQt5.QtWidgets
import sys

cell = '<b>Общая</b> <i>ле</i>ксик<u>а</u>'


class CustomDelegate(PyQt5.QtWidgets.QStyledItemDelegate):
    # akej74, https://stackoverflow.com/questions/35397943/how-to-make-a-fast-qtableview-with-html-formatted-and-clickable-cells
    def paint(self,painter,option,index):
        options = PyQt5.QtWidgets.QStyleOptionViewItem(option)
        self.initStyleOption(options,index)
    
        if options.widget:
            style = options.widget.style()
        else:
            style = PyQt5.QtWidgets.QApplication.style()
    
        doc = PyQt5.QtGui.QTextDocument()
        doc.setHtml(options.text)
        options.text = ''
    
        style.drawControl(PyQt5.QtWidgets.QStyle.CE_ItemViewItem,options,painter)
        ctx = PyQt5.QtGui.QAbstractTextDocumentLayout.PaintContext()
    
        textRect = style.subElementRect(PyQt5.QtWidgets.QStyle.SE_ItemViewItemText,options)
    
        painter.save()
    
        painter.translate(textRect.topLeft())
        painter.setClipRect(textRect.translated(-textRect.topLeft()))
        painter.translate(0,0.5*(options.rect.height() - doc.size().height()))
        doc.documentLayout().draw(painter,ctx)
    
        painter.restore()



class TableModel(PyQt5.QtCore.QAbstractTableModel):
    def __init__(self, data):
        super(TableModel, self).__init__()
        self._data = data

    def data(self,index,role):
        if role == PyQt5.QtCore.Qt.DisplayRole:
            return self._data[index.row()][index.column()]

    def rowCount(self,index):
        return len(self._data)

    def columnCount(self,index):
        ''' The following takes the first sub-list, and returns the length
            (only works if all rows are an equal length).
        '''
        return len(self._data[0])



class Table(PyQt5.QtWidgets.QWidget):
    
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
    
    def fill(self):
        table_item = PyQt5.QtWidgets.QTableWidgetItem(cell)
        self.table.setItem(0,0,table_item)
    
    def set_gui(self):
        self.table = PyQt5.QtWidgets.QTableWidget()
        self.table.setItemDelegate(CustomDelegate())
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
