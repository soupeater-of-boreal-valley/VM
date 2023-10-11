import os
import sys
from vmlib import regtypes as r
from vmlib import disasm
from vmlib.VGA import *
from vmlib import Ram
import vmlib.harddrive as hd
from vmlib import steak as s
import textwrap as tw
import time
import math

if sys.argv[1] != 'norm':
    if sys.argv[1] == 'shz':
        hz = int(sys.argv[2], 10)
    else:
        print('error, unknown mode.')
        quit()

else:
    hz = 123012303210321

NOTIME = False

for arg in sys.argv:
    if arg == 'ntm':
        NOTIME = True

print('\x99'.join(os.listdir(os.getcwd())))

a = math.sqrt(int('FFFF', 16))
print(a)

def GetRegisterByOpname16bit(opname):

        if   opname == '0':
            return ('EPC', 0)

        elif opname == '1':
            return ('AX', 0)

        elif opname == '2':
            return ('R1X', 0)

        elif opname == '3':
            return ('R2X', 0)

        elif opname == '4':
            return ('ESP', 0)

        elif opname == '5':
            return ('FLG', 0)

        elif opname == '6':
            return ('ERP', 0)

        elif opname == '7':
            return ('POS', 0)

        elif opname == '8':
            return ('POS', 1)

        elif opname == '9':
            return ('EVT', 0)

        elif opname.upper() == 'A':
            return ('KBI', 0)

        else:
            return 0

def GetRegisterByOpname8bit(opname):

        if   opname == '0':
            return ('PC', 0)

        elif opname == '1':
            return ('AH', 0)

        elif opname == '2':
            return ('AL', 0)

        elif opname == '3':
            return ('R1', 0)

        elif opname == '4':
            return ('R2', 0)

        elif opname == '5':
            return ('CL1', 0)

        elif opname == '6':
            return ('CL1', 1)

        elif opname == '7':
            return ('CL1', 2)

        elif opname == '8':
            return ('CL2', 0)

        elif opname == '9':
            return ('CL2', 1)

        elif opname.upper() == 'A':
            return ('CL2', 2)

        elif opname.upper() == 'B':
            return ('SP', 0)

        elif opname.upper() == 'C':
            return ('CCL', 0)

        else:
            return 0

def VGAprint(string, vga_, pos_, bg=(20,20,20), fg=(255,255,255)):

        x = pos_[0]
        y = pos_[1]

        for l in string:
            vga_.putlet(l, x, y, 2, 3, bg, fg)
            x += vga_.gletlen(2, 3)[0]

        return vga_.gletlen(2, 1.5)

def powr(ind, by):

        out = ind
        for l in range(by - 1):
            out *= ind
        return out

def LoadROMToRAM(vga_):
    global RAM

    vga_.cls((20, 20, 20))
    XGraphicalAxis = 0
    YGraphicalAxis = 0
    VGAAxisIncrement = VGAprint(  ["R", "O", "M", " ", "P", "R", "O", "C", "E", "S", "S", " ", "~", " ", "L", "O", "A", "D", "I", "N", "G", " ", "P", "R", "O", "C", "E", "S", "S", " ", "S", "T", "A", "R", "T"],  vga_,  (XGraphicalAxis, YGraphicalAxis))
    YGraphicalAxis += VGAAxisIncrement[1]
    ROMValuesPureArray = open('ROM', 'r').readlines()

    for LineValue in ROMValuesPureArray:

        AddressHexValue = LineValue[:4]
        AddressIntegerValue = r.htoi(AddressHexValue)
        VGAprint("ROM PROCESS ~ BASE ADDRESS #=> " + str(AddressIntegerValue), vga_, (XGraphicalAxis, YGraphicalAxis))
        YGraphicalAxis += VGAAxisIncrement[1]
        ROMCodeValues = tw.wrap(LineValue[5:], 2)
        RAM.SetValueSectionHex(AddressIntegerValue, ROMCodeValues)

    VGAprint("ROM PROCESS ~ COMPLETED ROM LOAD v", vga_, (XGraphicalAxis, YGraphicalAxis))

    print(end='')

def Timer():
    global timer, VGAScreenConnection, hz
    a = time.time()
    out = a - timer

    VGAprint('zzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzz', VGAScreenConnection, (0, 190 * VGAScreenConnection.incby[1]))
    VGAprint('DIFFERENCE : ' + str(out), VGAScreenConnection, (0, 230 * VGAScreenConnection.incby[1]))
    VGAprint('HERTZ      : ' + str(1 / out), VGAScreenConnection, (0, 240 * VGAScreenConnection.incby[1]))
    timer = a

    if hz != 123012303210321:
        time.sleep(1 / hz - 0.011)

def FetchData(Registers):

    global RAM

    AddressInteger1 = Registers['EPC'][0].geti()
    AddressInteger2 = Registers['PC'][0].geti()

    FetchDataCells = ['00', '00', '00', '00']

    for ValueLocation in range(4):
        FetchDataCells[ValueLocation] = RAM.GetValueHex(AddressInteger1, AddressInteger2 + ValueLocation)

    IntegerDataPCNew = Registers['PC'][0].geti() + 4

    if IntegerDataPCNew >= 256:
        Registers['EPC'][0].add(1)
        Registers['PC'][0].mov(0)

    else:
        Registers['PC'][0].mov(IntegerDataPCNew)

    return FetchDataCells

