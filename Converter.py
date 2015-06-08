#!/usr/bin/python

from PySide import QtGui
import os
import subprocess
import sys
import shutil
import datetime

def main():
    """Look at:
    http://stackoverflow.com/questions/20657753/python-pyside-and-progress-bar-threading
    for an example of a progress bar code.
    """
    app = QtGui.QApplication([])
    dialog = QtGui.QFileDialog()
    dialog.setDirectory("/home/damon/Documents/CODE/Programing/Python/IPython Notebook Folders (links)")
    dialog.setFileMode(QtGui.QFileDialog.ExistingFiles) #allow selection of multiple files
    dialog.filesSelected.connect(callback)
    dialog.setWindowTitle("Select files to convert to slides")
    dialog.show()
    chose_ = dialog.exec_()
    sys.exit()
    
def callback(files):
    """The --reveal-prefix "//cdn.jsdelivr.net/reveal.js/2.4.0" part of the
    command is not necessary if you have a reveal.js folder inside the gh-pages
    folder.  The contents should be downloaded as a zip from
        http://www.jsdelivr.com/#!reveal.js
    then extracted into that folder.  Note that these new slides should be 
    tested to see if the latest version of reveal.js has broken them.
    """
    Conversion = """Conversion will start upon clicking OK. 
This process may take somme time, but you will 
be notified upon completion, or errors."""
    msgBox = QtGui.QMessageBox()
    msgBox.setText(Conversion)
    msgBox.exec_()
    cmd = 'ipython nbconvert "%s" --to slides'
    path = files[0].rsplit('/',1)[0]
    os.chdir(path)
    path = os.getcwd()
    parts = path.rsplit('/',1)
    slide_path = '/'.join([parts[0],parts[1]+"-gh-pages",parts[1]]) + '/'
    er = 0
    for f in files:
        name = f.split('/')[-1]
        slides = name.split('.')[0] + '.slides.html'
        new_path = slide_path + slides
        try:
            subprocess.call(cmd%f,shell=True)
            shutil.move(slides, new_path)
        except:
            error = "Failed for %s\n\nslides = %s\nnew_path = %s"%(name,slides,new_path)
            print error
            log_error(path,error,er)
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
    Path = slide_path
    msgBox.setText('Slides where moved to:\n%s\nBe sure to update github.io'%Path)
    msgBox.exec_()
    
def log_error(path,message,count):
    if count == 0:
        Date = '\n\n'+datetime.datetime.now()
    else:
        Date = ''
    if path[-1] != '/':
        file_path = path+'/'+'error.log'
    else:
        file_path = path+'error.log'
    try:
        with open(file_path,'r')as f:
            er_text = f.read()
    except:
        er_text = ''
    er_text += Date+'\n'+message
    with open(file_path,'w')as f:
        f.write(er_text)
    
if __name__ == '__main__':
    main()
