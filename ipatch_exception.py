# This class simply acts as a wrapper for exceptions thrown 
# from the Workbook Readers and Writers so the front end
# application can properly identify and react to errors
class IPatchException(Exception):
    pass
