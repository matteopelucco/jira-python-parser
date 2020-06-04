import yaml, urllib, json, logging, sys, os

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
            cardComments.append(comment)
        
        return sorted(cardComments, key=lambda k: k['id'], reverse=True)

    def buildItem(self, item): 

        newItem = {}
        newItem['status'] = item.find("status").text
        newItem['projectKey'] = item.find("project").attrib["key"]
        newItem['summary'] = item.find('title').text
        newItem['key'] = item.find('key').text
        newItem['link'] = self.config.jiraBaseUrl + "/browse/" + item.find('key').text
        
        labels = ""
        for label in item.findall('labels/label'):
            labels = labels + " item-" + label.text

        newItem['labels'] = labels

        comments = item.findall('comments/comment')
        comments = self.sortComments(comments)
        newItem['comments'] = comments

        return newItem
        