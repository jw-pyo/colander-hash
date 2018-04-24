from timeit import default_timer

class Timer(object):
    def __init__(self, f_name, unit="ms"):
        self.timer = default_timer
        self.f_name = f_name
        self.unit = unit
    def __enter__(self):
        self.start = self.timer()
        return self
    def __exit__(self, *args):
        end = self.timer()
        self.elapsed_secs = end - self.start
        self.elapsed = self.elapsed_secs*1000
        if self.unit == "s":
            print("[%s] elapsed time: %f s" % (self.f_name, self.elapsed_secs))
        else:
            print("[%s] elapsed time: %f ms" % (self.f_name, self.elapsed))
if __name__ == '__main__':
    # example:
    #   'HTTP GET' from requests module, inside timer blocks.
    #   invoke the Timer context manager using the `with` statement.

    import requests

    url = 'https://github.com/timeline.json'

    # verbose (auto) timer output
    with Timer(verbose=True):
        r = requests.get(url)

    # print stored elapsed time in milliseconds
    with Timer() as t:
        r = requests.get(url)
    print('response time (millisecs): %.2f' % t.elapsed)

    # print stored elapsed time in seconds
    with Timer() as t:
        r = requests.get(url)
    print('response time (secs): %.3f' % t.elapsed_secs)
