# Holds the name and active status of a newsagent.
class Newsagent:
    def __init__(self):
        self.newsagentId = None
        self.name = None
        self.active = None

    # Basic getters and setters.
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

    # Reject blank or spaces-only names.
    def verify_name(self, name):
        return isinstance(name, str) and name.strip() != ""

    # Create a record only when the ID and name are valid.
    def create_newsagent(self, newsagentId, name):
        if type(newsagentId) is not int or newsagentId <= 0:
            return False
        if not self.verify_name(name):
            return False

        self.newsagentId = newsagentId
        self.name = name
        self.active = True
        return True


# Manages multiple newsagents using the CRUD pattern
class NewsagentManager:
    def __init__(self):
        self.newsagents = {}

    def create_newsagent(self, newsagentId, name):
        if newsagentId in self.newsagents:
            return False

        newsagent = Newsagent()
        if not newsagent.create_newsagent(newsagentId, name):
            return False

        self.newsagents[newsagentId] = newsagent
        return newsagentId

    def read_newsagent(self, newsagentId):
        return self.newsagents.get(newsagentId)

    def read_all_newsagents(self):
        return dict(self.newsagents)

    def update_newsagent(self, newsagentId, name):
        newsagent = self.read_newsagent(newsagentId)
        if newsagent is None or not newsagent.verify_name(name):
            return False

        newsagent.setName(name)
        return True

    def delete_newsagent(self, newsagentId):
        # An inactive record is kept
        newsagent = self.read_newsagent(newsagentId)
        if newsagent is None or newsagent.getActive() is False:
            return False

        newsagent.setActive(False)
        return True
