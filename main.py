import math
import re
from stop_list import closed_class_stop_words

def cleanText(text, stopWords):
    text = text.lower()
    text = re.sub(r'[^\w\s]', "", text)
    text = re.sub(r'\d+', "", text)
    tokens = text.split()
    filtered = [token for token in tokens if token not in stopWords]
    return filtered

def getIDF(*documents):
    length = len(documents)
    freq = {}

    for doc in documents:
        uniqueWords = set(doc)
        for word in uniqueWords:
            freq[word] = freq.get(word, 0) + 1
    
    idf = {}
    for word in freq:
        idf[word] = math.log(length / freq[word])

    return idf

def getTFID(documents, idf):
    vectors = []
    
    for document in documents:
        tfidVector = {}
        countOfWords = len(document)
        freq = {word: document.count(word) / countOfWords for word in document}

        for word, frequency in freq.items():
            if word in idf:
                tfidVector[word] = frequency * idf[word]
        
        vectors.append(tfidVector)
    return vectors

def cosineSimilarity(vec1, vec2):
    dotPro = sum(vec1[word] * vec2[word] for word in vec1 if word in vec2)
    mag1 = math.sqrt(sum(value**2 for value in vec1.values()))
    mag2 = math.sqrt(sum(value**2 for value in vec2.values()))

    if mag1 == 0 or mag2 == 0:
        return 0
    
    return dotPro / (mag1 * mag2)

def orderQ(querys, abstracts, stopWords):
    res = []
    
    filteredQ = list(querys.values())
    filteredA = list(abstracts.values())  

    idf = getIDF(*filteredQ, *filteredA)
    
    qVectors = getTFID(filteredQ, idf)
    aVectors = getTFID(filteredA, idf)

    for queryIndex, qVector in enumerate(qVectors, start=1):
        similarityScores = []
        
        for abstractIndex, aVector in enumerate(aVectors, start=1):
            similarity = cosineSimilarity(qVector, aVector)
            similarityScores.append((abstractIndex, similarity))

        similarityScores.sort(key=lambda x: x[1], reverse=True)
        
        for abstractIndex, similarity in similarityScores:
            res.append(f"{queryIndex} {abstractIndex} {similarity:.6f}")

    return res

def writeFile(output, name):
    with open(name, 'w') as file:
        for line in output:
            file.write(line + '\n')

def readAbstracts(file_path, stopWords):
    abstracts = {}
    with open(file_path, 'r') as f:
        abstract_id = None
        abstract_text = ''
        for line in f:
            if line.startswith('.I'):
                if abstract_id is not None:
                    abstracts[abstract_id] = cleanText(abstract_text, stopWords)
                abstract_id = int(line.strip().split()[1])
                abstract_text = ''
            elif line.startswith('.W'):
                continue
            else:
                abstract_text += line.strip() + ' '
        if abstract_id is not None:
            abstracts[abstract_id] = cleanText(abstract_text, stopWords)
    return abstracts

def readQueries(filePath, stopWords):
    queries = {}
    with open(filePath, 'r') as f:
        query_id = None
        query_text = ''
        for line in f:
            if line.startswith('.I'):
                if query_id is not None:
                    queries[query_id] = cleanText(query_text, stopWords)
                query_id = int(line.strip().split()[1])
                query_text = ''
            elif line.startswith('.W'):
                continue
            else:
                query_text += line.strip() + ' '
        if query_id is not None:
            queries[query_id] = cleanText(query_text, stopWords)
    return queries

stopWords = closed_class_stop_words
q = readQueries('cran.qry', stopWords)
a = readAbstracts('cran.all.1400', stopWords)
ordered = orderQ(q, a, stopWords)
writeFile(ordered, 'output.txt')
