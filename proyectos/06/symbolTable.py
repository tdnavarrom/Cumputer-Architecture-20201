class SymbolTable:

    """ reservedWords is a dictionary containing all the varaibles used in the
        Hack assembly language. reservedWords{"Variable":Address} """

    def __init__(self):
        self.reservedWords = {
        "R0": 0,
        "R1": 1,
        "R2": 2,
        "R3": 3,
        "R4": 4,
        "R5": 5,
        "R6": 6,
        "R7": 7,
        "R8": 8,
        "R9": 9,
        "R10": 10,
        "R11": 11,
        "R12": 12,
        "R13": 13,
        "R14": 14,
        "R15": 15,
        "SP": 0,
        "LCL": 1,
        "ARG": 2,
        "THIS": 3,
        "THAT": 4,
        "SCREEN": 16384,
        "KBD": 24576
        }


    def print(self):
        """Print reserved words"""
        print (self.reservedWords)


    def addEntry(self,variable,address):
        """Adds variable to reserved words"""
        self.reservedWords[variable]=address


    def contains(self,variable):
        """Tells whether a variable is in reserved words"""
        if variable in self.reservedWords:  return True


    def getAddress(self,variable):
        """returns address if variable is in reserved words"""
        try:
            x=self.reservedWords[variable]
            return x
        except KeyError:
            return None
