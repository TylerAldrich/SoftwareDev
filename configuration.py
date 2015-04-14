from ipatch_exception import IPatchException

class Configuration():

    def __init__(self, filename, lookzone_attrs, slide_attrs):
        self._lookzone_attrs = lookzone_attrs
        self._slide_attrs = slide_attrs
        self._filename = filename

    @staticmethod
    def read_config_file(filename):
        """This is a class method that reads in an existing Configuration File
        and returns a dictionary containing all attributes"""
        try:
            f = open(filename, 'r')
            seen_lookzone = False
            seen_slide = False
            lookzones = []
            slides = []
            config_dict = {"lookzone" : lookzones, "slide" : slides}
            val = "lookzone"
            for line in f:
                if line == "LOOKZONE:\n":
                    seen_lookzone = True
                    val = "lookzone"
                elif line == "SLIDE:\n":
                    seen_slide = True
                    val = "slide"
                else:
                    config_dict[val].append(line.rstrip('\r\n'))
            f.close()
        except:
            raise IPatchException('Invalid configuration file')

        # Check the file is a valid config file
        if not seen_lookzone or not seen_slide:
            raise IPatchException('Invalid configuration file')

        return config_dict


    def print_config_file(self):
        """ Prints the current configuration file """
        f = open("{}".format(self._filename), 'w')
        self.print_attributes(self._lookzone_attrs,"LOOKZONE:",f)
        self.print_attributes(self._slide_attrs,"SLIDE:",f)
        f.close()


    def print_attributes(self,attrs,heading,file_descriptor):
        """ Writes the given attributes to the given file descriptor """
        file_descriptor.write("{}\n".format(heading))
        for attr in attrs:
            file_descriptor.write("{}\n".format(attr))



