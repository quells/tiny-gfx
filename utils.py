import math

def bitcount(max_value: int, signed: bool = False):
    count = int(math.ceil(math.log(max_value) / math.log(2)))
    if signed:
        count += 1
    return count
