doc = PyQt5.QtGui.QTextDocument()
#doc.setPlainText('Hello World')

fmt = PyQt5.QtGui.QTextTableFormat()
fmt.setHeight(200)
fmt.setPadding(0.8)
fmt.setBorder(0)
#fmt.setBorderBrush(PyQt5.QtGui.QBrush(PyQt5.QtCore.Qt.SolidPattern))
#brush = PyQt5.QtGui.QBrush(PyQt5.QtCore.Qt.SolidPattern)
#color = PyQt5.QtCore.Qt.GlobalColor(12)
#color = PyQt5.QtGui.QColor().blueF().getRgb()
#color = PyQt5.QtGui.QColor().setBlue()
#print('color type:',type(color),'color:',color)
#self.setStyleSheet('border-width: 1px; border-color: blue;')
#table = cursor.insertTable(5,5)

css = '''.wrapper {height: 200px;}
 .table {position: relative; overflow: hidden; display: table; width: 100%; height: 50%;}
 .table-row {display: table-row; height: 100%;}
 .table-cell {position: relative; overflow: hidden; display: table-cell;}
 .cell-wrap {position: absolute; overflow: hidden; top: 0; left: 0; width: 100%; height: 100%;}
 '''
doc.setDefaultStyleSheet(css)

#prev = cursor.PreviousCell
prev = cursor.NextCell
print('prev cell type:',type(prev),'prev:',prev)
cursor.movePosition(prev)
#self.setTextCursor(cursor)
cursor.insertHtml('<b>Hello</b> <i>there!</i>')

cursor.movePosition(cursor.NextRow)
pos = cursor.position()
print('pos type:',type(pos),'cur pos:',pos)

pos = cursor.position() + 100
cursor.movePosition(13)

fmt = PyQt5.QtGui.QTextTableFormat()
fmt.setWidth(1024)
length = PyQt5.QtGui.QTextLength.FixedLength
PyQt5.QtGui.QTextLength()
length = PyQt5.QtGui.QTextLength(1,150)

self.setSizePolicy(PyQt5.QtWidgets.QSizePolicy.Policy.Minimum,100)
        
fmt = PyQt5.QtGui.QTextTableFormat()
fmt.setHeight(150)
fmt.setPadding(0.8)
fmt.setLeftMargin(1)
fmt.setRightMargin(1)

table = cursor.insertTable(10,10,fmt)
cell = table.cellAt(9,9)
print('type of cell:',type(cell),'cell:',cell)
rowno = cell.row()
print('type(rowno):',type(rowno),'rowno:',rowno)
colno = cell.column()
print('type(colno):',type(colno),'colno:',colno)

cell.setFormat(fmt)

self.setCursor(PyQt5.QtCore.Qt.BlankCursor)
app.setOverrideCursor(PyQt5.QtCore.Qt.BlankCursor)

