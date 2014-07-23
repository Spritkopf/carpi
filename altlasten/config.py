import ConfigParser


cfgFilePath = 'config.ini'

config = ConfigParser.ConfigParser()

def readConfig():
	config.read(cfgFilePath)

def writeConfig():
	cfgfile = open(cfgFilePath,'w')
	config.write(cfgfile)
	cfgfile.close()

def getMediaPath():
	return config.get('General','mediaPath',0)



