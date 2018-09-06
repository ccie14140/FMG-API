from random import *

def random_fgt_sn():
    tail_sn = 0
    fgt_sn = ""
    for num in range(6):
        tail_sn = randint(0,9)
        fgt_sn += str(tail_sn)
    print("FGT50E3U16" + fgt_sn)

random_fgt_sn()


