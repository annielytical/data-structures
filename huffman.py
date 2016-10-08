"""
This program uses the bitstream class to compress files using the
Huffman algorithm.

HuffNode: represents nodes used to build the Huffman tree
    __init__: initializes the node
    __str__: prints the node in string form

Huffman: manages reading/writing of the Huffman tree and compressing/
         decompressing of files
    __init__: accepts an input file name and output file name; sets up
              internal attributes for compressing or decompressing
    insert: accepts an ascii code; inserts the node at the proper
            position
    count: counts the frequency of different characters in the input
        file
    buildtree: constructs the code tree using the Huffman algorithm
    putcode: accepts a character number x; puts the code for x into the
             compressed file
    putheader: puts the Huffman header into the compressed file
    getheader: gets header information from the compressed file
               and builds the Huffman tree in node_array
    encode: encodes the file using the Huffman tree and writes
            to the compressed file
    decode: decodes the file using the Huffman tree and writes
            to the decompressed file
"""
from bitstream import Bitstream


class HuffNode:
    """Represent nodes used to build the Huffman tree"""
    def __init__(self):
        """initialize the node"""
        self.lchild = None
        self.rchild = None
        self.parent = None
        self.weight = 0
        self.nextroot = None

    def __str__(self):
        """Print node in string form (for debugging)"""
        return "w:{0},l:{1},r:{2},p:{3},n:{4}".format(self.weight,
                                                      self.lchild,
                                                      self.rchild,
                                                      self.parent,
                                                      self.nextroot)


class Huffman:
    """Manage reading/writing of Huffman tree and
       compressing/decompressing of files
    """

    def __init__(self, infile, outfile):
        """Set up internal attributes for either compressing or
           decompressing
        """
        # Index of final root node
        self.root = None
        # Head of linked list of root nodes
        self.rootlist = None
        # Number of leaves
        self.leaves = 0
        # Huffman tree array
        self.node_array = [HuffNode() for i in range(513)]
        # Open input and output files
        self.infile = infile
        self.bsIn = Bitstream(infile, "r")
        self.bsOut = Bitstream(outfile, "w")

    def insert(self, i):
        """Given an ascii code i, insert its node at the proper
           position (assuming ascending order)
        """
        if self.rootlist is None:
            self.rootlist = i
        elif self.node_array[self.rootlist].weight >= self.node_array[
                i].weight:
            temp = self.rootlist
            self.rootlist = i
            self.node_array[self.rootlist].nextroot = temp
        else:
            x = self.node_array[self.rootlist]
            while True:
                if x.nextroot is None:
                    self.root = i
                    x.nextroot = i
                    break
                elif self.node_array[x.nextroot].weight >= self.node_array[
                        i].weight:
                    temp = x.nextroot
                    x.nextroot = i
                    self.node_array[x.nextroot].nextroot = temp
                    break
                else:
                    x = self.node_array[x.nextroot]

    def count(self):
        """Count the frequency of characters in the input file"""
        fileIn = open(self.infile, "rb")
        self.node_array[256].weight += 1  # eof character
        while True:
            try:
                b = fileIn.read(1)
                self.node_array[int(b[0])].weight += 1
            except:
                break
        fileIn.close()

    def buildtree(self):
        """Construct code tree using the Huffman algorithm"""
        for i in range(513):
            if self.node_array[i].weight != 0:
                self.insert(i)
        i = 257
        while self.rootlist is not None and self.node_array[
                self.rootlist].nextroot is not None:
            u = self.rootlist
            v = self.node_array[self.rootlist].nextroot
            w = self.node_array[self.rootlist].weight + self.node_array[
                self.node_array[self.rootlist].nextroot].weight
            self.node_array[i].weight = w
            self.node_array[i].lchild = self.rootlist
            self.node_array[i].rchild = self.node_array[
                self.rootlist].nextroot
            self.node_array[u].parent = i
            self.node_array[v].parent = i
            self.rootlist = self.node_array[self.node_array[self.rootlist]
                                            .nextroot].nextroot
            self.insert(i)
            i += 1
        if self.node_array[self.rootlist].nextroot is None:
            self.root = self.rootlist

    def putcode(self, x):
        """Put code for character x into compressed file"""
        code = []
        while self.node_array[x].parent is not None:
            y = self.node_array[x].parent
            if self.node_array[y].lchild == x:
                code.append(0)
            if self.node_array[y].rchild == x:
                code.append(1)
            x = y
        code.reverse()
        for i in code:
            self.bsOut.putbit(i)

    def putheader(self):
        """Put Huffman tree into compressed file"""
        x = 257
        self.bsOut.putint(self.root, 10)
        while x <= self.root:
            self.bsOut.putint(self.node_array[x].lchild, 9)
            self.bsOut.putint(self.node_array[x].rchild, 9)
            x += 1

    def getheader(self):
        """Get header information from huffman compressed file and
           construct Huffman tree in node_array
        """
        x = 257
        self.root = self.bsIn.getint(10)
        while x <= self.root:
            self.node_array[x].lchild = self.bsIn.getint(9)
            self.node_array[x].rchild = self.bsIn.getint(9)
            x += 1

    def encode(self):
        """Encode the file using the Huffman tree and write it to the
           compressed file
        """
        while True:
            try:
                c = self.bsIn.getint(8)
                self.putcode(c)
            except:
                break
        self.putcode(256)
        self.bsOut.close()

    def decode(self):
        """Decode the file using the reconstructed Huffman tree and
           write it to the decompressed file
        """
        x = self.root
        while True:
            while x > 256:
                y = self.bsIn.getbit()
                if y == 0:
                    x = self.node_array[x].lchild
                if y == 1:
                    x = self.node_array[x].rchild
            self.bsOut.putint(x, 8)
            if x == 256:
                break
            x = self.root
        self.bsOut.close()
