"""SpellCheck Class

Stores wordlist.txt in a binary search tree, checks if a word is valid by
searching the BST, and generates suggestions if the word is invalid

Dependencies:
    wordlist.txt in the working directory
    pythonds module

Methods:
    __init__: creates the BST
    check: checks the BST for a word
    correct: creates similar words by swapping, inserting, and deleting letters
"""

from pythonds.trees.bst import BinarySearchTree


class SpellCheck:
    """houses the BST and methods to check spelling/generate suggestions"""

    letters = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L',
               'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X',
               'Y', 'Z', 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j',
               'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v',
               'w', 'x', 'y', 'z']

    def __init__(self):
        """creates the BST"""
        self.tree = BinarySearchTree()
        file = open("wordlist.txt", "r")
        x = file.readline()

        while x != '':
                x = x.replace('\n', '')
                self.tree.put(x, x)
                x = file.readline()

        file.close()

    def check(self, xx):
        """checks the BST for a word"""
        return self.tree.__contains__(xx)

    def correct(self, xx):
        """develops similar words"""
        if self.check(xx):
            return xx

        corrections = []
        x = list(xx)

        for i, val in enumerate(x):
            x = list(xx)
            x.remove(val)

            if self.check(''.join(x)):
                corrections.append(''.join(x))

            for j in SpellCheck.letters:
                x = list(xx)
                x.insert(i, j)

                if self.check(''.join(x)):
                    corrections.append(''.join(x))

                x = list(xx)
                x[i] = j

                if self.check(''.join(x)):
                    corrections.append(''.join(x))

            if i != len(x) - 1:
                x = list(xx)
                temp = x[i]
                x[i] = x[i + 1]
                x[i + 1] = temp

                if self.check(''.join(x)):
                    corrections.append(''.join(x))
            else:
                for j in SpellCheck.letters:
                    x = list(xx)
                    x.append(j)

                    if self.check(''.join(x)):
                        corrections.append(''.join(x))

        return corrections
