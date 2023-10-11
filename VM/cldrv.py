
def powr(ind, by):

    out = ind
    for l in range(by):
        out *= ind
    return out

dat = 4294967296 / 2

print( dat / 1073741824, 'Gigabytes')
a = input()

import math

dat = '\x00' * math.floor(dat)
open('drives\\C.drv', 'w').write(dat)