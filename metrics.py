import pprint

class Metrics():
    def __init__(self, name):
        """
        Metrics serves as a parent to both Lookzone and Slidemetrics,
        and is used to store attribute data for input workbooks.

        Lookzone and Slidemetrics add no functionality but are named
        to make their purpose more clear in the WorkbookReader class.
        """
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