def GetGMD():

    data = []

    Address = r.htoi('FF00')

    while True:

        if Address >= r.htoi('FF0F'):
            return data
        Focus = RAM.GetValueSectionHex(Address)
        Address += 1
        E = False
        for Byte in Focus:

            if E:
                if Byte == 'FE':
                    return data
                else:
                    E = False
            if Byte != 'FF':
                data += [Byte]

            else:
                E = True


def DisplayCurrantRamData( VGA, INP, POS, EVT):

    global RAM, VGAScreenConnection, Registers

    MemoryAddress = r.htoi('FF00')

    GraphicalMemoryData = GetGMD()


    GraphicalMode = RAM.GetValueHex(r.htoi('FF10'), 0)

    GraphicalColorOne = [Registers['CL1'][0].geti(), Registers['CL1'][1].geti(), Registers['CL1'][2].geti()]
    GraphicalColorTwo = [Registers['CL2'][0].geti(), Registers['CL2'][1].geti(), Registers['CL2'][2].geti()]

    for G in range(len(GraphicalColorOne)):

        if GraphicalColorOne[G] == 0:
            GraphicalColorOne[G] = 20

        if GraphicalColorTwo[G] == 0:
            GraphicalColorTwo[G] = 20

    if GraphicalMode == '00':
        VGAScreenConnection.cls(GraphicalColorOne)

    if GraphicalMode == '01':

        XGraphicalAxis = 0
        YGraphicalAxis = 0

        IncrementationValue = VGAScreenConnection.gletlen(3.75, 2.8125)

        counter = 0

        for DataByte in GraphicalMemoryData:

            counter += 1

            #DataByte = GraphicalMemoryData[DataByteIndex].replace('00', '20')

            VGAScreenConnection.putlet(chr(r.htoi(DataByte.replace('00', '20'))), XGraphicalAxis, YGraphicalAxis, 3.75, 2.8125, fg=GraphicalColorOne)

            XGraphicalAxis += IncrementationValue[0]

            if counter == 32:
                counter = 0
                XGraphicalAxis = 0

                YGraphicalAxis += IncrementationValue[1]

    # 2 color low graphical mode
    elif GraphicalMode == '02':

        XGraphicalAxis = 0
        YGraphicalAxis = 0
        IncrementationValue = VGAScreenConnection.gletlen(3.75, 3.75)
        counter = 0

        for DataByte in GraphicalMemoryData:

            counter += 1

            if DataByte != '01':
                VGAScreenConnection.disp(GraphicalColorOne, XGraphicalAxis, YGraphicalAxis, IncrementationValue[0], IncrementationValue[1] + 15)

            XGraphicalAxis += IncrementationValue[0]
            if counter == 32:
                counter = 0
                XGraphicalAxis = 0
                YGraphicalAxis += IncrementationValue[1]

    elif GraphicalMode == '03':

        counter = 0
        counterTwo = 0

        x = 0
        y = 0

        increment = VGAScreenConnection.gletlen(1, 2.5)

        while True:
            if counter >= len(GraphicalMemoryData):
                break

            Colors = GraphicalMemoryData[counter]

            counter += 1
            counterTwo +=1

            LetterValue = GraphicalMemoryData[counter]

            counter += 1
            counterTwo += 1

            Fg = GetVGAColor(Colors[1])
            Bg = GetVGAColor(Colors[0])

            VGAScreenConnection.putlet(chr(int(LetterValue, 16)), x, y, 1, 2.5, fg=Fg, bg=Bg)

            x += increment[0]

            if counterTwo == 158:
                y += increment[1]
                x = 0
                counterTwo = 0

    VGAScreenConnection.flp()

def GetVGAColor(Hexval):

    if Hexval == '0':
        return (20, 20, 20)

    if Hexval == '1':
        return (20, 20, 200)

    if Hexval == '2':
        return (20, 200, 20)

    if Hexval == '3':
        return (200, 20, 20)

    if Hexval == '4':
        return (20, 200, 20)

    if Hexval == '5':
        return (200, 20, 200)

    if Hexval == '6':
        return (20, 200, 200)

    if Hexval == '7':
        return (200, 200, 200)

    if Hexval == '8':
        return (20, 100, 200)

    if Hexval == '9':
        return (20, 200, 100)

    if Hexval == 'A':
        return (20, 100, 100)

    if Hexval == 'B':
        return (100, 20, 200)

    if Hexval == 'C':
        return (200, 20, 100)

    if Hexval == 'D':
        return (100, 20, 100)

    if Hexval == 'E':
        return (100, 200, 20)

    if Hexval == 'F':
        return (200, 100, 20)
    return (255 / 2, 255 / 2, 255 / 2)

