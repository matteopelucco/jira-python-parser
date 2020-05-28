#!/usr/bin/python

import logging, os, io, sys, getopt, time, datetime
import urllib.request, json, yaml, re
import xml.etree.ElementTree as ET

# custom helpers
from classes.ConfigHelper import Config as Config
from classes.HtmlHelper import Html as Html

# logger settings
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logging.getLogger('swagger2modsecurity').setLevel(logging.ERROR)

# ready to start
print("===============================================")
print("=== Jira Python Parser                      ===")
print("=== v.1.0.1                                 ===")
print("===============================================")

print("loading config..")
config = Config("config.yaml")
html = Html(config.outputFile)

print("reading input file..")
with open(config.inputFile) as inputFile:
    xmlTree = ET.parse(inputFile)
    xmlRoot = xmlTree.getroot()

print("preparing output file..")
open(config.outputFile, 'w').close()

print("writing document..")
html.printHeader()
for project in config.projects:
    html.printProjectHeader(project)
    for status in config.status:
        # print("project: {}; status: {}".format(project["name"], status["name"]))
        html.printStatusHeader(status)

        for item in xmlRoot.findall('channel/item'):

            itemStatus = item.find("status").text
            itemProjectKey = item.find("project").attrib["key"]
            itemTitle = item.find('title').text

            if itemProjectKey == project["key"] and itemStatus == status["code"]: 
                html.printItem(itemTitle)

        html.printStatusFooter(status)
    html.printProjectFooter(project)
html.printFooter()
print("all done!")
    