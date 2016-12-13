file=open("Hamlet.txt","r+")
wordCount = 0
for word in file.read().split():
    wordCount = wordCount + 1;
    if word.isupper() == True and len(word) > 2:
        print word
print wordCount