def ExecuteInstruction(Operation, VGAScreen, Registers, RAM):
    FullDword = ''.join(Operation)

    # Command Type : Part 0
    if FullDword == '00000000':

        print()
        for l in Registers:
            print(l + ' ' * [4-len(l)][0], end=' -- ')
            for reg in Registers[l]:
                print(reg.geth(), ' ' * [5 - len(reg.geth())][0], reg.geti(), end = ' ' * [5 - len(str(reg.geti()))][0])

            print()

        pygame.quit()
        raise (ValueError)

    if FullDword == '00000001':

        print()
        for l in Registers:
            print(l + ' ' * [4-len(l)][0], end=' -- ')
            for reg in Registers[l]:
                print(reg.geth(), ' ' * [5 - len(reg.geth())][0], reg.geti(), end=' ' * [5 - len(str(reg.geti()))][0])

            print()
    if FullDword == '01000002':
        #
        DisplayCurrantRamData(VGAScreen, (0, 0), 0, 0)

    PartOneInstruction = FullDword[2:4].upper()
    a = 0.01012313041258501275
    # Command Type : Part 1
    if a >= 1:
        pass
        pass

    # movs %$   DONE
    elif PartOneInstruction == '10':

        MoveValueData = Operation[3]
        RegisterData = GetRegisterByOpname8bit(Operation[0][0])
        Registers[RegisterData[0]][RegisterData[1]].mov(r.htoi(MoveValueData))

    # movl %$   DONE
    elif PartOneInstruction == '11':

        MoveValueData = Operation[2] + Operation[3]
        RegisterData = GetRegisterByOpname16bit(Operation[0][0])
        Registers[RegisterData[0]][RegisterData[1]].mov(r.htoi(MoveValueData))

    # movs %%   DONE
    elif PartOneInstruction == '12':

        RegisterInputData = GetRegisterByOpname8bit(Operation[3][1])
        RegisterOutputData = GetRegisterByOpname8bit(Operation[0][0])
        Registers[RegisterOutputData[0]][RegisterOutputData[1]].mov(Registers[RegisterInputData[0]][RegisterInputData[1]].geti())

    # movl %%   DONE
    elif PartOneInstruction == '13':

        RegisterInputData = GetRegisterByOpname16bit(Operation[3][1])
        RegisterOutputData = GetRegisterByOpname16bit(Operation[0][0])
        Registers[RegisterOutputData[0]][RegisterOutputData[1]].mov(Registers[RegisterInputData[0]][RegisterInputData[1]].geti())

    # movs %@   DONE
    elif PartOneInstruction == '14':

        AddressOneRegisterData = GetRegisterByOpname16bit(Operation[3][0])
        AddressTwoRegisterData = GetRegisterByOpname8bit (Operation[3][1])
        AddressOneData = Registers[AddressOneRegisterData[0]][AddressOneRegisterData[1]].geti()
        AddressTwoData = Registers[AddressTwoRegisterData[0]][AddressTwoRegisterData[1]].geti()
        RegisterData = GetRegisterByOpname8bit(Operation[0][0])
        Registers[RegisterData[0]][RegisterData[1]].mov(r.htoi(RAM.GetValueInteger(AddressOneData, AddressTwoData)))

    # mov @%    DONE
    elif PartOneInstruction == '15':
        AddressOneRegisterData = GetRegisterByOpname16bit(Operation[0][0])
        AddressTwoRegisterData = GetRegisterByOpname8bit(Operation[3][0])
        AddressOneData = Registers[AddressOneRegisterData[0]][AddressOneRegisterData[1]].geti()
        AddressTwoData = Registers[AddressTwoRegisterData[0]][AddressTwoRegisterData[1]].geti()
        RegisterData = GetRegisterByOpname8bit(Operation[3][1])
        RAM.SetValueInteger(AddressOneData, AddressTwoData, Registers[RegisterData[0]][RegisterData[1]].geti())

    # adds %$   DONE
    elif PartOneInstruction == '20':

            MoveValueData = Operation[3]
            RegisterData = GetRegisterByOpname8bit(Operation[0][0])
            Registers[RegisterData[0]][RegisterData[1]].add(r.htoi(MoveValueData))

    # addl %$   DONE
    elif PartOneInstruction == '21':

            MoveValueData = Operation[2] + Operation[3]
            RegisterData = GetRegisterByOpname16bit(Operation[0][0])
            Registers[RegisterData[0]][RegisterData[1]].add(r.htoi(MoveValueData))

    # adds %%   DONE
    elif PartOneInstruction == '22':

            RegisterInputData = GetRegisterByOpname8bit(Operation[3][1])
            RegisterOutputData = GetRegisterByOpname8bit(Operation[0][0])
            Registers[RegisterOutputData[0]][RegisterOutputData[1]].add(
                Registers[RegisterInputData[0]][RegisterInputData[1]].geti())

    # addl %%   DONE
    elif PartOneInstruction == '23':

            RegisterInputData = GetRegisterByOpname16bit(Operation[3][1])
            RegisterOutputData = GetRegisterByOpname16bit(Operation[0][0])
            Registers[RegisterOutputData[0]][RegisterOutputData[1]].add(
                Registers[RegisterInputData[0]][RegisterInputData[1]].geti())

    # subs %$   DONE
    elif PartOneInstruction == '30':

                MoveValueData = Operation[3]
                RegisterData = GetRegisterByOpname8bit(Operation[0][0])
                Registers[RegisterData[0]][RegisterData[1]].mov(r.htoi(MoveValueData))

    # subl %$   DONE
    elif PartOneInstruction == '31':

                MoveValueData = Operation[2] + Operation[3]
                RegisterData = GetRegisterByOpname16bit(Operation[0][0])
                Registers[RegisterData[0]][RegisterData[1]].sub(r.htoi(MoveValueData))

    # subs %%   DONE
    elif PartOneInstruction == '32':

                RegisterInputData = GetRegisterByOpname8bit(Operation[3][1])
                RegisterOutputData = GetRegisterByOpname8bit(Operation[0][0])
                Registers[RegisterOutputData[0]][RegisterOutputData[1]].sub(
                    Registers[RegisterInputData[0]][RegisterInputData[1]].geti())

    # subl %%   DONE
    elif PartOneInstruction == '33':

                RegisterInputData = GetRegisterByOpname16bit(Operation[3][1])
                RegisterOutputData = GetRegisterByOpname16bit(Operation[0][0])
                Registers[RegisterOutputData[0]][RegisterOutputData[1]].sub(
                    Registers[RegisterInputData[0]][RegisterInputData[1]].geti())

    # muls %$   DONE
    elif PartOneInstruction == '40':

                    MoveValueData = Operation[3]
                    RegisterData = GetRegisterByOpname8bit(Operation[0][0])
                    Registers[RegisterData[0]][RegisterData[1]].mul(r.htoi(MoveValueData))

    # mull %$   DONE
    elif PartOneInstruction == '41':

                    MoveValueData = Operation[2] + Operation[3]
                    RegisterData = GetRegisterByOpname16bit(Operation[0][0])
                    Registers[RegisterData[0]][RegisterData[1]].mul(r.htoi(MoveValueData))

    # muls %%   DONE
    elif PartOneInstruction == '42':

                    RegisterInputData = GetRegisterByOpname8bit(Operation[3][1])
                    RegisterOutputData = GetRegisterByOpname8bit(Operation[0][0])
                    Registers[RegisterOutputData[0]][RegisterOutputData[1]].mul(
                        Registers[RegisterInputData[0]][RegisterInputData[1]].geti())

    # mull %%   DONE
    elif PartOneInstruction == '43':

                    RegisterInputData = GetRegisterByOpname16bit(Operation[3][1])
                    RegisterOutputData = GetRegisterByOpname16bit(Operation[0][0])
                    Registers[RegisterOutputData[0]][RegisterOutputData[1]].mul(
                        Registers[RegisterInputData[0]][RegisterInputData[1]].geti())

    # divs %$   DONE
    elif PartOneInstruction == '50':

                        MoveValueData = Operation[3]
                        RegisterData = GetRegisterByOpname8bit(Operation[0][0])
                        Registers[RegisterData[0]][RegisterData[1]].div(r.htoi(MoveValueData))

    # divl %$   DONE
    elif PartOneInstruction == '51':

                        MoveValueData = Operation[2] + Operation[3]
                        RegisterData = GetRegisterByOpname16bit(Operation[0][0])
                        Registers[RegisterData[0]][RegisterData[1]].div(r.htoi(MoveValueData))

    # divs %%   DONE
    elif PartOneInstruction == '52':

                        RegisterInputData = GetRegisterByOpname8bit(Operation[3][1])
                        RegisterOutputData = GetRegisterByOpname8bit(Operation[0][0])
                        Registers[RegisterOutputData[0]][RegisterOutputData[1]].div(
                            Registers[RegisterInputData[0]][RegisterInputData[1]].geti())

    # divl %%   DONE
    elif PartOneInstruction == '53':

                        RegisterInputData = GetRegisterByOpname16bit(Operation[3][1])
                        RegisterOutputData = GetRegisterByOpname16bit(Operation[0][0])
                        Registers[RegisterOutputData[0]][RegisterOutputData[1]].div(
                            Registers[RegisterInputData[0]][RegisterInputData[1]].geti())

    # mods %$   DONE
    elif PartOneInstruction == '60':

                            MoveValueData = Operation[3]
                            RegisterData = GetRegisterByOpname8bit(Operation[0][0])
                            Registers[RegisterData[0]][RegisterData[1]].modulo(r.htoi(MoveValueData))

    # modl %$   DONE
    elif PartOneInstruction == '61':

                            MoveValueData = Operation[2] + Operation[3]
                            RegisterData = GetRegisterByOpname16bit(Operation[0][0])
                            Registers[RegisterData[0]][RegisterData[1]].modulo(r.htoi(MoveValueData))

    # mods %%   DONE
    elif PartOneInstruction == '62':

                            RegisterInputData = GetRegisterByOpname8bit(Operation[3][1])
                            RegisterOutputData = GetRegisterByOpname8bit(Operation[0][0])
                            Registers[RegisterOutputData[0]][RegisterOutputData[1]].modulo(
                                Registers[RegisterInputData[0]][RegisterInputData[1]].geti())

    # modl %%   DONE
    elif PartOneInstruction == '63':

                            RegisterInputData = GetRegisterByOpname16bit(Operation[3][1])
                            RegisterOutputData = GetRegisterByOpname16bit(Operation[0][0])
                            Registers[RegisterOutputData[0]][RegisterOutputData[1]].modulo(
                                Registers[RegisterInputData[0]][RegisterInputData[1]].geti())

    # nots %$   DONE
    elif PartOneInstruction == '70':

                    MoveValueData = Operation[3]
                    RegisterData = GetRegisterByOpname8bit(Operation[0][0])
                    Registers[RegisterData[0]][RegisterData[1]].not_(MoveValueData)

    # notl %$   DONE
    elif PartOneInstruction == '71':

                    MoveValueData = Operation[2] + Operation[3]
                    RegisterData = GetRegisterByOpname16bit(Operation[0][0])
                    Registers[RegisterData[0]][RegisterData[1]].not_(MoveValueData)

    # nots %%   DONE
    elif PartOneInstruction == '72':

                    RegisterInputData = GetRegisterByOpname8bit(Operation[3][1])
                    RegisterOutputData = GetRegisterByOpname8bit(Operation[0][0])
                    Registers[RegisterOutputData[0]][RegisterOutputData[1]].not_(
                        Registers[RegisterInputData[0]][RegisterInputData[1]].geth())

    # notl %%   DONE
    elif PartOneInstruction == '73':

                    RegisterInputData = GetRegisterByOpname16bit(Operation[3][1])
                    RegisterOutputData = GetRegisterByOpname16bit(Operation[0][0])
                    Registers[RegisterOutputData[0]][RegisterOutputData[1]].not_(
                        Registers[RegisterInputData[0]][RegisterInputData[1]].geth())

    # swcr @%@$ DONE
    elif PartOneInstruction == '80':

        RegisterData = GetRegisterByOpname16bit(Operation[0][0])
        RegisterValue = Registers[RegisterData[0]][RegisterData[1]].geti()

        AddressValue = r.htoi(Operation[2] + Operation[3])

        SectionDataOne = RAM.GetValueSectionHex(RegisterValue)
        SectionDataTwo = RAM.GetValueSectionHex(AddressValue)

        RAM.SetValueSectionHex(RegisterValue, SectionDataTwo)
        RAM.SetValueSectionHex(AddressValue, SectionDataOne)

    # swcr @%@% DONE
    elif PartOneInstruction == '81':

        RegisterDataOne = GetRegisterByOpname16bit(Operation[0][0])
        RegisterValue = Registers[RegisterDataOne[0]][RegisterDataOne[1]].geti()
        RegisterDataTwo = GetRegisterByOpname16bit(Operation[3][1])
        AddressValue = Registers[RegisterDataTwo[0]][RegisterDataTwo[1]].geti()
        SectionDataOne = RAM.GetValueSectionHex(RegisterValue)
        SectionDataTwo = RAM.GetValueSectionHex(AddressValue)

        RAM.SetValueSectionHex(RegisterValue, SectionDataTwo)
        RAM.SetValueSectionHex(AddressValue, SectionDataOne)

    # swch #%@$ DONE
    elif PartOneInstruction == '82':

        RegisterData             = GetRegisterByOpname16bit(Operation[0][0])
        RegisterData1            = GetRegisterByOpname16bit(Operation[0][1])
        RegisterValue            = Registers[RegisterData[0]][RegisterData[1]].geti()
        RegisterValueOne         = Registers[RegisterData1[0]][RegisterData1[1]].geti()
        AddressValue             = r.htoi(Operation[2] + Operation[3])
        SectionDataOne           = hd.ReadSegment256(RegisterValue, RegisterValueOne)
        SectionDataTwo           = RAM.GetValueSectionHex(AddressValue)

        hd.WriteToSegment256(RegisterValue, RegisterValueOne, SectionDataTwo)
        RAM.SetValueSectionHex(AddressValue, SectionDataOne)

    # swch #%@% DONE
    elif PartOneInstruction == '83':

        RegisterData             = GetRegisterByOpname16bit(Operation[0][0])
        RegisterData1            = GetRegisterByOpname16bit(Operation[0][1])
        RegisterValue            = Registers[RegisterData[0]][RegisterData[1]].geti()
        RegisterValueOne         = Registers[RegisterData1[0]][RegisterData1[1]].geti()
        AddressValue             = GetRegisterByOpname16bit(Operation[3][1])
        AddressValue             = Registers[AddressValue[0]][AddressValue[1]].geti()
        SectionDataOne           = hd.ReadSegment256(RegisterValue, RegisterValueOne)
        SectionDataTwo           = RAM.GetValueSectionHex(AddressValue)

        hd.WriteToSegment256(RegisterValue, RegisterValueOne, SectionDataTwo)
        RAM.SetValueSectionHex(AddressValue, SectionDataOne)

    # swcr @%@% DONE
    elif PartOneInstruction == '84':

        RAMAddressRegisterDataOne= GetRegisterByOpname16bit(Operation[0][0])
        RAMAddressRegisterDataTwo= GetRegisterByOpname16bit(Operation[3][1])
        AddressDataOne           = [Registers[RAMAddressRegisterDataOne[0][RAMAddressRegisterDataOne[1]]].geti(),
                                   Registers[RAMAddressRegisterDataTwo[0][RAMAddressRegisterDataTwo[1]]].geti()]
        DataOne                  = RAM.GetValueSectionHex(AddressDataOne[0])

        RAM.SetValueSectionHex(AddressDataOne[0], RAM.GetValueSectionHex(AddressDataOne[1]))
        RAM.SetValueSectionHex(AddressDataOne[1], DataOne)

    # swch @%#% DONE
    elif PartOneInstruction == '85':

        HDRegisterDataOne        = GetRegisterByOpname16bit(Operation[3][0])
        HDRegisterDataTwo        = GetRegisterByOpname8bit(Operation[3][1])
        HardDriveAddressOne      = Registers[HDRegisterDataOne[0]][HDRegisterDataOne[1]].geti()
        HardDriveAddressTwo      = Registers[HDRegisterDataTwo[0]][HDRegisterDataTwo[1]].geti()
        DataToPlaceInteger       = Registers[GetRegisterByOpname16bit(Operation[0][0])[0]][GetRegisterByOpname16bit(Operation[0][0])[1]].geti()
        Data                     = hd.ReadSegment256(HardDriveAddressOne, HardDriveAddressTwo)

        RAM.SetValueSectionHex(DataToPlaceInteger, Data)
        hd.WriteToSegment256(HardDriveAddressOne, HardDriveAddressTwo, RAM.GetValueSectionHex(DataToPlaceInteger))

    # swch #%@% DONE
    elif PartOneInstruction == '86':

        HDRegisterDataOne        = GetRegisterByOpname16bit(Operation[0][0])
        HDRegisterDataTwo        = GetRegisterByOpname16bit(Operation[2][1])
        HardDriveAddressOne      = Registers[HDRegisterDataOne[0]][HDRegisterDataOne[1]].geti()
        HardDriveAddressTwo      = Registers[HDRegisterDataTwo[0]][HDRegisterDataTwo[1]].geti()
        RAMRegister              = GetRegisterByOpname16bit(Operation[3][0])
        RAMRegisterTwo           = GetRegisterByOpname16bit(Operation[3][1])
        DataToPlaceInteger       = Registers[RAMRegister[0]][RAMRegister[1]].geti()
        DataToPlaceIntegerTwo    = Registers[RAMRegisterTwo[0]][RAMRegisterTwo[1]].geti()
        Data                     = hd.ReadByte(HardDriveAddressOne, HardDriveAddressTwo)

        RAM.SetValueHex(DataToPlaceInteger, DataToPlaceIntegerTwo, Data)
        hd.WriteToByte(HardDriveAddressOne, HardDriveAddressTwo, RAM.GetValueSectionHex(DataToPlaceInteger))

    # rplr @%@$ DONE
    elif PartOneInstruction == '87':

        PrimaryRegisterData       = GetRegisterByOpname16bit(Operation[0][0])
        SecondaryAddress          = r.htoi(Operation[2] + Operation[3])
        PrimaryAddress            = Registers[PrimaryRegisterData[0]][PrimaryRegisterData[1]].geti()

        RAM.SetValueSectionHex(PrimaryAddress, RAM.GetValueSectionHex(SecondaryAddress))

    # rplr @%@% DONE
    elif PartOneInstruction == '88':

        RAMAddressRegisterDataOne = GetRegisterByOpname16bit(Operation[0][0])
        RAMAddressRegisterDataTwo = GetRegisterByOpname16bit(Operation[3][1])
        AddressDataOne            = [Registers[RAMAddressRegisterDataOne[0][RAMAddressRegisterDataOne[1]]].geti(), Registers[RAMAddressRegisterDataTwo[0][RAMAddressRegisterDataTwo[1]]].geti()]

        RAM.SetValueSectionHex(AddressDataOne[0], RAM.GetValueSectionHex(AddressDataOne[1]))

    # rplh #%@$ DONE
    elif PartOneInstruction == '89':

        HDAddressRegisterDataOne = GetRegisterByOpname16bit(Operation[0][0])
        HDAddressRegisterDataTwo = GetRegisterByOpname8bit(Operation[0][1])
        RAMAddress               = r.htoi(Operation[2] + Operation[3])
        HDAddressOne             = Registers[HDAddressRegisterDataOne[0]][HDAddressRegisterDataOne[1]].geti()
        HDAddressTwo             = Registers[HDAddressRegisterDataTwo[0]][HDAddressRegisterDataTwo[1]].geti()

        hd.WriteToSegment256(HDAddressOne, HDAddressTwo, RAM.GetValueSectionHex(RAMAddress))

    # rplh #%@% DONE
    elif PartOneInstruction == '8A':

        HDAddressRegisterDataOne = GetRegisterByOpname16bit(Operation[0][0])
        HDAddressRegisterDataTwo = GetRegisterByOpname8bit(Operation[0][1])
        RAMAddressRegisterData   = GetRegisterByOpname16bit(Operation[3][1])
        RAMAddress               = Registers[RAMAddressRegisterData[0]][RAMAddressRegisterData[1]].geti()
        HDAddressOne             = Registers[HDAddressRegisterDataOne[0]][HDAddressRegisterDataOne[1]].geti()
        HDAddressTwo             = Registers[HDAddressRegisterDataTwo[0]][HDAddressRegisterDataTwo[1]].geti()

        hd.WriteToSegment256(HDAddressOne, HDAddressTwo, RAM.GetValueSectionHex(RAMAddress))

    # rplh @%#$ DONE
    elif PartOneInstruction == '8B':

        RAMAddressRegisterData   = GetRegisterByOpname16bit(Operation[0][0])
        HDAddressRegisterData    = GetRegisterByOpname16bit(Operation[0][1])
        RAMAddress               = Registers[RAMAddressRegisterData[0]][RAMAddressRegisterData[1]].geti()
        HDAddressOne             = r.htoi(Operation[2] + Operation[3])
        HDAddressTwo             = Registers[HDAddressRegisterData[0]][HDAddressRegisterData[1]].geti()
        HDData                   = hd.ReadSegment256(HDAddressOne, HDAddressTwo)

        RAM.SetValueSectionHex(RAMAddress, HDData)

    # rplh @%#% DONE
    elif PartOneInstruction == '8C':

        RAMAddressRegisterData   = GetRegisterByOpname16bit(Operation[0][0])
        HDAddressRegisterDataOne = GetRegisterByOpname16bit(Operation[0][1])
        HDAddressRegisterDataTwo = GetRegisterByOpname8bit(Operation[3][1])
        RAMAddress               = Registers[RAMAddressRegisterData[0]][RAMAddressRegisterData[1]].geti()
        HDAddressOne             = Registers[HDAddressRegisterDataTwo[0]][HDAddressRegisterDataTwo[1]].geti()
        HDAddressTwo             = Registers[HDAddressRegisterDataOne[0]][HDAddressRegisterDataOne[1]].geti()
        HDData                   = hd.ReadSegment256(HDAddressOne, HDAddressTwo)

        RAM.SetValueSectionHex(RAMAddress, HDData)

    # cmps %%   DONE
    elif PartOneInstruction == '90':

        RegisterDataOne = GetRegisterByOpname8bit(Operation[0][0])
        RegisterDataTwo = GetRegisterByOpname8bit(Operation[3][1])

        RegisterOne = Registers[RegisterDataOne[0]][RegisterDataOne[1]].geti()
        RegisterTwo = Registers[RegisterDataTwo[0]][RegisterDataTwo[1]].geti()

        outdata = '0000'

        if RegisterOne == RegisterTwo:
            outdata = '0001'

        if RegisterOne > RegisterTwo:
            outdata = '1000'

        Registers['FLG'][0].mov(r.htoi(outdata))

    # cmps %$   DONE
    elif PartOneInstruction == '91':

        RegisterDataOne = GetRegisterByOpname8bit(Operation[0][0])

        RegisterOne = Registers[RegisterDataOne[0]][RegisterDataOne[1]].geti()
        RegisterTwo = r.htoi(Operation[3])

        outdata = '0000'

        if RegisterOne == RegisterTwo:
            outdata = '0001'

        if RegisterOne > RegisterTwo:
            outdata = '1000'



        Registers['FLG'][0].mov(r.htoi(outdata))

    # cmpl %%   DONE
    elif PartOneInstruction == '92':

        RegisterDataOne = GetRegisterByOpname16bit(Operation[0][0])
        RegisterDataTwo = GetRegisterByOpname16bit(Operation[3][1])

        RegisterOne = Registers[RegisterDataOne[0]][RegisterDataOne[1]].geti()
        RegisterTwo = Registers[RegisterDataTwo[0]][RegisterDataTwo[1]].geti()

        outdata = '0000'

        if RegisterOne == RegisterTwo:
            outdata = '0001'

        if RegisterOne > RegisterTwo:
            outdata = '1000'

        Registers['FLG'][0].mov(r.htoi(outdata))

    # cmpl %$   DONE
    elif PartOneInstruction == '90':

        RegisterDataOne = GetRegisterByOpname16bit(Operation[0][0])

        RegisterOne = Registers[RegisterDataOne[0]][RegisterDataOne[1]].geti()
        RegisterTwo = r.htoi(Operation[2] + Operation[3])

        outdata = '0000'

        if RegisterOne == RegisterTwo:
            outdata = '0001'

        if RegisterOne > RegisterTwo:
            outdata = '1000'

        Registers['FLG'][0].mov(r.htoi(outdata))



    # jnel $$   DONE
    elif PartOneInstruction == 'A0':

        Address = r.htoi(Operation[2] + Operation[3])
        Short = r.htoi(Operation[0])

        flag = Registers['FLG'][0].geth()

        if flag != '0001':
            Registers['EPC'][0].mov(Address)
            Registers['PC'][0].mov(Short)

    # jnes %    DONE

    elif PartOneInstruction == 'A1':

        RegisterData = GetRegisterByOpname8bit(Operation[0][0])

        Address = Registers[RegisterData[0]][RegisterData[1]].geti()

        flag = Registers['FLG'][0].geth()

        if flag != '0001':
            Registers['PC'][0].mov(Address)

    # jnzl $$   DONE
    elif PartOneInstruction == 'A2':

        Address = r.htoi(Operation[2] + Operation[3])
        Short = r.htoi(Operation[0])

        flag = Registers['FLG'][0].geth()

        if flag == '0001':
            Registers['EPC'][0].mov(Address)
            Registers['PC'][0].mov(Short)

    # jnzs %    DONE
    elif PartOneInstruction == 'A3':

        RegisterData = GetRegisterByOpname8bit(Operation[0][0])

        Address = Registers[RegisterData[0]][RegisterData[1]].geti()

        flag = Registers['FLG'][0].geth()
        if flag == '0001':
            Registers['PC'][0].mov(Address)

    # jnml $$   DONE
    elif PartOneInstruction == 'A4':

        Address = r.htoi(Operation[2] + Operation[3])
        Short = r.htoi(Operation[0])

        flag = Registers['FLG'][0].geth()

        if flag != '1000':
            Registers['EPC'][0].mov(Address)
            Registers['PC'][0].mov(Short)


    # jnms %    DONE
    elif PartOneInstruction == 'A5':

        RegisterData = GetRegisterByOpname8bit(Operation[0][0])

        Address = Registers[RegisterData[0]][RegisterData[1]].geti()

        flag = Registers['FLG'][0].geth()

        if flag != '1000':
            Registers['PC'][0].mov(Address)

    # jnll $$   DONE
    elif PartOneInstruction == 'A6':

        Address = r.htoi(Operation[2] + Operation[3])
        Short = r.htoi(Operation[0])

        flag = Registers['FLG'][0].geth()

        if flag != '0000':
            Registers['EPC'][0].mov(Address)
            Registers['PC'][0].mov(Short)

    # jnls %    DONE
    elif PartOneInstruction == 'A7':

        RegisterData = GetRegisterByOpname8bit(Operation[0][0])

        Address = Registers[RegisterData[0]][RegisterData[1]].geti()

        flag = Registers['FLG'][0].geth()

        if flag != '0000':
            Registers['PC'][0].mov(Address)

    # jmps $    TODO
    elif PartOneInstruction == 'A8':
        Value = r.htoi(Operation[3])

        Registers['PC'][0].mov(Value)

    # jmpl %%   TODO
    if PartOneInstruction == 'AA':

        RegisterOne = GetRegisterByOpname16bit(Operation[0][0])
        RegisterTwo = GetRegisterByOpname8bit(Operation[3][1])

        AddressData = Registers[RegisterOne[0]][RegisterOne[1]].geti()
        Short = Registers[RegisterTwo[0]][RegisterTwo[1]].geti()

        Registers['PC'][0].mov(Short)
        Registers['EPC'][0].mov(AddressData)


    # jmpl $$   TODO
    if PartOneInstruction == 'AA':

        AddressData = r.htoi(Operation[2] + Operation[3])
        Short = r.htoi(Operation[0])

        Registers['PC'][0].mov(Short)
        Registers['EPC'][0].mov(AddressData)

    # brns %    TODO


    # brns $    TODO


    # brnl %%   TODO


    # brnl $$   TODO


    # ret       TODO



    # pshs %    TODO


    # pshs $    TODO


    # pshl %    TODO


    # pshl $    TODO


    # pops %    TODO


    # popl %    TODO



    # plas %    TODO
    elif PartOneInstruction == 'C0':

        RegisterLocation = GetRegisterByOpname8bit(Operation[0][0])
        RegisterLocationA = GetRegisterByOpname8bit(Operation[0][1])

        Data = Registers[RegisterLocation[0]][RegisterLocation[1]].geti()
        Dur = Registers[RegisterLocationA[0]][RegisterLocationA[1]].geti()

        s.f8beep(Data, Dur)

    # plal %    TODO
    elif PartOneInstruction == 'C1':

        RegisterLocation = GetRegisterByOpname16bit(Operation[0][0])
        RegisterLocationA = GetRegisterByOpname8bit(Operation[0][1])

        Data = Registers[RegisterLocation[0]][RegisterLocation[1]].geti()
        Dur = Registers[RegisterLocationA[0]][RegisterLocationA[1]].geti()

        s.f16beep(Data, Dur)


    # bnel $$   TODO


    # bnzl $$   TODO



