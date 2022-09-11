import sys
import PyQt5
import PyQt5.QtWidgets


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



class Table(PyQt5.QtWidgets.QTableView):
    
    def __init__(self):
        super().__init__()
        # mouseMoveEvent is not activated without this
        self.setMouseTracking(True)
    
    def mouseMoveEvent(self,event):
        print('CustomTableView.mouseMoveEvent')
        colno = self.columnAt(event.pos().x())
        rowno = self.rowAt(event.pos().y())
        mes = 'Row: {}, column: {}'.format(rowno,colno)
        print(mes)



class MainWindow(PyQt5.QtWidgets.QMainWindow):
    
    def __init__(self):
        super().__init__()

        self.table = Table()

        lst = [['<b>4</b>', '<b>9</b> <i>no</i> <u>excuses</u>, fairy tale creatures<b>!</b>', '2']
               ,['1', '0', '0']
               ,['3', '5', '0']
               ,['3', '3', '2']
               ,['7', '8', '9']
               ,
               ]
        
        model = TableModel(lst)
        self.table.setModel(model)
        self.table.setItemDelegate(CustomDelegate())
        self.setCentralWidget(self.table)


if __name__ == '__main__':
    app = PyQt5.QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    app.exec_()
