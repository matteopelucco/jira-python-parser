#!/usr/bin/python

import logging, os, io, sys, getopt, time, datetime
import urllib.request, json, yaml, re
import xml.etree.ElementTree as ET

# custom helpers
from classes.ConfigHelper import Config as Config
from classes.HtmlHelper import Html as Html
from classes.ParserHelper import Parser as Parser

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
parser = Parser(config)

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

            item = parser.buildItem(item)

            if item['projectKey'] == project['key'] and item['status'] == status['code']: 
                html.printItemHeader(item)

                comments = item['comments']

                if comments is None: 
                    html.printNoComment()
                else:
                    for comment in comments:
                        html.printComment(comment)

                html.printItemFooter()

        html.printStatusFooter()
    html.printProjectFooter()
html.printFooter()
print("all done!")
    