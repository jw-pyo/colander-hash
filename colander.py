# author: wjddn1801@snu.ac.kr
# github.com/jw-pyo/colander-hash

import numpy as np
#import matplotlib.pyplot as plt
from collections import OrderedDict
import binascii
from bitstring import BitArray
import inspect

from timer import Timer
from metric import Metric

# unit
bit = 1
B = 8
KB = 1024*B
MB = 1024*KB
GB = 1024*MB

class Colander(object):

    def __init__(self, path):
        self.path = path
        self.chunk_size = None # single chunk size
        self.chunk_list = []
        self.key_length = 5*bit # return length of colander(key of histogram)
        self.histogram = dict() # distribution of colander: the number of colander
        self.set_count = 1 # the count which make chunk list. It affects the speed and accuracy
        self.lower_bound = 0 # no appears in the histogram under this value
    @property
    def bin_count(self):
        return len(self.chunk_list)
    def printParam(self):
        """
        print all parameters of corresponding object.
        """
        print("""
        data path: {}
        chunk size: {}
        total chunk: {}
        """.format(self.path, self.chunk_size, self.bin_count)
        )

    def chopByChunk(self, chunk_size = 32*MB, set_count=1):
        """
        chop the file by chunk and save chunk list in memory(self.chunk_list).
        path: file path
        return: bool
        """
        with Timer(f_name=inspect.stack()[0][3]) as t:
            self.chunk_size = chunk_size
            self.set_count = set_count
            chunk_list = []
            dummy = bytes(('0'*int(chunk_size/set_count)).encode("utf-8"))
            #dummy = str("0"*int(chunk_size/set_count))
            with open(self.path, "rb") as f:
                for i in range(set_count):
                    fstream = dummy*i + f.read()
                    bitarray = BitArray(bytes=fstream).bin
                    self.chunk_list.extend([bitarray[i*chunk_size:(i+1)*chunk_size] for i in range(int(len(fstream)/chunk_size))])
        return True
    def setKeyLength(self, k):
        """
        setter of key_length
        k: new colander size
        """
        self.key_length = k
    def colander(self, i):
        """
        pass single chunk to the colander hash function and return result
        i: the i-th chunk in chunk_list
        return: [0-Z]
        """
        return self.chunk_list[i][:self.key_length]
    def compareChunk(self, i, j):
        pass
    def makeHistogram(self, lower_bound=0):
        """
        make histogram
        """
        with Timer(f_name=inspect.stack()[0][3]) as t:
            self.lower_bound = lower_bound
            for i, chunk in enumerate(self.chunk_list):
                hash_result = self.colander(i)
                if hash_result in self.histogram.keys():
                    self.histogram[hash_result] += 1
                else:
                    self.histogram[hash_result] = 1
            # erase key-value whose value is under lower_bound in histogram
            pop_key_list = []
            for k,v in self.histogram.items():
                if v <= self.lower_bound:
                    pop_key_list.append(k)
            for element in pop_key_list:
                self.histogram.pop(element)

    def normalizeHistogram(self):
        """
        normalize histogram
        """
        bin_count = self.bin_count
        for key in self.histogram.keys():
            self.histogram[key] = float(self.histogram[key])/bin_count

    def printHistogram(self, option):
        """
        print histogram of colander distribution.
        option:
            "count": just print the number of each colander
            "percent": print the percent of each colander compared to entire number
        """
        with Timer(f_name=inspect.stack()[0][3]) as t:
            print("{")
            if option == "count":
                for key, value in self.histogram.items():
                    print("{}: {}".format(key, value))
            elif option == "percent":
                for key in list(self.histogram.keys()):
                    print("{}: {}".format(binascii.hexlify(key).decode(), self.histogram[key]/self.bin_count))
            else:
                for key, value in self.histogram.items():
                    print("{}: {}".format(key, value))
            print("}")
    def compareHistogram(self, other_hist):
        """
        compare the distribution of two histogram.
        """
        with Timer(f_name=inspect.stack()[0][3]) as t:
            for key in list(other_hist.keys()):
                if key not in list(self.histogram.keys()):
                    self.histogram[key] = 0
            for key in list(self.histogram.keys()):
                if key not in list(other_hist.keys()):
                    other_hist[key] = 0
            print(Metric.chi_square(self.histogram, other_hist))
    def plotHistogram(self, low_bound=0):
        """
        plot histogram.
        """
        with Timer(f_name=inspect.stack()[0][3]) as t:
            # the key of self.histogram is sorted in ascending order
            od = OrderedDict(sorted(self.histogram.items()))

            labels = list(od.keys())
            plt.bar(range(len(self.histogram)), self.histogram.values(), color='g', tick_label = labels)
            plt.show()
    def XORTopN(self, n):
        """
        sort the key in descending order and XOR the top n keys.
        n: the number of blocks to be operated XOR
        return: the result of XOR
        """
        with Timer(f_name=inspect.stack()[0][3]) as t:
            od = OrderedDict(sorted(self.histogram.items(), key=lambda kv: kv[1], reverse=True))
            if len(list(od.keys())) == 0:
                raise ValueError("there is no key in histogram")
            ret = list(od.keys())[0]
            for key in list(od.keys())[1:n]:
                ret = Metric.xor(ret, key, bin=True)
        return ret



if __name__ == "__main__":
    data_1 = Colander("/home/jwpyo/colander-hash/sample-data/insurance1.csv")
    data_2 = Colander("/home/jwpyo/colander-hash/sample-data/insurance2.csv")
    data_1.chopByChunk(1*MB, set_count=1)
    data_2.chopByChunk(1*MB, set_count=1)
    data_1.setKeyLength(8)
    data_2.setKeyLength(8)
    data_1.makeHistogram(lower_bound=1*bit)
    data_2.makeHistogram(lower_bound=1*bit)
    #data_1.normalizeHistogram()
    #data_2.normalizeHistogram()
    data_1.printHistogram(option="count")
    data_2.printHistogram(option="count")
    #data_1.plotHistogram()
    #data_2.plotHistogram()
    #data_1.compareHistogram(data_2.histogram)
    print("data1 top10: ", data_1.XORTopN(10))
    print("data2 top10: ", data_2.XORTopN(10))
    #func.printParam()
    #print(func.bin_count)
    #func.plotHistogram()
    #print(b'\x7E'.decode("ascii"))
