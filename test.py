from itertools import repeat
from timeit import default_timer as timer
from multiprocessing import Pool
import random


def assign_integer(a):
    b = a
    return b

a = random.getrandbits(1)

start = timer()
for i in range(0, 1000000):
    assign_integer(a)
end = timer()
print(end - start)