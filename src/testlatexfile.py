#!/usr/bin/python

from latexfile import *
        
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
          self.enunciats = []

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
          nq = self.llegeixCmd("newquestion")
	  if nq:
             p=re.compile("\{([^{}]*)\}")
             params = p.findall(self.liniaAct)

	     self.lastDefId = params[0]
             self.lastType = params[1]

	     print "*** Nova questio ",self.lastDefId
             defQuestio = {"tipus":    params[1],
			   "enunciat": "",
			   "versions": []} 
             self.questions[self.lastDefId] =defQuestio
          else:
             dq = self.llegeixDef(self.lastDefId)
             if dq:
                print "    Afegida definicio",self.lastDefId
                print "   ",dq.groups()[2]
                self.questions[self.lastDefId]["enunciat"] = dq.groups()[2]
                if re.search(r"^multiple choice.*", self.lastType):
                   print "Ara llegirem Multiple Choice"
                   self.estat = 10
                else:
                   self.estat = self.estat + 1

      ###########################################################################
      # Metodes per a llegir multiple choices
  
      def llegeixVersionsMC(self):
          if self.llegeixCmdInt("%(def)s{" % {"def": self.lastDefId}):
             print "Llegim respostes possibles"
             self.estat = self.estat + 1
             self.lastVersion = {"respCorrectes": [],
                                 "respostes": []}
             self.enunciats=[] 
          else:
             if re.findall(r"^}$", self.liniaAct.rstrip()):
                print "Final de versio"
                self.estat = 12             
             else:
                np = self.llegeixCmdInt("newpage")
                if np:
                   self.enunciats = []
                   print "Final de la questio"
                   self.estat = 2
                 
      def llegeixRespostaMC(self):
          na = re.findall(r"\\verb", self.liniaAct)
	  if na:
             p=re.compile("\?(.*)\?")
             answer = p.findall(self.liniaAct)
             if answer:
                print "   ",answer[0]
	        self.lastVersion["respostes"].append(answer[0])
          else:
             if self.llegeixEnv("end","enumerate"):
                self.estat = 10 

      def llegeixRespostesOKMC(self):
          na = self.llegeixCmd("answer")
          if na:
             p=re.compile("\?(.*)\?")
             answer = p.findall(self.liniaAct)
             if answer:
                print "   ",answer[0]
                self.lastVersion["respCorrectes"] = [int(a) for a in answer[0].split()]
          else:
             self.questions[self.lastDefId]["versions"].append(self.lastVersion)
             self.estat = 10
 
      ###########################################################################
      # Metodes per llegir short answers
 
      def acabaVer(self):
          self.estat = 4
          print "    Versions de :",self.lastDefId
          self.lastVersion = {"enunciat": self.enunciats,
                              "respostes": []}
          self.enunciats=[] 
     
      def llegeixVersions(self):
             linia = self.liniaAct.rstrip()
             print linia

             nv = self.llegeixCmd(self.lastDefId)
             if nv:
                enunciat = re.findall(r"\{(.*)\}%$",linia)
                if(len(enunciat)>0):
                  self.enunciats.append(enunciat[0])
                else:
                  enunciat = re.findall(r"\{(.*)\}\\\\$",linia)
                  if(len(enunciat)>0):
                     self.enunciats.append(enunciat[0])
                     self.acabaVer()
             else:
                np = self.llegeixCmdInt("newpage")     
                if np:
                   self.enunciats = [] 
                   print "Final de la questio"			
                   self.estat = 2
	        else:
                  fiPars = re.findall(r"^\{(.*)}\\\\$", self.liniaAct.rstrip())
                  if fiPars:
                     self.enunciats.append(fiPars[0])
                     print self.enunciats
                     self.acabaVer()
                  else:
                     enunciat = re.findall(r"\{(.*)\}%$",linia)
                     if(len(enunciat)>0):
                       self.enunciats.append(enunciat[0])
                     else:
                       self.estat = 3


      def llegeixResposta(self): 
          na = self.llegeixCmd("answer")
	  if na:
             p=re.compile("\?(.*)\?")
             answer = p.findall(self.liniaAct)
             if answer:
                print "   ",answer[0]
	        self.lastVersion["respostes"].append(answer[0])
          else:
	     self.questions[self.lastDefId]["versions"].append(self.lastVersion)
             self.estat = 3

      estatsPosibles = {-1: beginDocument,
                         0: introTest,
                         1: llegeixParametresTest,

                         2: llegeixQuestions,
			 3: llegeixVersions,
                         4: llegeixResposta, 

                        10: llegeixVersionsMC,
                        11: llegeixRespostaMC,
                        12: llegeixRespostesOKMC,
 
		        99: endDocument	 
		       }

      def parse(self):
          while not self.eof():
                self.estatsPosibles.get(self.estat, self.initState)(self)
                self.nextLine()

          return(not self.estat<0)


