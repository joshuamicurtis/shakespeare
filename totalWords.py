file=open("Hamlet.txt","r+")
wordCount = 0
for word in file.read().split():
    wordCount = wordCount + 1;
print wordCount