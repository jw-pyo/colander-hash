# author: wjddn1801@snu.ac.kr
# github.com/jw-pyo/colander-hash
from operator import xor
from bitstring import BitArray, BitStream

class Metric(object):
    def __init__(self):
        pass
    @staticmethod
    def xor(obj1, obj2, **kwargs):
        """
        XOR operation with two same-size byte stream.
        bytes obj1: bytes of size k
        bytes obj2: bytes of size k
        bytes return: obj1 XOR obj2 of size k
        """
        if "bytes" in kwargs:
            b1 = BitArray(bytes=obj1)
            b2 = BitArray(bytes=obj2)
            ret = ''
            for x, y in zip(b1.bin, b2.bin):
                ret += str(ord(x) ^ ord(y))
            return ret
        elif "bin" in kwargs:
            b1 = BitArray(bin=obj1)
            b2 = BitArray(bin=obj2)
            ret = ''
            for x, y in zip(b1.bin, b2.bin):
                ret += str(ord(x) ^ ord(y))
            return ret
        elif "hex" in kwargs:
            b1 = BitArray(hex=obj1)
            b2 = BitArray(hex=obj2)
            ret = ''
            for x, y in zip(b1.bin, b2.bin):
                ret += str(ord(x) ^ ord(y))
            return ret
        else:
            b1 = BitArray(bytes=obj1)
            b2 = BitArray(bytes=obj2)
            ret = ''
            for x, y in zip(b1.bin, b2.bin):
                ret += str(ord(x) ^ ord(y))
            return ret


    @staticmethod
    def chi_square(dict1, dict2):
        """
        chi-square histogram. If it closes to 0, two histogram is more similar.
        dict1: histogram 1
        dict2: histogram 2
        return: chi-square value
        """
        ret = 0
        for x, y in zip(list(dict1.values()), list(dict2.values())):
            if x+y == 0:
                pass
            else:
                ret += float("{0:.3f}".format(float(x-y)**2 / float(x+y)))
        return float("{0:.3f}".format(ret))
