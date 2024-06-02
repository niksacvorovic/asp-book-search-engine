class TrieNode():
    def __init__(self, value):
        self.value = value
        self.children = []
        self.index = []

class Trie():
    def __init__(self):
        self.root = TrieNode(None)

    def add(self, string, ordinal):
        current = self.root
        for char in string:
            exists = False
            for child in current.children:
                if child.value == char:
                    exists = True
                    current = child
                    break
            if exists:
                continue
            else:
                newnode = TrieNode(char)
                current.children.append(newnode)
                current = newnode
        current.index.append(ordinal)

    def search(self, string):
        current = self.root
        for char in string:
            exists = False
            for child in current.children:
                if child.value == char:
                    exists = True
                    current = child
                    break
            if exists:
                continue
            else:
                return None
        return current.index