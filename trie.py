from collections import defaultdict


class TrieNode():

    def __init__(self):
        self.children = defaultdict()
        self.documents = []
        self.terminating = False


class Trie():

    def __init__(self):
        self.root = self.get_node()

    def get_node(self):
        return TrieNode()

    def get_index(self, ch):
        return ord(ch) - ord('a')

    def insert(self, word, links):

        root = self.root
        len1 = len(word)

        for i in range(len1):
            index = self.get_index(word[i])

            if index not in root.children:
                root.children[index] = self.get_node()
            root = root.children.get(index)

        for path in links:
            if path not in root.documents:
                root.documents.append(path)

        root.terminating = True

    def search(self, word):
        root = self.root
        len1 = len(word)

        for i in range(len1):
            index = self.get_index(word[i])
            if not root:
                return []
            root = root.children.get(index)

        return root.documents if root and root.terminating else []