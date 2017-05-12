class Utils(object):
    '''Utilities class'''
    @staticmethod
    def readFile(fileName):
        '''method to read a file and return file lines'''
        with open(fileName) as file:
            lines = file.read().splitlines()
        return [line for line in lines if "//" not in line]

    @staticmethod
    def writeFile(fileName,lines):
        '''method to write the string to the file'''
        with open(fileName,"a") as file:
            for line in lines:
                file.write(line+"\n")

    @staticmethod
    def normalize(keyValue):
        '''normalizes a dictionary of values'''
        if sum(keyValue.values()) == 0:
            total = sum([(value+0.000001) for value in keyValue.values()])
        else:
            total = sum(keyValue.values())
        for key in keyValue:
            keyValue[key] = keyValue[key]/float(total)
        return keyValue

    @staticmethod
    def difference(list1,list2):
        '''returns elements in list1 and not in list2'''
        return [item for item in list1 if item not in list2]

    @staticmethod
    def contains(line,list1):   
        '''returns true if line contains any element in the list'''
        for item in list1:
            if item in line:
                return True
        return False

    @staticmethod
    def printList(list1):
        '''prints a list of elements'''
        for item in list1:
            print item
    
        
