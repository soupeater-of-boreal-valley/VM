import math


def htoi(hex_):
    return int(hex_, 16)

def itoh(int_, bits_ = 8):
    value_ = hex(int_)[2:]

    hlen_  = math.floor(bits_ / 4)

    if len(value_) > hlen_:
        value_ = value_[len(value_)-hlen_:]

    if len(value_) != hlen_:
        value_ = '0' * [hlen_ - len(value_)][0] + value_
        #print(value_, hlen_)
    return value_

def notsi(hex_):
    if   hex_ == '0':
        return 'f'
    elif hex_ == '1':
        return 'e'
    elif hex_ == '2':
        return 'd'
    elif hex_ == '3':
        return 'c'
    elif hex_ == '4':
        return 'b'
    elif hex_ == '5':
        return 'a'
    elif hex_ == '6':
        return '9'
    elif hex_ == '7':
        return '8'
    elif hex_ == '8':
        return '7'
    elif hex_ == 'f':
        return '0'
    elif hex_ == 'e':
        return '1'
    elif hex_ == 'd':
        return '2'
    elif hex_ == 'c':
        return '3'
    elif hex_ == 'b':
        return '4'
    elif hex_ == 'a':
        return '5'
    elif hex_ == '9':
        return '6'
    else:
        raise(ValueError)



class _8bit:
    def __init__(self, num):

        self.value = 0

        self.mov(num)

    def geth(self):
        return self.value

    def geti(self):
        return htoi(self.value)

    def add(self, num: int):
        baseval_ = self.geti()

        newval_ = baseval_ + num

        self.value = itoh(newval_, 8)

        return 0

    def sub(self, num: int):
        baseval_ = self.geti()

        newval_ = baseval_ - num

        self.value = itoh(newval_, 8)

        return 0

    def mul(self, num: int):
        baseval_ = self.geti()

        newval_ = baseval_ * num

        self.value = itoh(newval_, 8)

    def div(self, num: int):
        baseval_ = self.geti()

        newval_ = math.floor(baseval_ / num)

        self.value = itoh(newval_, 8)

    def modulo(self, num: int):
        baseval_ = self.geti()

        newval_ = baseval_ % num

        self.value = itoh(newval_, 8)

    def not_(self, value):
        baseval_ = value

        newval_ = ''

        for l in baseval_:
            newval_ += notsi(l)

        self.value = newval_

    def mov(self, num: int):

        newval_ = itoh(num, 8)

        self.value = newval_

class _16bit:
    def __init__(self, num):

        self.value = 0

        self.mov(num)

    def geth(self):

        return self.value

    def geti(self):

        return htoi(self.value)

    def add(self, num: int):

        baseval_ = self.geti()

        newval_  = baseval_ + num

        self.value = itoh(newval_, 16)

        return 0

    def sub(self,num: int):

        baseval_ = self.geti()

        newval_ = baseval_ - num

        self.value = itoh(newval_, 16)

        return 0

    def mul(self,num: int):

        baseval_ = self.geti()

        newval_ = baseval_ * num

        self.value = itoh(newval_, 16)

    def div(self,num: int):

        baseval_ = self.geti()

        newval_ = math.floor(baseval_ / num)

        self.value = itoh(newval_, 16)

    def modulo(self,num: int):

        baseval_ = self.geti()

        newval_ = baseval_ % num

        self.value = itoh(newval_, 16)

    def not_(self):

        baseval_ = self.geth()

        newval_  = ''

        for l in baseval_:
            newval_ += notsi(l)

        self.value = newval_

    def mov(self, num: int):

        newval_  = itoh(num, 16)

        self.value = newval_