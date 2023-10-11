
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

def WriteToSegment256 (LongAddress, ShortAddress, Data: list):

    WholeData = b''

    for Byte in Data:
        WholeData += chr(int(Byte, 16)).encode() 

    OldValue = open('drives\C.drv', 'rb').read()

    SegmentedHDIMG = wrap(OldValue, 259, 'norm')

    SegmentLoc = 'error'
    
    for CurrantSegmentLocation in SegmentedHDIMG:

        Segment = SegmentedHDIMG[CurrantSegmentLocation]
        
        AddressBytes = Segment[:3]
        CurrantLongAddress = int(hex(ord(AddressBytes[0]))[2:] + hex(ord(AddressBytes[1]))[2:], 16)
        if CurrantLongAddress != LongAddress:
            continue
        CurrantShortAddress = ord(AddressBytes[2])
        if CurrantShortAddress != ShortAddress:
            continue

        SegmentLoc = CurrantSegmentLocation
        
        break

    if type(SegmentLoc) == str:

        ByteAddress = LongAddress.to_bytes('big', 2) + ShortAddress.to_bytes('big', 1)

        SegmentedHDIMG += [ByteAddress + WholeData]
    
    else:
    
        SegmentedHDIMG[SegmentLoc] = AddressByte + WholeData

    NewValue = ''.join(SegmentedHDIMG)
    
    open('drives\C.drv', 'wb').write(NewValue)

def WriteToByte (AddressOne, AddressTwo, Data: int):

    

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
