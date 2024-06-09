from random import randint
from collections import deque

class LogicException(Exception):
    pass

class Result():
    def __init__(self, page, index, value):
        self.page = page
        self.index = index
        self.value = value

def results(data, query):
    querywords = query.split(" ")
    resultlist = []
    if ("AND" in querywords) or ("OR" in querywords) or ("NOT" in querywords):
        try:
            resultlist = logicsearch(data, querywords)
        except LogicException:
            print("Nepravilno unesen logički izraz!")
    elif query[0] == "\"" and query[-1] == "\"":
        resultlist = phrasesearch(data, query)
    else:
        resultlist = regsearch(data, querywords)
    foundlist = []
    for res in resultlist:
        if res.value != 0:
            res.value += len(res.page.refs)
            for ref in res.page.refs:
                res.value += resultlist[ref].value / 4
            foundlist.append(res)
    return sortresults(foundlist)

def sortresults(resultlist):
    if len(resultlist) == 0 or len(resultlist) == 1:
        return resultlist
    pivot = resultlist[randint(0, len(resultlist) - 1)]
    less = []
    more = []
    equal = []
    for elem in resultlist:
        if pivot.value < elem.value:
            more.append(elem)
        elif pivot.value > elem.value:
            less.append(elem)
        else:
            equal.append(elem)
    sortedless = sortresults(less)
    sortedmore = sortresults(more)
    sorted = sortedmore + equal + sortedless
    return sorted

def regsearch(data, querywords):
    resultlist = []
    for page in data:
        index = {}
        value = 0
        for word in querywords:
            wordresult = page.trie.search(word.lower())
            if wordresult == None:
                continue
            else:
                value += len(wordresult)
                index[word.lower()] = wordresult
        value *= len(index)
        result = Result(page, index, value)
        resultlist.append(result)
    return resultlist

def logicsearch(data, querywords):
    wordgroups = []
    logic = []
    group = []
    if querywords[0] in ["AND", "OR", "NOT"] or querywords[-1] in ["AND", "OR", "NOT"]:
        raise LogicException()
    for word in querywords:
        if word in ["AND", "OR", "NOT"]:
            logic.append(word)
            wordgroups.append(group)
            group = []
        else:
            group.append(word.lower())
    wordgroups.append(group)
    if len(wordgroups) != len(logic) + 1:
        raise LogicException()
    searches = []
    for query in wordgroups:
        searches.append(regsearch(data, query))
    finalresult = searches[0]
    for i in range(len(logic)):
        operator = logic[i]
        operand = searches[i + 1]
        if operator == "AND":
            for j in range(len(operand)):
                final = finalresult[j]
                current = operand[j]
                if final.value != 0 and current.value != 0:
                    final.value += current.value
                    final.index.update(current.index)
                else:
                    final.value = 0
        elif operator == "NOT":
            for j in range(len(operand)):
                final = finalresult[j]
                current = operand[j]
                if current.value != 0:
                    final.value = 0
        else:
            for j in range(len(operand)):
                final = finalresult[j]
                current = operand[j]
                if current.value != 0:
                    final.value += current.value
                    final.index.update(current.index)
    return finalresult

def phrasesearch(data, query):
    phrase = query[1:-1]
    phrasewords = phrase.split(" ")
    unfiltered = regsearch(data, phrasewords)
    resultlist = []
    for result in unfiltered:
        if len(result.index) != len(phrasewords):
            resultlist.append(Result(result.page, [], 0))
        else:
            finalset = set(result.index[phrasewords[0]])
            current = ""
            for word in phrasewords:
                intersect = set()
                for num in result.index[word]:
                    check = num - len(current)
                    intersect.add(check)
                finalset = finalset.intersection(intersect)
                current += word + " "
                if len(finalset) == 0:
                    resultlist.append(Result(result.page, [], 0))
                    break
            if len(finalset) != 0:
                index = {}
                index[phrase] = list(finalset)
                value = len(finalset)
                newresult = Result(result.page, index, value)
                resultlist.append(newresult)
    return resultlist