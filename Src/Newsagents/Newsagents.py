class Newsagent:
    def __init__(self):
        self.newsagentId = None
        self.name = None
        self.active = None

    def getNewsagentId(self):
        return self.newsagentId

    def getName(self):
        return self.name

    def setName(self, name):
        self.name = name

    def getActive(self):
        return self.active

    def setActive(self, active):
        self.active = active

    def verify_name(name):
        return isinstance(name, str) and name.strip() != ""

    def create_newsagent(self, newsagentId, name):
        if type(newsagentId) is not int or newsagentId <= 0:
            return False
        if not self.verify_name():
            return False

        self.newsagentId = newsagentId
        self.name = name
        self.active = True
        return True
