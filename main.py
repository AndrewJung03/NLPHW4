import math
import re

def removeStopWords(text: str, stopWords: list) -> list:
    text = re.sub(r'[^\w\s]','', text)
    text = re.sub(r'\d+','', text)
    wordsInText = text.lower().split()
    for word1 in stopWords:
        if word1 in wordsInText:
            wordsInText.remove(word1)
            
    return wordsInText

def getIDF(wordLists: list) -> dict:
    numberOfWordLists = len(wordLists)
    freq = {}
    for wordList in wordLists:
        uniqueWordSet = set(wordList)
        for word in uniqueWordSet:
            if word in freq:
                freq[word] += 1
            else:
                freq[word] = 1

    idf = {}
    for word, df in freq.items():
        if df> 0:
            idf[word] = math.log(numberOfWordLists/df)
    return idf



list1 = removeStopWords("Hello this is Andrew and I love to play minecraft 2.0!", ["this"])
list2 = removeStopWords("This is the second LIST!", ["this"])
list3 = list1, list2
print(list3)
print(getIDF(list3))

