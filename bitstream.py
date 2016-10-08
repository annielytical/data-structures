"""
This is a bitstream class for bit manipulation.

Methods:
    __init__: initializes the bistream object; accepts a filename and
             read/write specification; opens the file
    __str__: returns the current byte buffer
    __len__: returns the number of bytes in the bitstream
    flush: zeroes out remaining bits and writes byte buffer to the file
    putbit: accepts a bit c; writes c to the file
    getbit: reads the next bit from a file
    putint: accepts an integer (n) and number of bits (numbits); writes
            n to the file using numbits bits
    getint: accepts number of bits (numbits); gets numbits bits from
        the file and returns the corresponding integer (or None)
    close: flushes the last byte (if needed) and closes the file
"""


class Bitstream:

    def __init__(self, filename, rw):
        """Create a bitstream object, read from/write to filename"""
        if rw == "r":
            self.filename = open(filename, 'rb')
            self.rw = 'r'
        elif rw == "w":
            self.filename = open(filename, 'wb')
            self.rw = 'w'
        self.bytebuffer = bytearray(1)
        self.bitpos = 0
        self.size = 0

    def __str__(self):
        """return current byte buffer (for printing), 8 bits, most
           significant to least significant
        """
        bit = ''
        for i in range(7, -1, -1):
            x = (self.bytebuffer[0] & 1 << i) >> i
            bit += str(x)
        return bit

    def __len__(self):
        """return the number of bytes in the bitstream"""
        return self.size

    def flush(self):
        """zero out remaining bits, write byte buffer to file"""
        self.bytebuffer[0] = (self.bytebuffer[0] <<
                              self.bitpos) >> self.bitpos
        self.filename.write(self.bytebuffer)

    def putbit(self, c):
        """write bit c to file (for writing)"""
        if c == 1:
            self.bytebuffer[0] = self.bytebuffer[0] | (1 << self.bitpos)
        elif c == 0:
            self.bytebuffer[0] = self.bytebuffer[0] & ~(1 << self.bitpos)
        self.bitpos += 1
        if self.bitpos > 7:
            self.filename.write(self.bytebuffer)
            self.bitpos = 0

    def getbit(self):
        """return next bit from file (for reading)"""
        if self.bitpos == 0:
            char = self.filename.read(1)
            if len(char) == 0:
                return None
            self.bytebuffer[0] = ord(char)
        b = (self.bytebuffer[0] & (1 << self.bitpos)) >> self.bitpos
        self.bitpos += 1
        if self.bitpos > 7:
            self.bitpos = 0
        return b

    def putint(self, n, numbits):
        """write integer n into file using numbits bits"""
        for i in range(numbits):
            bit = (n & (1 << i)) >> i
            self.putbit(bit)
        self.size += 1

    def getint(self, numbits):
        """get numbits bits from the file; return the corresponding
           integer; return None if at end of file
        """
        n = 0
        for i in range(numbits):
            b = self.getbit()
            if b is None:
                return None
            n += b * 2 ** i
        self.size += 1
        return n

    def close(self):
        """flush last byte if necessary and close the file"""
        if self.rw == 'w' and self.bitpos != 0:
            self.flush()
        self.filename.close()
