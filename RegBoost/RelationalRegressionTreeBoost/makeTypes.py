from Utils import Utils
factLines = Utils.readFile("facts.txt")
target = Utils.readFile("examples.txt")[0]
number = target.split('s')[1][:-2]
replaceString = "s"+number
Utils.writeToFile(target.replace(replaceString,"X")[:-1],"types.txt") #get target
seen = []
for line in factLines:
    number = line.rsplit('s',1)[1][:-2]
    replaceString = "s"+number
    typ = line.replace(replaceString,"X")
    if typ not in seen:
        seen.append(typ)
        Utils.writeToFile(typ[:-1],"types.txt")
