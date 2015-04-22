# This class simply acts as a wrapper for exceptions thrown 
# from the Workbook Readers and Writers so the front end
# application can properly identify and react to errors
""" Custom Wrapper by iPatch errors thrown from Back-End """
class IPatchException(Exception):
    pass
