from progressbar import *
import time
import subprocess
import sys

def runCommand(command,p):
    child = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE)
    #child = subprocess.Popen(command, shell=True)
    while True:

        out = child.stdout.readline()
        if out == '':
            ret  = child.poll()
	    #print command,'return',ret
            if ret != None:
                p.SetState(ret==0)
                p.update(p.maxval)
                break
        else:
	#time.sleep(0.01)
            val = p.currval + 1
            if val >= p.maxval:
                val = 1
            p.update(val)
	

def cur_file_dir():
    path = sys.path[0]
    if os.path.isdir(path):
        return path
    elif os.path.isfile(path):
        return os.path.dirname(path)

def RunProgress(command,message = "",maxval = 200):
    widgets = ['[Run \033[0;32m%s\033[0m]'%message,' ',Percentage(),' ',Bar(marker='#',left=' ',right=' ') ,' ',AnimatedMarker(),' ',ETA(),' ',ResultShow()]
    p = ProgressBar(widgets=widgets,maxval=maxval).start()
    runCommand(command,p)
    p.finish()
    
class InstallStep(object):
    command = ""
    message = ""
    state = 0
    def __init__(self,command,message="",state=0):
        self.command = command
        self.message = message
        self.state = state
    def GetCommand(self):
        return command
    def IsEnable(self):
        return (self.state!=0)


class InstallStepManager(object):
    def __init__(self):
        """
            installconfig  installglib  installipsutil  installlibvirt  installndb  installrpm  installtftp  remakekenerl
        """
        self.InstallStepList = [InstallStep('installrpm','install rpm packet',1),
                                InstallStep('installipsutil','install psutil moudle'), 
                                InstallStep('installlibvirt','install libvirt moudle'),
                                InstallStep('installglib','install glib moudle'),
                                InstallStep('installndb','install ndb moudle'),
                                InstallStep('remakekenerl','remake system kenerl'),
                                InstallStep('installtftp','install and config tftp server'),
                                InstallStep('installconfig','config install to completed',1),
                                ]
        self.services = ""
    def EnableStep(self,stepName):
        for step in self.InstallStepList:
            if step.command == stepName:
                step.state = 1
    def DisableStep(self,stepName):
        for step in self.InstallStepList:
            if step.command == stepName:
                step.state = 0
    def AddInstallService(self,serviceName):
        self.services+= " "
        self.services+=serviceName
        if serviceName == "storage_server":
            self.EnableStep("installglib")
            self.EnableStep("installndb")
            self.EnableStep("installtftp")
        if serviceName == "node_client":
            self.EnableStep("installipsutil")
            self.EnableStep("installlibvirt")
            self.EnableStep("installglib")
            self.EnableStep("installndb")
            self.EnableStep("remakekenerl")
    def RunInstallScript(self):
        for i in xrange(len(self.InstallStepList)):
            if self.InstallStepList[i].IsEnable():
               cmd = cur_file_dir()
               if cmd[-1] != '/':
                  cmd += '/'
               cmd += self.InstallStepList[i].command
               cmd += self.services
               #print ("cmd====%s"%cmd)
               RunProgress("sh "+cmd,self.InstallStepList[i].message)
                
if __name__ == '__main__':
    print "#############################################"
    print "######Zhicloud service installer Runing######"
    print "#############################################"

    installStepManager = InstallStepManager()
    for service in sys.argv[1:]:
        installStepManager.AddInstallService(service)

    installStepManager.RunInstallScript()

    print "#############################################"
    print "####Zhicloud service installer Completed#####"
    print "#############################################"
