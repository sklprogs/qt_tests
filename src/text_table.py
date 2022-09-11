#!/usr/bin/python3
# https://gis.stackexchange.com/questions/385616/qtexttable-insert-a-line-in-a-cell

from PyQt5.QtWidgets import QApplication ,QWidget
from PyQt5.QtPrintSupport import QPrinter,QPrintPreviewDialog
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QTextDocument,QTextCursor,QPainter,QFont,QImage,QTextTableFormat,QPixmap,QTextLength,QPixmap,QTextBlockFormat,QTextCharFormat,QPen,QTextFrameFormat,QIcon,QColor,QBrush


class QPrint_Table(QWidget):
    def __init__(self,table,fields):
        super().__init__()
        self.table=table
        self.fields=fields
        self.printer = QPrinter(QPrinter.HighResolution)
        dialog = QPrintPreviewDialog()
        dialog.paintRequested.connect(self.handlePaintRequest)
        dialog.exec_()

    def handlePaintRequest(self, printer):
        document = self.makeTableDocument()
        document.print_(printer)

    def makeTableDocument(self):
        document = QTextDocument()
        cursor = QTextCursor(document)
        rows = len(self.table)
        columns = len(self.fields)
        self.pageSize = self.printer.pageRect().size()

        tableFormat = QTextTableFormat()
        #tableFormat.setAlignment(QtCore.Qt.AlignRight) # Justify Table
        #tableFormat.setBackground(QtGui.QColor('#e0e0e0'))
        tableFormat.setCellPadding(4)
        tableFormat.setCellSpacing(0)
        tableFormat.setBorder(0)
        tableFormat.setWidth(QTextLength(QTextLength.PercentageLength, 100))

        table_text = cursor.insertTable(rows + 2, columns, tableFormat)
        format = table_text.format()
        format.setHeaderRowCount(1)
        table_text.setFormat(format)
        format = cursor.blockCharFormat()
        format.setFontWeight(QFont.Bold)
        for column in range(columns):
            cursor.setCharFormat(format)
            cursor.insertText(fields[column])
            cursor.movePosition(QTextCursor.NextCell)
            
        table_text.mergeCells(1,0,1,columns)
        cell=table_text.cellAt(1,0)
        format =cell.format()
        
        line_option=4
        if line_option==1:
            # Option 1 - For black Line
            format =cell.format()
            format.setBackground(Qt.black)
            cell.setFormat(format)  
            format_low=cursor.blockCharFormat()
            font=QFont ( "Arial" , 0 )
            font.setPointSizeF(0.9)
            format_low.setFont(font)
            cursor.setCharFormat(format_low)
            cursor.insertText('.') 
        elif line_option==2:      
            # Option 2 
            cursor.insertHtml('<html> <body> <hr style="height:5px;border-width:3px;color:red;background-color:green"></body> </html>')
        elif line_option==3:  
            # Option 3
            height=20
            line_width=self.pageSize.width()
            image = QImage(line_width,height,QImage.Format_RGB32)
            ratio=self.printer.resolution()/60
            image.setDevicePixelRatio(ratio)
            painter = QPainter(image)
            pen = QPen(Qt.red, height*2)
            painter.setPen(pen)
            painter.drawLine(0, 0, line_width, 0)
            cursor.insertImage(image)
            painter.end()
        elif line_option==4:
            # Option 4
            format_cell=format.toTableCellFormat()
            format_cell.setBackground(Qt.blue)
            format_cell.setBorder(100)
            format_cell.setBottomBorder(10)
            format_cell.setBottomBorderBrush(QBrush(QColor("red")))
            
            cell.setFormat(format_cell)

        
        cursor.movePosition(QTextCursor.NextCell)
            
        for row in range(rows):
            for column in range(columns):
                cursor.insertText(str(self.table[row][column]))
                cursor.movePosition(QTextCursor.NextCell)
        return document

def create_table():
    list=[]
    for i in range(10):
        list.append([i,'Name '+str(i),'Address '+str(i),'City '+str(i),'Country '+str(i)])
    fields=['Id','Name','Address','City','Country']
    return list,fields
    
if __name__ == '__main__':

    import sys
    app = QApplication(sys.argv)
    table,fields=create_table()
    QPrint_Table(table,fields)
