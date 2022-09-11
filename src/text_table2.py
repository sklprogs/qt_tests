#!/usr/bin/python3
# Based on https://gis.stackexchange.com/questions/385616/qtexttable-insert-a-line-in-a-cell

import sys
import PyQt5
import PyQt5.QtWidgets
import PyQt5.QtPrintSupport


class QPrint_Table(PyQt5.QtWidgets.QWidget):

    def __init__(self,table,fields):
        super().__init__()
        self.table = table
        self.fields = fields
        self.printer = PyQt5.QtPrintSupport.QPrinter(PyQt5.QtPrintSupport.QPrinter.HighResolution)
        dialog = PyQt5.QtPrintSupport.QPrintPreviewDialog()
        dialog.paintRequested.connect(self.handlePaintRequest)
        dialog.exec_()

    def handlePaintRequest(self, printer):
        document = self.makeTableDocument()
        document.print_(printer)

    def makeTableDocument(self):
        document = PyQt5.QtGui.QTextDocument()
        cursor = PyQt5.QtGui.QTextCursor(document)
        rows = len(self.table)
        columns = len(self.fields)
        self.pageSize = self.printer.pageRect().size()

        tableFormat = PyQt5.QtGui.QTextTableFormat()
        #tableFormat.setAlignment(PyQt5.QtCore.Qt.AlignRight) # Justify Table
        #tableFormat.setBackground(PyQt5.QtGui.QColor('#e0e0e0'))
        tableFormat.setCellPadding(4)
        tableFormat.setCellSpacing(0)
        tableFormat.setBorder(0)
        tableFormat.setWidth(PyQt5.QtGui.QTextLength(PyQt5.QtGui.QTextLength.PercentageLength, 100))

        table_text = cursor.insertTable(rows+2,columns,tableFormat)
        format_ = table_text.format()
        format_.setHeaderRowCount(1)
        table_text.setFormat(format_)
        format_ = cursor.blockCharFormat()
        format_.setFontWeight(PyQt5.QtGui.QFont.Bold)
        for column in range(columns):
            cursor.setCharFormat(format_)
            cursor.insertText(fields[column])
            cursor.movePosition(PyQt5.QtGui.QTextCursor.NextCell)
            
        table_text.mergeCells(1,0,1,columns)
        cell = table_text.cellAt(1,0)
        format_ = cell.format()
        
        line_option = 4
        if line_option == 1:
            # Option 1 - For black Line
            format_ = cell.format()
            format_.setBackground(PyQt5.QtCore.Qt.black)
            cell.setFormat(format_)
            format_low = cursor.blockCharFormat()
            font = PyQt5.QtGui.QFont('Arial',0)
            font.setPointSizeF(0.9)
            format_low.setFont(font)
            cursor.setCharFormat(format_low)
            cursor.insertText('.') 
        elif line_option == 2:      
            # Option 2 
            cursor.insertHtml('<html> <body> <hr style="height:5px;border-width:3px;color:red;background-color:green"></body> </html>')
        elif line_option == 3:  
            # Option 3
            height = 20
            line_width = self.pageSize.width()
            image = PyQt5.QtGui.QImage(line_width,height,PyQt5.QtGui.QImage.Format_RGB32)
            ratio = self.printer.resolution() / 60
            image.setDevicePixelRatio(ratio)
            painter = PyQt5.QtGui.QPainter(image)
            pen = QPyQt5.QtGui.Pen(PyQt5.QtCore.Qt.red,height*2)
            painter.setPen(pen)
            painter.drawLine(0,0,line_width,0)
            cursor.insertImage(image)
            painter.end()
        elif line_option == 4:
            # Option 4
            format_cell = format_.toTableCellFormat()
            format_cell.setBackground(PyQt5.QtCore.Qt.blue)
            format_cell.setBorder(100)
            format_cell.setBottomBorder(10)
            format_cell.setBottomBorderBrush(PyQt5.QtGui.QBrush(PyQt5.QtGui.QColor("red")))
            
            cell.setFormat(format_cell)

        
        cursor.movePosition(PyQt5.QtGui.QTextCursor.NextCell)
            
        for row in range(rows):
            for column in range(columns):
                cursor.insertText(str(self.table[row][column]))
                cursor.movePosition(PyQt5.QtGui.QTextCursor.NextCell)
        return document

def create_table():
    lst = []
    for i in range(10):
        lst.append([i,'Name '+str(i),'Address '+str(i),'City '+str(i),'Country '+str(i)])
    fields = ['Id','Name','Address','City','Country']
    return lst,fields
    
if __name__ == '__main__':
    app = PyQt5.QtWidgets.QApplication(sys.argv)
    table, fields = create_table()
    QPrint_Table(table,fields)
