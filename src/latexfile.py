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
          #strRE = r
          return re.search(strRE, self.liniaAct.rstrip()) 

      def llegeixCmdInt(self,cmd):
          strRE = r"^\\%(cmd)s$" % {"cmd": cmd}
          return re.findall(strRE, self.liniaAct.rstrip())

      def llegeixDef(self, nomDef):
          strRE = r"^\\def\\%(nom)s((#[0-9])+|)?{(.+)}$" % {"nom": nomDef}
          return re.search(strRE, self.liniaAct.rstrip())

      def eof(self):
          return (not self.liniaAct)     
   
      def nextLine(self):
          self.liniaAct = self.readline()
 
