import math
import vmlib.regtypes as r

def powr(Arg1, Arg2):

    ValueOut = Arg1

    for l in range(Arg2-1):
        ValueOut *= Arg1

    return ValueOut

class Ram:
    def __init__(self, AddressArg1=16, AddressArg2=8):

        self.AddressSize1 = powr(2, AddressArg1)
        self.AddressSize2 = powr(2, AddressArg2)

        self.RAMValue = [['00' for x in range( self.AddressSize2 )] for x in range( self.AddressSize1 )]

    def CheckAddressVelidity(self, Address1, Address2):

        if self.AddressSize1 < Address1-1:
            return False
        elif self.AddressSize2 < Address2-1:
            return False
        else:
            return True

    def SetValueInteger(self, Address1, Address2, Value):

        HexValue = r.itoh(Value, 8)

        if not self.CheckAddressVelidity(Address1, Address2):
            return False

        self.RAMValue[Address1][Address2] = HexValue

        return True

    def GetValueInteger(self, Address1, Address2):

        if not self.CheckAddressVelidity(Address1, Address2):
            raise(ValueError)

        return self.RAMValue[Address1][Address2]

    def SetValueSectionInteger(self, Address1, Value):

        for DataLocation in range(len(Value)):

            if type(Value[DataLocation]) != int:
                raise(TypeError)

            if not self.CheckAddressVelidity(Address1, DataLocation):
                raise (ValueError)

            self.RAMValue[Address1][DataLocation] = r.itoh(Value[DataLocation], 8)

        return True

    def GetValueSectionHex(self, Address1):

        if not self.CheckAddressVelidity(Address1, 0):
            raise (ValueError)
        return self.RAMValue[Address1]

    def SetValueSectionHex(self, Address1, Value):

        for DataLocation in range(len(Value)):

            if len(Value[DataLocation]) != 2:
                raise (TypeError)

            if not self.CheckAddressVelidity(Address1, DataLocation):
                raise (ValueError)

            try:
                self.RAMValue[Address1][DataLocation] = Value[DataLocation]
            except:
                pass
        return True

    def SetValueHex(self, Address1, Address2, Value):

        if len(Value) != 2:
            raise (TypeError)

        if not self.CheckAddressVelidity(Address1, Address2):
            raise (ValueError)

        self.RAMValue[Address1][Address2] = Value

    def GetValueHex(self, Address1, Address2):

        if not self.CheckAddressVelidity(Address1, Address2):
            raise (ValueError)

        return self.RAMValue[Address1][Address2]