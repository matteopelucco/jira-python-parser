import yaml, urllib, json, logging, sys, os, time
from datetime import datetime, timezone

class Parser:
    
    def __init__(self, config):
        self.config = config

    def sortComments(self, comments):

        cardComments = []
        for elem in comments:
            comment = {}
            comment['id'] = elem.attrib['id']
            comment['created'] = elem.attrib['created']
            comment['author'] = elem.attrib['author']
            comment['text'] = elem.text

            # Mon, 8 Jun 2020 10:10:50 +0200

            now = datetime.now()
            dateObj = datetime.strptime(comment['created'], '%a, %d %b %Y %H:%M:%S %z')
            now = datetime.now(timezone.utc)
            if ((now - dateObj).days > self.config.commentVisibilityDays):
                continue
            if ((now - dateObj).days > self.config.commentIsFreshDays):
                comment["isFresh"] = False
            else:
                comment["isFresh"] = True

            # dateReverse = str(dateObj.year) + "." + str(dateObj.month) + "." + str(dateObj.day)
            dateReverse = dateObj.strftime("%Y.%m.%d %H:%M:%S")
            comment["createdReverse"] = dateReverse

            cardComments.append(comment)
        
        return sorted(cardComments, key=lambda k: k['id'], reverse=True)

    def buildItem(self, item): 

        newItem = {}
        newItem['status'] = item.find("status").text
        newItem['projectKey'] = item.find("project").attrib["key"]
        summary = item.find('title').text
        
        # clean Jira ID on Epics summary, can be tedious. [MYC-1233] myEpic => myEpic
        summary = summary[(summary.find(']') + 1):]
        newItem['summary'] = summary

        newItem['key'] = item.find('key').text
        newItem['link'] = self.config.jira['baseUrl'] + "/browse/" + item.find('key').text
        
        labels = ""
        for label in item.findall('labels/label'):
            labels = labels + " item-" + label.text

        newItem['labels'] = labels

        comments = item.findall('comments/comment')
        comments = self.sortComments(comments)
        newItem['comments'] = comments

        return newItem
        