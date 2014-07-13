#!/usr/bin/python

import re

class latexFile(file):
      def __init__(self, nomFitxer): 
          file.__init__(self, nomFitxer)
          self.liniaAct = self.readline() 
       
      def llegeixEnv(self, tipus, nom):
          strRE = r"^\\%(type)s{%(nam)s}$" % {"type": tipus, "nam": nom}       
          return re.findall(strRE, self.liniaAct.rstrip())

      def llegeixCmd(self, cmd):
          strRE = r"^\\%(cmd)s({|\s)((\w(\s|))*)(}|)" % {"cmd": cmd}
          return re.search(strRE, self.liniaAct.rstrip()) 

      def llegeixCmdInt(self,cmd):
          strRE = r"^\\%(cmd)s$"
          return re.search(strRE, self.liniaAct.rstrip())

      def llegeixDef(self, nomDef):
          strRE = r"^\\def\\%(nom)s(#[0-9]|){(.+)}$" % {"nom": nomDef}
          return re.search(strRE, self.liniaAct.rstrip())

      def eof(self):
          return (not self.liniaAct)     
   
      def nextLine(self):
          self.liniaAct = self.readline()
         
class testLatexFile(latexFile):
      def __init__(self, nomFitxer):
          latexFile.__init__(self, nomFitxer)
          self.estat = -1
          self.paramTest = {"title":      "",
                            "adaptative": False,
                            "time":       0}

          self.questions = {} 
	  self.lastVersion = {}
          self.lastDefId = ""

      def initState(self): 
          self.estat = -1

      def beginDocument(self):
          if(self.llegeixEnv("begin", "document")):
             print "Inici de document..."
             self.estat = self.estat + 1

      def endDocument(self):
          if(self.llegeixEnv("end", "document")):
             print "Final del document..."

      def introTest(self):
          if(self.llegeixEnv("begin", "introtest")):
             print "Inici parametres..."
             self.estat = self.estat + 1

      def llegeixParametresTest(self):
          if(self.llegeixEnv("end", "introtest")):
             print self.paramTest 
             print "Final de parametres..."
             self.estat = self.estat + 1
          else:
             tc = self.llegeixCmd("titletest")             
             if tc:
                self.paramTest["title"] = tc.groups()[1]
             else:
                ad = self.llegeixCmd("adaptativetest")
                if ad:
                   self.paramTest["adaptative"] = (ad.groups()[1].upper() == "YES") 
                else:
                   tt = self.llegeixCmd("timetest")
                   if tt:
                      self.paramTest["time"] = int(tt.groups()[1])
         
      def llegeixQuestions(self):
	  print "Llegint questions..."
          nq = self.llegeixCmd("newquestion")
	  if nq:
	     print "	Nova questio"
	     self.lastDefId = nq.groups()[1]
	     defQuestio = {"tipus":    "",
			   "enunciat": "",
			   "versions": []} 

             self.questions[self.lastDefId] =defQuestio
          else:
             dq = self.llegeixDef(self.lastDefId)
	     if dq:
                self.questions[self.lastDefId]["enunciat"] = dq.groups()[1]
                self.estat = self.estat + 1
      
      def llegeixVersions(self):
	  nv = self.llegeixCmd(self.lastDefId)
          if nv:
             print "Versions de :",self.lastDefId
	     print nv.groups()
   	     self.lastVersion = {"enunciat": nv.groups()[1],
		                 "respostes": []}
          else:
             na = self.llegeixCmd("answer")
	     if na:
		self.lastVersion["respostes"].append(na.groups()[1])
             else:
		self.questions[self.lastDefId]["versions"].append(self.lastVersion)
	        self.estat = self.estat+1

      def novaQuestio(self):		
          np = self.llegeixCmdInt("newpage")     
          if np:
             print "Final de la questio"			
             self.estat = 2
	  else:
             self.estat = 3 


      estatsPosibles = {-1: beginDocument,
                         0: introTest,
                         1: llegeixParametresTest,
                         2: llegeixQuestions,
			 3: llegeixVersions, 
			 4: novaQuestio, 
		        99: endDocument	 
		       }

      def parse(self):
          while not self.eof():
                self.estatsPosibles.get(self.estat, self.initState)(self)
                self.nextLine()

          return(not self.estat<0)

if __name__ == "__main__":
   tf = testLatexFile("test1.tex")

   if tf.parse():
      print tf.questions
   else:
      print "El fitxer no pareix esser LaTeX"


   tf.close()
