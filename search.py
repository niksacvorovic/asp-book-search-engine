from random import randint

class Result():
    def __init__(self, page, index, value):
        self.page = page
        self.index = index
        self.value = value

def results(data, query):
    resultlist = []
    querywords = query.split(" ")
    for page in data:
        index = {}
        value = 0
        for word in querywords:
            wordresult = page.trie.search(word)
            if wordresult == None:
                continue
            else:
                value += len(wordresult)
                index[word] = wordresult
        value *= len(index)
        result = Result(page, index, value)
        resultlist.append(result)
    foundlist = []
    for res in resultlist:
        if res.value != 0:
            res.value += len(res.page.refs)
            for ref in res.page.refs:
                res.value += resultlist[ref].value / 4
            foundlist.append(res)
    return sortresults(foundlist)

def sortresults(list):
    if len(list) == 0 or len(list) == 1:
        return list
    pivot = list[randint(0, len(list) - 1)]
    less = []
    more = []
    equal = []
    for elem in list:
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
