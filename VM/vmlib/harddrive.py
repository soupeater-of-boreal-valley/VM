
def Wrap (Value, by, mode = 'norm'):

    OutputValue = []

    Counter = 0

    for Letter in Value:

        Counter += 1

        if mode == 'norm':
            OutputValue[len(OutputValue) - 1] += Letter

        elif mode == 'hex':
            OutputValue[len(OutputValue) - 1] += hex(ord(Letter))[2:4]

        if Counter == by:
            OutputValue += ['']
            Counter = 0

def powr(ind, by):

    out = ind
    for l in range(by - 1):
        out *= ind
    return out

def WriteToSegment256 (AddressOne, AddressTwo, Data: list):

    WholeData = b''

    for Byte in Data:
        WholeData += chr(int(Byte, 16)).encode()

    TotalAddressStart = AddressOne * powr(2, 16)
    TotalAddressStart += AddressTwo * powr(2, 8)

    TotalAddressEnd = TotalAddressStart + 256

    OldValue = open('drives\C.drv', 'rb').read()

    NewValue = OldValue[:TotalAddressStart] + WholeData + OldValue[TotalAddressEnd:]

    open('drives\C.drv', 'wb').write(NewValue)

def WriteToByte (AddressOne, AddressTwo, Data: int):

    WholeData = chr(Data).encode()

    TotalAddressStart = AddressOne * powr(2, 16)
    TotalAddressStart += AddressTwo * powr(2, 16)

    TotalAddressEnd = TotalAddressStart + 1

    OldValue = open('drives\C.drv', 'rb').read()

    NewValue = OldValue[:TotalAddressStart] + WholeData + OldValue[TotalAddressEnd:]

    open('drives\C.drv', 'wb').write(NewValue)

def ReadSegment256 (AddressOne, AddressTwo):


    TotalAddressStart = AddressOne * powr(2, 16)
    TotalAddressStart += AddressTwo * powr(2, 8)

    TotalAddressEnd = TotalAddressStart + 256

    Value = open('drives\C.drv', 'r').read()

    ReadValue = Wrap(Value[TotalAddressStart:TotalAddressEnd], 1, 'hex')

    return ReadValue

def ReadByte (AddressOne, AddressTwo):

    TotalAddressStart = AddressOne * powr(2, 16)
    TotalAddressStart += AddressTwo * powr(2, 16)

    TotalAddressEnd = TotalAddressStart + 1

    Value = open('drives\C.drv', 'r').read()

    ReadValue = Wrap(Value[TotalAddressStart:TotalAddressEnd], 1, 'hex')

    return ReadValue