def autocomplete(data, query):
    completions = {}
    def triedfs(suffix, node):
        if node.children == []:
            if suffix in completions:
                completions[suffix] += 1
            else:
                completions[suffix] = 1
        else:
            for child in node.children:
                triedfs(suffix + child.value, child)
    for page in data:
        current = page.trie.root
        complete = False
        for letter in query:
            if letter == "*":
                complete = True
            exists = False
            for child in current.children:
                if child.value == letter:
                    exists = True
                    current = child
                    break
            if not exists:
                break
        if complete:
            triedfs(query[:-1], current)
        else:
            continue
    ret = []
    for elem in completions:
        if completions[elem] > 1:
            ret.append(elem)
    return ret

def autocorrect(data, query):
    word = query[0]
    corrections = []
    for i in range(1, len(query)):
        search = word + "*"
        possiblewords = autocomplete(data, search)
        for pos in possiblewords:
            if len(query) != len(pos):
                continue
            elif query[i + 1:] == pos[i + 1:]:
                corrections.append(pos)
        word += query[i]
    return corrections