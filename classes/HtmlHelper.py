import re

class Html:
    def __init__(self, file):
        self.file = file

        # empty file
        open(file, 'w').close()

        # templating
        self.tplHeader = self.loadTemplate('tpls/header.txt')
        self.tplFooter = self.loadTemplate('tpls/footer.txt')
        self.tplProjectHeader = self.loadTemplate('tpls/projectHeader.txt')
        self.tplProjectFooter = self.loadTemplate('tpls/projectFooter.txt')
        self.tplStatusHeader = self.loadTemplate('tpls/statusHeader.txt')
        self.tplStatusFooter = self.loadTemplate('tpls/statusFooter.txt')
        self.tplItemHeader = self.loadTemplate('tpls/itemHeader.txt')   
        self.tplItemFooter = self.loadTemplate('tpls/itemFooter.txt')   
        self.tplComment = self.loadTemplate('tpls/comment.txt')  
        self.tplNoComment = self.loadTemplate('tpls/noComment.txt')       

    def loadTemplate(self, tplName):
        with open(tplName, 'r') as file:
            return file.read()

    def write(self, *args, **kwargs):
        with open(self.file, 'a') as file:
            print(*args, **kwargs, file=file)

    def printHeader(self):
        with open(self.file, 'a') as file:
            self.write(self.tplHeader)

    def printFooter(self):
        with open(self.file, 'a') as file:
            self.write(self.tplFooter)


    def printProjectHeader(self, project):
        with open(self.file, 'a') as file:
            self.write(self.tplProjectHeader.format(projectName = project["name"]))
    
    def printProjectFooter(self):
        with open(self.file, 'a') as file:
            self.write(self.tplProjectFooter)

    def printStatusHeader(self, status):
        with open(self.file, 'a') as file:
            self.write(self.tplStatusHeader.format(statusName = status["name"]))

    def printStatusFooter(self):
        with open(self.file, 'a') as file:
            self.write(self.tplStatusFooter)

    def printItemHeader(self, item):
        with open(self.file, 'a') as file:
            self.write(self.tplItemHeader.format(itemSummary = item['summary'], itemLabels = item['labels'], itemLink = item['link'], itemKey = item['key']))

    def printItemFooter(self):
        with open(self.file, 'a') as file:
            self.write(self.tplItemFooter)

    def printComment(self, comment):
        commentClass = ""
        if comment["isFresh"] == True: 
            commentClass = "current"
        with open(self.file, 'a') as file:
            self.write(self.tplComment.format(commentDate = comment['createdReverse'], commentAuthor = comment['author'], commentText = comment['text'], commentClass = commentClass))

    def printNoComment(self):
        with open(self.file, 'a') as file:
            self.write(self.tplNoComment)


    

