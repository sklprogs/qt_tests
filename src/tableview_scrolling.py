import sys
import PyQt5
import PyQt5.QtWidgets


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



class MainWindow(PyQt5.QtWidgets.QMainWindow):
    
    def __init__(self):
        super().__init__()
        self.slider = PyQt5.QtWidgets.QScrollArea()
        self.widget = PyQt5.QtWidgets.QWidget()
        self.layout = PyQt5.QtWidgets.QVBoxLayout()
        self.table = PyQt5.QtWidgets.QTableView()
        self.layout.addWidget(self.table)
        self.widget.setLayout(self.layout)
        self.slider.setWidgetResizable(True)
        self.slider.setWidget(self.widget)
        self.setCentralWidget(self.slider)
        self.vscroll = self.slider.verticalScrollBar()
        # Scrolling does not work without this
        self.slider.setVerticalScrollBarPolicy(PyQt5.QtCore.Qt.ScrollBarAlwaysOn)
        self.set_bindings()
    
    def go_down(self):
        print('Going down...')
        # Required for scrolling; works only after the main widget is shown
        self.vscroll.setMaximum(100)
        #self.slider.ensureVisible(0,1300,50,50)
        #self.slider.ensureVisible(0,100,20,20)
        value = self.vscroll.value()
        print('Scrollbar is at',value)
        self.vscroll.setValue(value + 10)
        value = self.vscroll.value()
        print('Scrollbar moved to',value)
    
    def bind(self,hotkey,action):
        PyQt5.QtWidgets.QShortcut(PyQt5.QtGui.QKeySequence(hotkey),self).activated.connect(action)
    
    def set_bindings(self):
        self.bind('Esc',self.go_down)


if __name__ == '__main__':
    app = PyQt5.QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    rows = []
    for i in range(200):
        row = []
        for j in range(20):
            mes = 'Row: {}. Column: {}'.format(i,j)
            row.append(mes)
        rows.append(row)
    model = TableModel(rows)
    window.table.setModel(model)
    window.show()
    window.setGeometry(300,300,800,600)
    app.exec_()
