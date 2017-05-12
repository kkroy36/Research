class Utils(object):
    '''utilities class'''
    @staticmethod
    def readFile(fileName):
        '''reads file and returns file lines'''
        with open(fileName) as file:
            fileLines = file.read().splitlines()
        return fileLines
