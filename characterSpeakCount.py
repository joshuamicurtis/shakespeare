import operator

file=open("Hamlet.txt","r+")
wordcount={}
for word in file.read().split():
    word = word.lstrip('\'\"-,.:;!?]')
    word = word.rstrip('\'\"-,.:;!?]')
    if word.isupper() and len(word) > 3:
        if word not in wordcount:
            wordcount[word] = 1
        else:
            wordcount[word] += 1
sortedWordCount = sorted(wordcount.items(), key=operator.itemgetter(1))       
for word in sortedWordCount:
    print word