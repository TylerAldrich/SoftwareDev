import pprint

class Lookzone():
    def __init__(self, name):
        self.data = {}
        self.name = name

    def add_value_for_attribute(self, value, attr):
        self.data[attr] = value

    def value_for_attribute(self,attr):
        return self.data[attr]

    def has_attribute(self,attr):
        return self.data.get(attr) != None
