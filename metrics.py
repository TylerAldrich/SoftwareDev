import pprint

class Metrics():
    def __init__(self, name):
        self.data = {}
        self.name = name

    def add_value_for_attribute(self, value, attr):
        self.data[attr] = value

    def value_for_attribute(self,attr):
        return self.data[attr]

    def has_attribute(self,attr):
        return self.data.get(attr) != None

class Lookzone(Metrics):
    def __init__(self, name):
        Metrics.__init__(self, name)


class Slidemetrics(Metrics):
    def __init__(self, name):
        Metrics.__init__(self, name)
