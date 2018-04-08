
# unit
KB = 1024
MB = 1024*1024
GB = 1024*1024*1024

class Colander(object):

    def __init__(self, path):
        self.path = path
        self.chunk_size = None
        self.chunk_list = None
        self.colander_size = 3
        self.histogram = dict()
    def printParam(self):
        print("""
        data path: {}
        chunk size: {}
        total chunk: {}
        """.format(self.path, self.chunk_size, len(self.chunk_list))
        )

    def chopByChunk(self, chunk_size = 32*MB, save=False):
        """
        chop the file by chunk and return chunk list in memory.
        path: file path
        return: chunk_list(byte array)
        """
        self.chunk_size = chunk_size
        chunk_list = []
        with open(self.path, "rb") as f:
            fstream = f.read()
            chunk_list = [fstream[i*chunk_size:(i+1)*chunk_size] for i in range(int(len(fstream)/chunk_size))]
        if save is True:
            self.chunk_list = chunk_list
        return chunk_list
    def colander(self, i):
        """
        pass single chunk to the colander hash function and return result.
        i: the i-th chunk in chunk_list
        return: [0-Z]
        """
        return self.chunk_list[i][:self.colander_size]

        pass
    def compareChunk(self, i, j):
        pass
    def makeHistogram(self):
        """
        make histogram
        """
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
        pass


if __name__ == "__main__":
    func = Colander("/Users/pyo/blockchain/colander-hash/sample-data/1.picture.jpeg")
    func.chopByChunk(16, True)
    func.makeHistogram()
    func.printHistogram("percent")
    func.printParam()
    #print(b'\x7E'.decode("ascii")) 
