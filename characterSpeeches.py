import operator

file=open("Hamlet.txt","r+")
speeches=[]
file.seek(0, 2)
EOF = file.tell()
file.seek(0)   
while file.tell() < EOF:
    line = file.readline()
    if line.replace(" ", "").strip().isupper() and line[0:3] != "ACT":
        #print line[0:2]
        character = line.rstrip("\n")
        speech = ""
        line = file.readline()
        while line.replace(" ", "").strip().isupper() == False:
            speech += line.rstrip("\n")
            line = file.readline()
        speechDict = {character: speech}
        speeches.append(speechDict)
for item in speeches:
    print item


        
