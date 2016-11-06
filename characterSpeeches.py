import operator

file=open("Hamlet.txt","r+")
speeches=[]
speech = ""
character = ""

for line in file:
    if line.isupper() and line[0:3] != "ACT":
        speechDict = {character: speech}
        speeches.append(speechDict)
        character = line.rstrip("\n")
        speech = ""
    if line.isupper() == False:
        speech += " " + line.rstrip("\n")
speechDict = {character: speech}
speeches.append(speechDict)
for item in speeches:
    print item


        
