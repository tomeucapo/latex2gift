#!/usr/bin/python
# -*- coding: utf-8 -*-

import os 
import sys
from PyQt4 import QtCore, QtGui

from testlatexfile import *
from giftfile import *

from frmPrincipal import Ui_finestraPrincipal

class latex2gift(QtGui.QMainWindow):

    def __init__(self):
        QtGui.QMainWindow.__init__(self)

        self.ui = Ui_finestraPrincipal()
        self.ui.setupUi(self)
     
        self.connect(self.ui.botoConvert, QtCore.SIGNAL("clicked()"), self.onCmdConvertir)
        self.connect(self.ui.botoAfegir, QtCore.SIGNAL("clicked()"), self.onCmdAfegirFitxers)
        self.connect(self.ui.botoLlevarFitxer, QtCore.SIGNAL("clicked()"), self.onCmdLlevarFitxer)
        self.ui.botoLlevarFitxer.setDisabled(1)
        self.ui.botoConvert.setDisabled(1)
                
    def onCmdConvertir(self):
        fitxers = self.ui.llistaFitxersTex
        self.ui.logConversio.clear()
        self.ui.llistaFitxersGIFT.clear()
        self.ui.barraProgress.setMaximum(fitxers.count())

        for i in range(fitxers.count()):
            item = QtGui.QListWidgetItem(fitxers.item(i))
            nomFitxerTex = item.text()
            tf = testLatexFile(nomFitxerTex)
            self.ui.barraProgress.setValue(i+1)

            if tf.parse():
               self.ui.logConversio.append("*** Processat del LaTeX ... Ok!")

               nomFitxerGIFT = nomFitxerTex.replace(".tex", ".gift")
               fitxerGift = giftFile(nomFitxerGIFT)
               fitxerGift.writeQuestions(tf)
               fitxerGift.close()
      
               self.ui.logConversio.append("*** Generat el fitxer "+nomFitxerGIFT)
               self.ui.llistaFitxersGIFT.addItem(nomFitxerGIFT)
            else:
               self.ui.logConversio.append("Hmmmm? El fitxer "+nomFitxerTex+" no pareix esser LaTeX")

            tf.close()


    def onCmdAfegirFitxers(self):
        nom_fitxers = QtGui.QFileDialog.getOpenFileNames(self,
                                                      self.tr("Afegir fitxers a convertir"),
                                                      ".",
                                                      self.tr("TeX Files (*.tex);;All Files (*)"))
        if not nom_fitxers.isEmpty():
           self.ui.llistaFitxersTex.addItems(nom_fitxers)
           self.ui.botoLlevarFitxer.setDisabled(0)
           self.ui.botoConvert.setDisabled(0)     

    def onCmdLlevarFitxer(self):
        print "Llevar"
        


if __name__ == "__main__":
   app = QtGui.QApplication(sys.argv)
   d = latex2gift()
   d.show()
   sys.exit(app.exec_())


