import sys
import PyQt5
import PyQt5.QtWidgets


class CustomDelegate(PyQt5.QtWidgets.QStyledItemDelegate):
    
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.index = None
    
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
    
        if self.index and index == self.index:
            color = PyQt5.QtGui.QColor('red')
            pen = PyQt5.QtGui.QPen(color,2)
            painter.setPen(pen)
            # Avoid intersecting cell borders and artifacts as the result
            x1, y1, x2, y2 = option.rect.getCoords()
            option.rect.setCoords(x1+1,y1+1,x2-1,y2-1)
            painter.drawRect(option.rect)
        
        painter.translate(textRect.topLeft())
        painter.setClipRect(textRect.translated(-textRect.topLeft()))
        painter.translate(0,0.5*(options.rect.height() - doc.size().height()))
        doc.documentLayout().draw(painter,ctx)
    
        painter.restore()



class TableModel(PyQt5.QtCore.QAbstractTableModel):
    def __init__(self, data):
        super(TableModel, self).__init__()
        self._data = data

    def update(self,index_):
        self.dataChanged.emit(index_,index_)
    
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
        self.delegate = CustomDelegate()
        self.setItemDelegate(self.delegate)
    
    def _use_mouse(self,event):
        if self.delegate.index:
            self.mymodel.update(self.delegate.index)
        pos = event.pos()
        rowno = self.rowAt(pos.y())
        colno = self.columnAt(pos.x())
        index_ = self.mymodel.index(rowno,colno)
        mes = 'Row #{}. Column #{}. Index: {}'.format(rowno,colno,index_)
        print(mes)
        #self.setCurrentIndex(index_)
        self.delegate.index = index_
        self.mymodel.update(self.delegate.index)
    
    """
    def mouseMoveEvent(self,event):
        '''
        print('CustomTableView.mouseMoveEvent')
        colno = self.columnAt(event.pos().x())
        rowno = self.rowAt(event.pos().y())
        mes = 'Row: {}, column: {}'.format(rowno,colno)
        print(mes)
        '''
        self._use_mouse(event)
    """
    
    def eventFilter(self,widget,event):
        ''' #NOTE: Return True for matches only, otherwise the app will freeze!
            Qt accepts boolean at output, but not NoneType.
        '''
        if event.type() == PyQt5.QtCore.QEvent.MouseMove:
            self._use_mouse(event)
            return True
        return False



class MainWindow(PyQt5.QtWidgets.QMainWindow):
    
    def __init__(self):
        super().__init__()
        self.table = Table()
        lst = []
        for rowno in range(200):
            row = []
            for colno in range(10):
                mes = 'Row: {}. Column: {}'.format(rowno,colno)
                row.append(mes)
            lst.append(row)
        model = TableModel(lst)
        self.table.setModel(model)
        self.table.mymodel = model
        self.setCentralWidget(self.table)
        self.setGeometry(100,100,400,400)
        self.set_bindings()
    
    def bind(self,hotkey,action):
        PyQt5.QtWidgets.QShortcut(PyQt5.QtGui.QKeySequence(hotkey),self).activated.connect(action)
    
    def set_bindings(self):
        self.bind('Ctrl+Q',self.close)


if __name__ == '__main__':
    app = PyQt5.QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    app.installEventFilter(window.table)
    window.show()
    app.exec_()
