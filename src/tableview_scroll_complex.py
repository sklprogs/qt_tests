import sys
import PyQt5
import PyQt5.QtWidgets

from skl_shared_qt.localize import _
import skl_shared_qt.shared as sh


class TableDelegate(PyQt5.QtWidgets.QStyledItemDelegate):
    # akej74, https://stackoverflow.com/questions/35397943/how-to-make-a-fast-qtableview-with-html-formatted-and-clickable-cells
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.match_index = 0
    
    def paint(self,painter,option,index):
        options = PyQt5.QtWidgets.QStyleOptionViewItem(option)
        self.initStyleOption(options,index)
        style = options.widget.style()
        style.drawControl(PyQt5.QtWidgets.QStyle.CE_ItemViewItem,options,painter)
        
        if index == self.match_index:
            color = PyQt5.QtGui.QColor('red')
            pen = PyQt5.QtGui.QPen(color,2)
            painter.setPen(pen)
            # Avoid intersecting cell borders and artifacts as the result
            x1, y1, x2, y2 = option.rect.getCoords()
            option.rect.setCoords(x1+1,y1+1,x2-1,y2-1)
            painter.drawRect(option.rect)
        
        painter.save()
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
    
    def update(self,index_):
        self.dataChanged.emit(index_,index_)



class Table(PyQt5.QtWidgets.QTableView):
    
    def __init__(self):
        super().__init__()
        self.rownum = 200
        self.colnum = 10
        self.delegate = TableDelegate()
        self.setItemDelegate(self.delegate)
        self.set_row_height()
    
    def go_down(self):
        f = '[QtTests] tableview_scroll_complex.Table.go_down'
        old_index = self.currentIndex()
        rowno = old_index.row()
        colno = old_index.column()
        #TODO: elaborate
        rowno += 1
        new_index = self.mymodel.index(rowno,colno)
        self.setCurrentIndex(new_index)
        self.delegate.match_index = new_index
        self.mymodel.update(old_index)
        self.mymodel.update(new_index)
    
    def scroll_top(self):
        f = '[QtTests] tableview_scroll_complex.Table.scroll_top'
        print('Scrolling top...')
        height = self.height()
        index_ = self.currentIndex()
        rowno = index_.row()
        colno = index_.column()
        y = self.rowViewportPosition(rowno)
        row_height = self.rowHeight(rowno)
        page_y = y - height + 2 * row_height
        page_row_no = self.rowAt(page_y)
        new_index = self.mymodel.index(page_row_no,colno)
        mes = _('Table height: {}, row #{}, column #{}, row height: {}, row Y: {}, page Y: {}, page row #{}')
        mes = mes.format(height,rowno,colno,row_height,y,page_y,page_row_no)
        sh.objs.get_mes(f,mes,True).show_debug()
        #self.scrollTo(new_index,PyQt5.QtWidgets.QAbstractItemView.PositionAtTop)
        self.scrollTo(new_index,PyQt5.QtWidgets.QAbstractItemView.PositionAtTop)
    
    def keyPressEvent(self,event):
        #if event.key() == PyQt5.QtCore.Qt.Key_Down:
        if event.key() == PyQt5.QtCore.Qt.Key_Q:
            print('Going down...')
            self.go_down()
            #self.print_cell()
        super().keyPressEvent(event)
            
    def set_row_height(self,height=42):
        for no in range(self.rownum):
            self.setRowHeight(no,height)
    
    def print_cell(self):
        index_ = self.currentIndex()
        mes = '"' + str(self.mymodel.data(index_)) + '"'
        sh.objs.get_mes(f,mes,True).show_debug()



class App(PyQt5.QtWidgets.QMainWindow):
    
    def __init__(self):
        super().__init__()
        self.table = Table()
        self.setCentralWidget(self.table)
        self.setGeometry(300,200,800,600)
        #PyQt5.QtWidgets.QShortcut(PyQt5.QtGui.QKeySequence('Down'),self).activated.connect(self.table.go_down)
        PyQt5.QtWidgets.QShortcut(PyQt5.QtGui.QKeySequence('x'),self).activated.connect(self.table.scroll_top)
    
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
    app.show()
    exe.exec_()
