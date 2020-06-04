import yaml, urllib, json, logging, sys, os

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
                self.jiraBaseUrl = configFile['jiraBaseUrl']
            except yaml.YAMLError as exc:
                print(exc)