
# unit
KB = 1024
MB = 1024*1024
GB = 1024*1024*1024

class Colander(object):

    def __init__(self, path):
        self.path = path
        self.chunk_list = None
    def chopByChunk(self, chunk_size = 32*MB, save=False):
        """
        chop the file by chunk and return chunk list in memory.
        path: file path
        return: chunk_list(byte array)
        """
        chunk_list = []
        with open(self.path, "rb") as f:
            fstream = f.read()
            chunk_list = [fstream[i*chunk_size:(i+1)*chunk_size] for i in range(int(len(fstream)/chunk_size))]
        if save is True:
            self.chunk_list = chunk_list
        return chunk_list
    def colander(self, i):
        pass
    def compareChunk(self, i, j):
        pass




if __name__ == "__main__":
    func = Colander("/Users/pyo/blockchain/colander-hash/sample-data/test.txt")
    print(func.chopByChunk(16))
    print(b'\x7E'.decode("ascii")) 
