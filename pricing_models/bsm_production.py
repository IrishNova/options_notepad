import math
import datetime as dt


class Model:

    def __init__(self, p, n, r, s, v, t0):
        self.p =  p
        self.n = n
        self.r = r
        self.s = s
        self.t0 = t0
        self.v = v

    def theta_decay(self):
        return self.t0 - dt.time() / 365 # time left

    def d1(self):
        ...

    def d2(self):
        ...

    def iv(self):
        ...

    def run_model(self):
        ...
