import operator

file=open("Hamlet.txt","r+")
wordcount={}
commonWords = ['the', 'and', 'of', 'to', 'i', 'you', 'a', 'my', 'in', 'it', 'is', 'not', 'his', 'that', 'this', 'but', 'with', 'for', 'your', 'me', 'be', 'as', 'he', 'what', 'him', 'so', 'have', 'will', 'do', 'we', 'no', 'are', 'on', 'o', 'all', 'our', 'by', 'shall', 'if', 'or']
for word in file.read().split():
    word = word.lstrip('\'\"-,.:;!?]')
    word = word.rstrip('\'\"-,.:;!?]')
    word = word.lower()
    if word in commonWords:
        continue
    if word not in wordcount:
        wordcount[word] = 1
    else:
        wordcount[word] += 1
sortedWordCount = sorted(wordcount.items(), key=operator.itemgetter(1))       
for word in sortedWordCount:
    print word