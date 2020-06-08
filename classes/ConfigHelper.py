import yaml, urllib, json, logging, sys, os, ssl
import xml.etree.ElementTree as ET

class Config:

    def __init__(self, file):
        self.file = file

        with open(self.file, 'r') as stream:
            try:
                configFile = yaml.load(stream)
                self.commentVisibilityDays = configFile['commentVisibilityDays']
                self.commentIsFreshDays = configFile['commentIsFreshDays']
                self.inputFile = configFile['inputFile']
                self.outputFile = configFile['outputFile']
                self.projects = configFile['projects']
                self.status = configFile['status']
                self.jira = configFile['jira']
            except yaml.YAMLError as exc:
                print(exc)
    
    def readInputFile(self):
        url = self.inputFile
        if url.startswith("https") and "//" in url:
            print('Remote downloading input file..')
            try:

                if (not os.environ.get('PYTHONHTTPSVERIFY', '') and getattr(ssl, '_create_unverified_context', None)):
                    ssl._create_default_https_context = ssl._create_unverified_context

                remoteFile = urllib.request.urlopen(url)
                print("Input file downloaded with success. Now parsing input file..")
                xmlTree = ET.parse(remoteFile)
                print("Input file succesfully parsed.")
                return xmlTree.getroot()
            except Exception as e:
                logging.error("Error retrieving file {0}".format(url))
                logging.error("                      {0}".format(str(e)))
                sys.exit(1)
        else: 
            with open(self.inputFile) as inputFile:
                print('Parsing a local input file..')
                xmlTree = ET.parse(inputFile)
                print("Input file succesfully parsed.")
                return xmlTree.getroot()