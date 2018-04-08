# author: wjddn1801@snu.ac.kr
# github.com/jw-pyo/colander-hash

import numpy as np
import matplotlib.pyplot as plt
import collections

# unit
B = 1
KB = 1024
MB = 1024*1024
GB = 1024*1024*1024

class Colander(object):

    def __init__(self, path):
        self.path = path
        self.chunk_size = None # single chunk size
        self.chunk_list = []
        self.colander_size = 1 # return length of colander
        self.histogram = dict() # distribution of colander: the number of colander
        self.set_count = 1 # the count which make chunk list. It affects the speed and accuracy
    def printParam(self):
        """
        print all parameters of corresponding object.
        """
        print("""
        data path: {}
        chunk size: {}
        total chunk: {}
        """.format(self.path, self.chunk_size, len(self.chunk_list))
        )

    def chopByChunk(self, chunk_size = 32*MB, set_count=1):
        """
        chop the file by chunk and save chunk list in memory(self.chunk_list).
        path: file path
        return: bool
        """
        self.chunk_size = chunk_size
        self.set_count = set_count
        chunk_list = []
        dummy = bytes(('0'*int(chunk_size/set_count)).encode("utf-8"))
        for i in range(set_count):
            with open(self.path, "rb") as f:
                fstream = dummy*i + f.read()
                chunk_list = [fstream[i*chunk_size:(i+1)*chunk_size] for i in range(int(len(fstream)/chunk_size))]
            self.chunk_list.extend(chunk_list)
        return True
    def setColanderSize(self, k):
        """
        setter of colander_size
        k: new colander size
        """
        self.colander_size = k
    def colander(self, i):
        """
        pass single chunk to the colander hash function and return result.
        i: the i-th chunk in chunk_list
        return: [0-Z]
        """
        return self.chunk_list[i][:self.colander_size]
    def compareChunk(self, i, j):
        pass
    def makeHistogram(self):
        """
        make histogram
        """
        #TODO: add option to make only noticable result(only make dicts higher than certain value)
        for i, chunk in enumerate(self.chunk_list):
            hash_result = self.colander(i)
            if hash_result in self.histogram.keys():
                self.histogram[hash_result] += 1
            else:
                self.histogram[hash_result] = 1
    def printHistogram(self, option):
        """
        print histogram of colander distribution.
        option: 
            "count": just print the number of each colander
            "percent": print the percent of each colander compared to entire number
        """
        if option == "count":
            print(self.histogram)
        elif option == "percent":
            print("{")
            for key in list(self.histogram.keys()):
                print("{}: {}".format(key, self.histogram[key]/len(self.chunk_list)))
            print("}")
        else:
            print(self.histogram)
    def compareHistogram(self, other_hist):
        """
        compare the distribution of two histogram.
        """
        pass
    def plotHistogram(self):
        """
        plot histogram.
        """
        # the key of self.histogram is sorted in ascending order
        od = collections.OrderedDict(sorted(self.histogram.items()))

        labels = list(od.keys())
        plt.bar(range(len(self.histogram)), self.histogram.values(), color='g', tick_label = labels)
        plt.show()


if __name__ == "__main__":
    func = Colander("/Users/pyo/blockchain/colander-hash/sample-data/test.txt")
    func.chopByChunk(16*B, set_count=5)
    func.makeHistogram()
    #func.printHistogram("percent")
    func.printHistogram("count")
    func.printParam()
    #func.plotHistogram()
    #print(b'\x7E'.decode("ascii")) 
