# MUST BE RUN FROM TERMINAL!  Must also use Python 2 (not 3)
# python Search_n_Replace.py

import sys
import os
from PySide.QtCore import SIGNAL
from PySide import QtGui
import shutil

def main():
    """Even though this is a GUI application there is a fault in it that requires
    it to be run from the comand line.  As it is, if it is exicuted from 
    Nautilus it creates three files titled sys, os, and shutil (upon mouse 
    clicks) then quits.
    
    Created: August 13, 2014
    
    """
    app = QtGui.QApplication([])
    form = Form()
    form.show()
    #print form.Replace

    choice = form.exec_()
    global var
    var = [form.Search.encode('ascii', errors='backslashreplace'), form.Replace.encode('ascii', errors='backslashreplace')]
    #print choice
    #print "var = %s"%var
    if choice == 1:
        dialog = QtGui.QFileDialog()
        dialog.setDirectory("/home/damon/Documents/CODE/Programing/Python/IPython Notebook Folders (links)")
        dialog.setFileMode(QtGui.QFileDialog.ExistingFiles) #allow selection of multiple files
        dialog.filesSelected.connect(callback)
        dialog.setWindowTitle('Select Notebooks to have the git Path Updated')
        dialog.show()
        #dialog.change = [form.Search, form.Replace]
        chose_ = dialog.exec_()
    sys.exit()


class Form(QtGui.QDialog):
    def __init__(self, parent=None):
        super(Form, self).__init__(parent)
        self.Replace = ''
        self.Search = ''
        self.resize(450, 100)
        #self.browser = QtGui.QTextBrowser()
        self.search_label = QtGui.QLabel("Type the text to be replaced here")
        self.search = QtGui.QLineEdit()
        self.search.setPlaceholderText("Type the text to be replaced here")
        #self.search.selectAll()
        self.replace_label = QtGui.QLabel("Type the replacement text here")
        self.replace = QtGui.QLineEdit()
        self.replace.setPlaceholderText("Type the replacement text here")
        self.buttonBox = QtGui.QDialogButtonBox()
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        
        layout = QtGui.QVBoxLayout()
        layout.addWidget(self.search_label)
        layout.addWidget(self.search)
        layout.addWidget(self.replace_label)
        layout.addWidget(self.replace)
        layout.addWidget(self.buttonBox)
        self.setLayout(layout)
        
        self.search.setFocus()
        
        self.connect(self.search, SIGNAL('editingFinished()'),self.Next)
        self.connect(self.replace, SIGNAL('editingFinished()'),self.Final)
        self.connect(self.buttonBox, SIGNAL('accepted()'),self.OK)
        self.connect(self.buttonBox, SIGNAL('rejected()'),self.Cancel)
        
        self.setWindowTitle('Update git Path in IPython Notebooks')
        
        
    def Next(self):
        #self.replace.selectAll()
        self.Search = self.search.text()
        #print self.Search
        self.replace.setFocus()
    
    def Final(self):
        #self.buttonBox.setFocus()
        self.Replace = self.replace.text()
        #print self.Replace
        self.search.setFocus()
    
    def OK(self):
        print 'OK pressed'
        Search = self.Search
        Replace = self.Replace
        self.accept()
        self._end()
        
    def Cancel(self):
        print 'Cancel pressed'
        self.reject()
        self._end()
    
    def _end(self):
        print 'exit'
        
        
def callback(files):
    """This searches all the selected files for the search string and replaces
    them with the replacement string.
    """
    print var
    #cmd = 'ipython nbconvert "%s" --to slides'
    path = files[0].rsplit('/',1)[0]
    os.chdir(path)
    parts = path.rsplit('/',1)
    back_path = path + '/backup/'
    if not os.path.exists(back_path):
        os.mkdir(back_path)
    er = 0
    for f in files:
        name = f.split('/')[-1]
        new_path = back_path + name
        try:
            #subprocess.call(cmd%f,shell=True)
            out = []
            #print '1 here'
            with open(name, 'r') as FF:
                for line in FF:
                    out.append(line.replace(var[0],var[1]))
            #print '2 here'
            shutil.move(name, new_path)
            #print '3 here'
            new_name = name#.replace('.','_dh.')
            #print '4 here - len(out) = %d'%len(out)
            with open(new_name, 'w') as FF:
                #print '4.1 here'
                #text = '\n'.join(out)
                #print '4.2 here'
                for line in out:
                    FF.write(line)
            #print '5 here'
            pass
        except:
            error = "Failed for %s"%name
            print error
            msgBox = QtGui.QMessageBox()
            msgBox.setText(error)
            msgBox.exec_()
            er += 1
            if er>2:
                msgBox = QtGui.QMessageBox()
                msgBox.setText('Too many errors occured.\nEnding conversion')
                msgBox.exec_()
                break
    msgBox = QtGui.QMessageBox()
    Path = back_path[:-1]
    bak_txt = 'Files where backedup in:\n%s'%Path
    print(bak_txt)
    msgBox.setText(bak_txt)
    msgBox.exec_()
        
        
if __name__ == '__main__':
    main()        
#app = QtGui.QApplication(sys.argv)


