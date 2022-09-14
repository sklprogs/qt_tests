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
        self.table = PyQt5.QtWidgets.QTableView()
        self.slider = PyQt5.QtWidgets.QScrollArea()
        self.slider.setWidgetResizable(True)
        self.slider.setWidget(self.table)
        self.setCentralWidget(self.slider)


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
    app.exec_()