def PushData(Byte:str):
    global Registers, RAM

    RAM.GetValueHex(Registers['ESP'][0].geti(), Registers['SP'][0].geti(), r.htoi(Byte))

    if Registers['SP'][0].geth() == 'FF':
        Registers['SP'][0].mov(0)
        Registers['ESP'][0].add(1)

    else:
        Registers['SP'][0].add(1)

def FetchDecodeExecuteCycle(VgaScreenConnection, InputInteger, PossitionalTuple, EventWhole):
    global Registers, RAM

    if InputInteger == K_LEFT:
        Registers['KBI'][0].mov(1)

    elif InputInteger == K_RIGHT:
        Registers['KBI'][0].mov(2)

    elif InputInteger == K_UP:
        Registers['KBI'][0].mov(3)

    elif InputInteger == K_DOWN:
        Registers['KBI'][0].mov(4)

    elif InputInteger == K_CAPSLOCK:
        Registers['KBI'][0].mov(5)

    elif InputInteger == K_TAB:
        Registers['KBI'][0].mov(6)

    elif InputInteger == K_LSHIFT:
        Registers['KBI'][0].mov(7)

    elif InputInteger == K_RSHIFT:
        Registers['KBI'][0].mov(8)

    else:
        Registers['KBI'][0].mov(InputInteger)

    Registers['POS'][0].mov(PossitionalTuple[0])
    Registers['POS'][1].mov(PossitionalTuple[1])

    Registers['EVT'][0].mov(EventWhole.type)
    FetchedOparation = FetchData(Registers)
    #print('fx' + Registers['EPC'][0].geth() + '.' + Registers['PC'][0].geth(), '~', disasm.strdisasm(FetchedOparation, Registers, RAM))
    ExecuteInstruction(FetchedOparation, VgaScreenConnection, Registers, RAM)
    if hz != 123012303210321:
        VGAprint(disasm.strdisasm(FetchedOparation, Registers, RAM).upper(), VGAScreenConnection, (0, 210 * VGAScreenConnection.incby[1]))
    if not NOTIME:
        Timer()

