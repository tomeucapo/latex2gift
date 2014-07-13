#!/usr/bin/python
# -*- coding: utf-8 -*-

from testlatexfile import *
from giftfile import *
import os 
import sys

if __name__ == "__main__":
   if len(sys.argv)<2:
      print "LaTeX to GIFT Conversor v.1.00\n"
      print "Usage: latex2gift [latexfile] [giftfile]"
      sys.exit(-1)

   if not os.path.exists(sys.argv[1]):
      print "El fitxer "+sys.argv[1]+" que vol convertir no existeix!"
      sys.exit(-1) 

   tf = testLatexFile(sys.argv[1])

   if tf.parse():
      print "\n\n*** Processat del LaTeX ... Ok!"

      fitxerGift = giftFile(sys.argv[2])
      fitxerGift.writeQuestions(tf)
      fitxerGift.close()
      
      print "*** Generat el fitxer GIFT "+sys.argv[2]
   else:
      print "Hmmmm? El fitxer no pareix esser LaTeX"

   tf.close()

