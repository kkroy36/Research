from math import exp
class Utils(object):
    '''Utilities class'''
    @staticmethod
    def sigmoid(number):
        '''returns the sigmoid of a number'''
        return exp(number)/float(1+exp(number))
    
    @staticmethod
    def readFile(fileName):
        '''reads files and returns filelines'''
        with open(fileName) as file:
            fileLines = file.read().splitlines()
        return fileLines
    
    @staticmethod
    def writeToFile(string,fileName):
        '''writes the string to the file'''
        with open(fileName,"a") as file:
            file.write(string+"\n")
        
    @staticmethod
    def difference(l1,l2):
        '''returns all elements of list1 not in lis2'''
        return [item for item in l1 if item not in l2]

    @staticmethod
    def getArity(predicate):
        '''returns arity of the predicate'''
        if ',' in predicate:
            return 2
        else:
            return 1