timer = time.time()
VGAScreenConnection = VGAscreen()

VGAprint("LOADING RAM PLEAS WAIT .. .. ..", VGAScreenConnection, (0, 0))

VGAScreenConnection.flp()

RAM = Ram.Ram(16, 8)
Registers = {
        'PC' : [r._8bit (0)],
        'EPC': [r._16bit(0)],
        'AH' : [r._8bit (0)],
        'AL' : [r._8bit (0)],
        'AX' : [r._16bit(0)],
        'R1' : [r._8bit (0)],
        'R2' : [r._8bit (0)],
        'R1X': [r._16bit(0)],
        'R2X': [r._16bit(0)],
        'CL1': [r._8bit (0), r._8bit (0), r._8bit (0)],
        'CL2': [r._8bit (0), r._8bit (0), r._8bit (0)],
        'SP' : [r._8bit (0)],
        'ESP': [r._16bit(0)],
        'CCL': [r._8bit (1)],
        'FLG': [r._16bit(0)],
        'RP ': [r._8bit (0)],
        'ERP': [r._16bit(0)],
        'POS': [r._16bit(0), r._16bit(0)],
        'EVT': [r._16bit(0)],
        'KBI': [r._16bit(0)]
}

def DisplayOldRAMData(RAM):
    print('RAM DATA DISPLAY')

    while True:

        a = input(' $ ').split(' ')

        if a[0] == 'DISP':

            try:
                address = int(a[1], 16)
            except:
                print(f'invalid address {a[1]}')
                continue

            COUNTER = 0

            fetched = []

            for l in range(len(RAM[address])):
                fetched += [RAM[address][l]]
                COUNTER += 1
                if COUNTER >= 4:
                    print('fx' + r.itoh(address, 16) + '.' + r.itoh(l, 8) + ' ~ ' + disasm.strdisasm(fetched, Registers, RAM))
                    fetched = []
                    COUNTER = 0

        if a[0] == 'QUIT':
            quit(0)
VGAScreenConnection.mainloop([FetchDecodeExecuteCycle], [LoadROMToRAM])

DisplayOldRAMData(RAM.RAMValue)