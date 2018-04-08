# author: wjddn1801@snu.ac.kr
# github.com/jw-pyo/colander-hash

class Metric(object):
    def __init__(self):
        pass
    def chi-square(self, dict1, dict2):
        """
        chi-square histogram. If it closes to 0, two histogram is more similar.
        dict1: histogram 1
        dict2: histogram 2
        return: chi-square value
        """
        ret = 0
        for x, y in zip(list(dict1.values()), list(dict2.values())):
            ret += (x-y)**2 / (x+y)
        return ret
