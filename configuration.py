class Configuration():

    def __init__(self, filename, lookzone_attrs, slide_attrs):
        self._lookzone_attrs = lookzone_attrs
        self._slide_attrs = slide_attrs
        self._filename = filename

    @classmethod
    def read_config_file(cls,filename):
        """This is a class method that reads in an existing Configuration File
        and returns a dictionary containing all attributes"""
        f = open(filename, 'r')
        lookzones = []    
        slides = []
        config_dict = {"lookzone" : lookzones, "slide" : slides}
        val = "lookzone"
        for line in f:
            if line == "LOOKZONE:\n":
                val = "lookzone"
            elif line == "SLIDE:\n":
                val = "slide"
            else: 
                config_dict[val].append(line.rstrip('\r\n'))
        f.close()
        return config_dict


    def print_config_file(self):
        """ Prints the current configuration file """
        f = open("{}.ipatch".format(self._filename), 'w')
        self.print_attributes(self._lookzone_attrs,"LOOKZONE:",f)
        self.print_attributes(self._slide_attrs,"SLIDE:",f)
        f.close()
        


    def print_attributes(self,attrs,heading,file_descriptor):
        """ Writes the given attributes to the given file descriptor """
        file_descriptor.write("{}\n".format(heading))
        for attr in attrs:
            file_descriptor.write("{}\n".format(attr))



