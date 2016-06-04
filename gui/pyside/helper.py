from PySide import QtCore, QtGui, QtUiTools

def load_ui_widget(uifilename, parent=None):
    loader = QtUiTools.QUiLoader()
    uifile = QtCore.QFile(uifilename)
    uifile.open(QtCore.QFile.ReadOnly)
    ui = loader.load(uifile, parent)
    uifile.close()
    return ui

def load_image(label, image):
    my_pixmap = QtGui.QPixmap(image)
    my_scaled_pixelmap = my_pixmap.scaled(label.size(), QtCore.Qt.KeepAspectRatio)
    label.setPixmap(my_scaled_pixelmap)