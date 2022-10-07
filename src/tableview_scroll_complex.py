import sys
import PyQt5
import PyQt5.QtWidgets


class TableDelegate(PyQt5.QtWidgets.QStyledItemDelegate):
    # akej74, https://stackoverflow.com/questions/35397943/how-to-make-a-fast-qtableview-with-html-formatted-and-clickable-cells
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.rowno = 0
        self.colno = 0
    
    def paint(self,painter,option,index):
        options = PyQt5.QtWidgets.QStyleOptionViewItem(option)
        self.initStyleOption(options,index)
        
        if options.widget:
            style = options.widget.style()
        else:
            style = PyQt5.QtWidgets.QApplication.style()
            
        style.drawControl(PyQt5.QtWidgets.QStyle.CE_ItemViewItem,options,painter)
        ctx = PyQt5.QtGui.QAbstractTextDocumentLayout.PaintContext()
        
        textRect = style.subElementRect(PyQt5.QtWidgets.QStyle.SE_ItemViewItemText,options)
        
        if index.row() == self.rowno and index.column() == self.colno:
            color = PyQt5.QtGui.QColor('red')
            pen = PyQt5.QtGui.QPen(color,2)
            painter.setPen(pen)
            # Avoid intersecting cell borders and artifacts as the result
            x1, y1, x2, y2 = option.rect.getCoords()
            option.rect.setCoords(x1+1,y1+1,x2-1,y2-1)
            painter.drawRect(option.rect)
        
        painter.save()
    
        painter.translate(textRect.topLeft())
        # Hide too long text; do not allow cells to overlap
        painter.setClipRect(textRect.translated(-textRect.topLeft()))
    
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
        return len(self._data[0])



class Table(PyQt5.QtWidgets.QTableView):
    
    def __init__(self):
        super().__init__()
        self.rownum = 200
        self.colnum = 10
        self.y = []
        self.delegate = TableDelegate()
        self.setItemDelegate(self.delegate)
        self.vscroll = self.verticalScrollBar()
        self.set_row_height()
    
    def set_row_height(self,height=42):
        for no in range(self.rownum):
            self.setRowHeight(no,height)
    
    def select(self,rowno,colno):
        if rowno == self.delegate.rowno and colno == self.delegate.colno:
            return
        self.mymodel.update(self.delegate.rowno,self.delegate.colno)
        self.mymodel.update(rowno,colno)
        self.delegate.rowno = rowno
        self.delegate.colno = colno
    
    def set_all_y(self):
        for rowno in range(self.rownum):
            self.y.append(self.rowViewportPosition(rowno))
        print(self.y)
    
    def get_page_y(self,y):
        height = self.height()
        print('Table height:',height)
        y += 42
        page_no = int(y/height)
        print('Page #{}'.format(page_no))
        y = page_no * height
        #y = page_no * height + (page_no + 1) * 42
        mes = 'Page Y: {}'.format(y)
        print(mes)
        return y
    
    def get_scroll(self,y):
        max_ = self.vscroll.maximum()
        #TODO: do not hardcode row height
        #y += 42
        y = self.get_page_y(y)
        scrolly = int((max_*y)/(self.y[-1]))
        mes = 'Scrolling percentage: {}'.format(scrolly)
        print(mes)
        return scrolly
    
    def print_cell(self):
        mes = '"' + self.matrix[self.delegate.rowno][self.delegate.colno] + '"'
        print(mes)
    
    def set_scroll(self,y):
        self.vscroll.setValue(0)
        percent = self.get_scroll(y)
        self.vscroll.setValue(percent)
        self.print_cell()
    
    def show_row(self,rowno):
        y = self.y[rowno]
        self.set_scroll(y)
    
    def go_down(self):
        rowno = self.delegate.rowno
        colno = self.delegate.colno
        next_rowno = rowno + 1
        self.select(rowno,colno)
        self.show_row(rowno)



class App(PyQt5.QtWidgets.QMainWindow):
    
    def __init__(self):
        super().__init__()
        self.table = Table()
        self.setCentralWidget(self.table)
        self.setGeometry(300,200,800,600)
        PyQt5.QtWidgets.QShortcut(PyQt5.QtGui.QKeySequence('Down'),self).activated.connect(self.table.go_down)
    
    def fill(self):
        self.table.matrix = []
        for i in range(self.table.rownum):
            row = []
            for j in range(self.table.colnum):
                mes = 'Row {}. Column {}'.format(i+1,j+1)
                row.append(mes)
            self.table.matrix.append(row)
        self.table.mymodel = TableModel(self.table.matrix)
        self.table.setModel(self.table.mymodel)


if __name__ == '__main__':
    exe = PyQt5.QtWidgets.QApplication(sys.argv)
    app = App()
    app.fill()
    app.table.set_all_y()
    app.show()
    exe.exec_()
