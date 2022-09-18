#!/usr/bin/python3
# -*- coding: UTF-8 -*-

import PyQt5
import PyQt5.QtWidgets

from skl_shared_qt.localize import _
import skl_shared_qt.shared as sh


class App:
    
    def __init__(self):
        self.set_gui()
    
    def show(self):
        self.widget.showMaximized()
        #self.widget.show()
    
    def set_gui(self):
        self.widget = PyQt5.QtWidgets.QMainWindow()
        self.panel = Panel()
        self.widget.setCentralWidget(self.panel.widget)



class Panel:

    def __init__(self):
        self.set_values()
        self.set_gui()
    
    def set_gui(self):
        self.widget = PyQt5.QtWidgets.QWidget()
        self.layout = PyQt5.QtWidgets.QHBoxLayout()
        self.set_buttons()
        self.layout.addWidget(self.btn_trn.widget)
        self.layout.addWidget(self.btn_clr.widget)
        self.layout.addWidget(self.btn_ins.widget)
        self.layout.addWidget(self.btn_rp1.widget)
        self.layout.addWidget(self.btn_rp2.widget)
        self.layout.setContentsMargins(4,4,4,4)
        self.widget.setLayout(self.layout)
    
    def set_buttons(self):
        self.btn_trn = sh.Button (hint = _('Translate')
                                 ,inactive = self.icn_ret
                                 ,active = self.icn_ret
                                 )
        self.btn_clr = sh.Button (hint = _('Clear search field')
                                 ,inactive = self.icn_clr
                                 ,active = self.icn_clr
                                 )
        self.btn_ins = sh.Button (hint = _('Paste text from clipboard')
                                 ,inactive = self.icn_ins
                                 ,active = self.icn_ins
                                 )
        self.btn_rp1 = sh.Button (hint = _('Paste current request')
                                 ,inactive = self.icn_rp0
                                 ,active = self.icn_rp1
                                 )
        self.btn_rp2 = sh.Button (hint = _('Paste previous request')
                                 ,inactive = self.icn_r20
                                 ,active = self.icn_r21
                                 )
    
    def set_values(self):
        self.icn_ret = sh.objs.get_pdir().add ('..','resources','buttons'
                                              ,'go_search.svgz'
                                              )
        self.icn_clr = sh.objs.pdir.add ('..','resources','buttons'
                                        ,'clear_search_field.svgz'
                                        )
        self.icn_ins = sh.objs.pdir.add ('..','resources','buttons'
                                        ,'paste.svgz'
                                        )
        self.icn_rp0 = sh.objs.pdir.add ('..','resources','buttons'
                                        ,'repeat_sign_off.svgz'
                                        )
        self.icn_rp1 = sh.objs.pdir.add ('..','resources','buttons'
                                        ,'repeat_sign.svgz'
                                        )
        self.icn_r20 = sh.objs.pdir.add ('..','resources','buttons'
                                        ,'repeat_sign2_off.svgz'
                                        )
        self.icn_r21 = sh.objs.pdir.add ('..','resources','buttons'
                                        ,'repeat_sign2.svgz'
                                        )



if __name__ == '__main__':
    import sys
    exe = PyQt5.QtWidgets.QApplication(sys.argv)
    app = App()
    '''
    app.set_gui()
    data = [['helLo','I Am Here','Hello there!']
           ,['distinct','creation','suffering']
           ,['tree','as;f,d','sdafsdfasdfasdfsdfsdfsd']
           ]
    
    global model
    model = TableModel(data)
    app.table.setModel(model)
    '''
    app.show()
    sys.exit(exe.exec_())
