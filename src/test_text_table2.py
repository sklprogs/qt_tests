#!/usr/bin/python3

import sys
import PyQt5
import PyQt5.QtWidgets


class Table(PyQt5.QtWidgets.QTextEdit):

    def __init__(self):
        super().__init__()
        self.set_gui()

    def set_max_col_width(self):
        #TODO: elaborate
        constraints = [PyQt5.QtGui.QTextLength(PyQt5.QtGui.QTextLength.FixedLength,63)
                      ,PyQt5.QtGui.QTextLength(PyQt5.QtGui.QTextLength.FixedLength,63)
                      ,PyQt5.QtGui.QTextLength(PyQt5.QtGui.QTextLength.FixedLength,63)
                      ,PyQt5.QtGui.QTextLength(PyQt5.QtGui.QTextLength.FixedLength,63)
                      ,PyQt5.QtGui.QTextLength(PyQt5.QtGui.QTextLength.FixedLength,221)
                      ,PyQt5.QtGui.QTextLength(PyQt5.QtGui.QTextLength.FixedLength,221)
                      ,PyQt5.QtGui.QTextLength(PyQt5.QtGui.QTextLength.FixedLength,221)
                      ,PyQt5.QtGui.QTextLength(PyQt5.QtGui.QTextLength.FixedLength,221)
                      ,PyQt5.QtGui.QTextLength(PyQt5.QtGui.QTextLength.FixedLength,221)
                      ,PyQt5.QtGui.QTextLength(PyQt5.QtGui.QTextLength.FixedLength,221)
                      ]
        self.fmt.setColumnWidthConstraints(constraints)
    
    def enable_borders(self):
        self.fmt.setBorder(True)
    
    def disable_borders(self):
        self.fmt.setBorder(False)
    
    def set_spacing(self,value=0):
        # Set a distance between adjacent cells (integer)
        self.fmt.setCellSpacing(value)
    
    def set_widgets(self):
        self.doc = PyQt5.QtGui.QTextDocument()
        self.cursor = PyQt5.QtGui.QTextCursor(self.textCursor())
        self.fmt = PyQt5.QtGui.QTextTableFormat()
    
    def set_border_color(self,color='darkgray'):
        brush = PyQt5.QtGui.QBrush(PyQt5.QtCore.Qt.SolidPattern)
        color = PyQt5.QtGui.QColor(color)
        brush.setColor(color)
        self.fmt.setBorderBrush(brush)
    
    def create_table(self,rownum,colnum):
        # Do this only after 'fmt' is fully adjusted but before selecting cells
        self.table = self.cursor.insertTable(rownum,colnum,self.fmt)
    
    def set_cell_by_no(self,no):
        ''' Go to a cell by its number starting from 1. If the cell number is
            outside of table boundaries, only a warning is shown, but no
            exception is thrown. -1 is automatically corrected to 1, positions
            after the end - to the end.
        '''
        self.cursor.setPosition(no)
        self.cell = self.table.cellAt(no)
    
    def set_cell_by_index(self,rowno,colno):
        ''' Return a cell by rowno, colno as PyQt5.QtGui.QTextTableCell. Unlike
            `setPosition`, numbers start from 0 when using `cellAt`. If a cell
            number is outside of table boundaries, a segmentation fault will be
            thrown.
        '''
        self.cell = self.table.cellAt(rowno,colno)
        self.cursor = self.cell.firstCursorPosition()                                                                                                                                                 
        self.setTextCursor(self.cursor)
    
    def fill(self):
        #TODO: elaborate
        self.cursor.insertHtml('<b>Hello</b> <i>there!</i>')
    
    def set_cell_bg(self,color='cyan'):
        cell_fmt = self.cell.format()
        cell_fmt.setBackground(PyQt5.QtGui.QColor(color))
        self.cell.setFormat(cell_fmt)
    
    def set_cell_border(self,color='red'):
        # Not working yet
        # QTextCharFormat
        cell_fmt = self.cell.format()
        pen = cell_fmt.textOutline()
        brush = pen.brush()
        qcolor = PyQt5.QtGui.QColor(color)
        brush.setColor(qcolor)
        pen.setColor(qcolor)
        pen.setBrush(brush)
        cell_fmt.setTextOutline(pen)
        self.cell.setFormat(cell_fmt)
    
    def disable_cursor(self):
        self.setReadOnly(True)
    
    def enable_cursor(self):
        self.setReadOnly(False)
    
    def set_cell(self):
        #TODO: choose one of the methods
        self.set_cell_by_no(100)
        #self.set_cell_by_index(9,9)
        self.set_cell_bg('cyan')
        #self.set_cell_border('red')
    
    def set_gui(self):
        self.set_widgets()
        self.set_max_col_width()
        self.set_spacing(0)
        self.set_border_color()
        self.disable_borders()
        self.disable_cursor()
        self.create_table(10,10)
        self.set_cell()
        self.fill()


if __name__ == '__main__':
    app = PyQt5.QtWidgets.QApplication(sys.argv)
    itable = Table()
    itable.showMaximized()
    app.exec_()
