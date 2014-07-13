#!/usr/bin/python

SHORT_ANSWER = 0
MULTIPLE_CHOICE = 1

class questio():
      def __init__(self, nom, enunciat):
          self.nom = nom
          self.enunciat = enunciat
          self.respostes = []
          self.type = SHORT_ANSWER 
      
      def setType(self, type):
          self.type = type
  
      def afegeixResposta(self, bona, pes, resposta):
          rsp = {"bona": bona,
                 "resp": resposta,
                 "pes": pes }

          self.respostes.append(rsp)

      def clearRespostes(self):
          self.respostes = []
         
      def __str__(self):
          retval = "::%(nom)s::[html]%(enunciat)s {\n" % {"nom": self.nom, "enunciat": self.enunciat}
          for res in self.respostes:
              sym = '~'
              pes = ''
              if(res["bona"]):
                sym = '=' 

              if(res["pes"]>0):
                 pes = "%%%(p)d%%" % {"p": res["pes"]}

              respStr = res["resp"].replace("{","\{")
              respStr = respStr.replace("}","\}")
              respStr = respStr.replace("=","\=")
              respStr = respStr.replace("#","\#")
              respStr = respStr.replace(":","\:")
              respStr = respStr.replace("~","\~")

              retval+="\t%(sym)s%(pes)s%(res)s\n" % {"sym": sym, "pes": pes, "res": respStr}
          retval+="}\n"

          return(retval)

class giftFile(file):
      def __init__(self, nomFitxer):
          file.__init__(self, nomFitxer, "w")
          self.catName = ''
          self.actVariant = []
          self.enunciatGen = ''
 
      def setCategory(self,catName):
          self.catName = catName
          self.write("$CATEGORY: "+catName+"\n\n")
     
      def prepareEnunciat(self):
          i=1
          enunciatVer = self.enunciatGen.replace("$","$$")

          if (self.tipusEnunciat == "short answer"):
             for e in self.actVariant:
                 enunciatVer = enunciatVer.replace("#%(ne)s" % {"ne": i}, e)
                 i=i+1 

          enunciatVer = enunciatVer.replace("{","\{")
          enunciatVer = enunciatVer.replace("}","\}")
          return(enunciatVer)

      def writeQuestions(self, tf):
          self.setCategory(tf.paramTest["title"])

          for idQuestio, dades in tf.questions.iteritems():
              self.enunciatGen = dades['enunciat']
              self.tipusEnunciat = dades['tipus']
              self.setCategory(tf.paramTest["title"]+"/"+idQuestio)
              j=1
              print "\n*** Generant %(nv)d versions de la questio %(idq)s" % {"nv": len(dades['versions']), "idq": idQuestio}
              for ver in dades['versions']:

                  if (self.tipusEnunciat == "short answer"):
                     self.actVariant = ver['enunciat']

                  enunciatVer = self.prepareEnunciat()
                  
                  print "v.%(v)d " % {"v": j},

                  if len(ver['respostes'])>0: 
                     novaQuestio = questio("%(nq)s-%(numq)02d" % {"nq": idQuestio, "numq": j}, enunciatVer)

                     answerStatus = True
                     nAns = 1
                     for answer in ver['respostes']:
                         if (self.tipusEnunciat == "multiple choice as short answer"):
                            answerStatus = (nAns in ver['respCorrectes'])

                         novaQuestio.afegeixResposta(answerStatus, 0, answer)
                         nAns = nAns + 1

                     questioStr = "%(nq)s\n" % {"nq": novaQuestio }
                     self.write(questioStr)
                  else:
                     print "\t(No hi ha respostes d'aquesta versio!)" 
                  j=j+1
