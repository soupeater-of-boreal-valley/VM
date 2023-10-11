def GetRegisterByOpname16bit(opname):
    if opname == '0':
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
    if opname == '0':
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

def GetOparationByPOI(poi):

    poi = poi.upper()

    if poi == '00':
        return ('sysn', ['>'])

    elif poi == '10':
        return ('movs', ['%', 0, 0, 8], ['$', 3])

    elif poi == '11':
        return ('movl', ['%', 0, 0, 16], ['$$', 2, 3])

    elif poi == '12':
        return ('movs', ['%', 0, 0, 8], ['%', 3, 1, 8])

    elif poi == '13':
        return ('movl', ['%', 0, 0, 16], ['%', 3, 1, 16])

    elif poi == '14':
        return ('movs', ['%', 0, 0, 8], ['@', ['%', 3, 0, 16], ['%', 3, 1, 8]])

    elif poi == '15':
        return ('movs', ['@', ['%', 0, 0, 16], ['%', 2, 1, 8]], ['%', 3, 1, 8])

    elif poi == '20':
        return ('adds', ['%', 0, 0, 8], ['$', 3])

    elif poi == '21':
        return ('addl', ['%', 0, 0, 16], ['$$', 2, 3])

    elif poi == '22':
        return ('adds', ['%', 0, 0, 8], ['%', 3, 1, 8])

    elif poi == '23':
        return ('addl', ['%', 0, 0, 16], ['%', 3, 1, 16])

    elif poi == '30':
        return ('subs', ['%', 0, 0, 8], ['$', 3])

    elif poi == '31':
        return ('subl', ['%', 0, 0, 16], ['$$', 2, 3])

    elif poi == '32':
        return ('subs', ['%', 0, 0, 8], ['%', 3, 1, 8])

    elif poi == '33':
        return ('subl', ['%', 0, 0, 16], ['%', 3, 1, 16])

    elif poi == '40':
        return ('muls', ['%', 0, 0, 8], ['$', 3])

    elif poi == '41':
        return ('mull', ['%', 0, 0, 16], ['$$', 2, 3])

    elif poi == '42':
        return ('muls', ['%', 0, 0, 8], ['%', 3, 1, 8])

    elif poi == '43':
        return ('mull', ['%', 0, 0, 16], ['%', 3, 1, 16])

    elif poi == '50':
        return ('divs', ['%', 0, 0, 8], ['$', 3])

    elif poi == '51':
        return ('divl', ['%', 0, 0, 16], ['$$', 2, 3])

    elif poi == '52':
        return ('divs', ['%', 0, 0, 8], ['%', 3, 1, 8])

    elif poi == '53':
        return ('divl', ['%', 0, 0, 16], ['%', 3, 1, 16])

    elif poi == '60':
        return ('mods', ['%', 0, 0, 8], ['$', 3])

    elif poi == '61':
        return ('modl', ['%', 0, 0, 16], ['$$', 2, 3])

    elif poi == '62':
        return ('mods', ['%', 0, 0, 8], ['%', 3, 1, 8])

    elif poi == '63':
        return ('modl', ['%', 0, 0, 16], ['%', 3, 1, 16])

    elif poi == '70':
        return ('nots', ['%', 0, 0, 8], ['$', 3])

    elif poi == '71':
        return ('notl', ['%', 0, 0, 16], ['$$', 2, 3])

    elif poi == '72':
        return ('nots', ['%', 0, 0, 8], ['%', 3, 1, 8])

    elif poi == '73':
        return ('notl', ['%', 0, 0, 16], ['%', 3, 1, 16])

    elif poi == '80':
        return ('swcr', ['%', 0, 0, 16], ['$$', 2, 3])

    elif poi == '81':
        return ('swcr', ['%', 0, 0, 16], ['%', 3, 1, 16])

    elif poi == '82':
        return ('swch', ['#', ['%', 0, 0, 16], ['%', 0, 1, 8]], ['$$', 2, 3])

    elif poi == '83':
        return ('swch', ['#', ['%', 0, 0, 16], ['%', 0, 1, 8]], ['%', 3, 1, 16])

    elif poi == '84':
        return('swch', ['@', ['%', 0, 0, 16], ['%', 0, 1, 8]], ['#', ['%', 0, 0, 16], ['%', 0, 1, 16]])

    elif poi == '85':
        return ('swch', ['#', ['%', 0, 0, 16], ['%', 0, 1, 8]], ['@', ['%', 0, 0, 16], ['%', 0, 1, 16]])

    elif poi == '86':
        return ('repr', ['%', 0, 0, 16], ['$$', 2, 3])

    elif poi == '87':
        return ('repr', ['%', 0, 0, 16], ['%', 3, 1, 16])

    elif poi == '88':
        return ('reph', ['#', ['%', 0, 0, 16], ['%', 0, 1, 8]], ['$$', 2, 3])

    elif poi == '89':
        return ('reph', ['#', ['%', 0, 0, 16], ['%', 0, 1, 8]], ['%', 3, 1, 16])

    elif poi == '8A':
        return ('reph', ['%', 0, 0, 16], ['#', ['$$', 2, 3], ['%', 0, 1, 8]])

    elif poi == '8B':
        return ('reph', ['%', 0, 0, 16], ['#', ['%', 3, 1, 16], ['%', 0, 1, 8]])

    elif poi == '90':
        return ('cmps', ['%', 0, 0, 8], ['%', 0, 0, 8])

    elif poi == '91':
        return ('cmps', ['%', 0, 0, 8], ['$', 3])

    elif poi == '92':
        return ('cmpl', ['%', 0, 0, 16], ['%', 3, 1, 16])

    elif poi == '93':
        return ('cmps', ['%', 0, 0, 16], ['$$', 2, 3])

    elif poi == 'A0':
        return ('jnel', ['$', 0], ['$$', 2, 3])

    elif poi == 'A1':
        return ('jnes', ['%', 0, 0, 8])

    elif poi == 'A2':
        return ('jnzl', ['$', 0], ['$$', 2, 3])

    elif poi == 'A3':
        return ('jnzs', ['%', 0, 0, 8])

    elif poi == 'A4':
        return ('jnml', ['$', 0], ['$$', 2, 3])

    elif poi == 'A5':
        return ('jnms', ['%', 0, 0, 8])

    elif poi == 'A6':
        return ('jnll', ['$', 0], ['$$', 2, 3])

    elif poi == 'A7':
        return ('jnls', ['$', 3])

    elif poi == 'A8':
        return ('jmps', ['$', 3])

    elif poi == 'A9':
        return ('jmpl', ['%', 0, 0, 16], ['%', 3, 1, 8])

    elif poi == 'AA':
        return ('jmpl', ['$', 0], ['$$', 2, 3])

    elif poi == 'C0':
        return ('plys', ['%', 0, 0, 8])

    elif poi == 'C1':
        return ('plyl', ['%', 0, 0, 16])

    else:
        return ('noop', ['>'])

def Stringify(Format, Reg, RAM, Fetch):

    StrOut = ''

    if Format[0] == '%':
        Address = Format[1:]

        Op = Fetch[Address[0]][Address[1]]

        if Format[3] == 8:

            if GetRegisterByOpname8bit(Op)[1] != 0:
                StrOut = '%' + GetRegisterByOpname8bit(Op)[0].lower() + '<' + str(GetRegisterByOpname8bit(Op)[1]) + '>'
            else:
                StrOut = '%' + GetRegisterByOpname8bit(Op)[0].lower()
        if Format[3] == 16:
            if GetRegisterByOpname16bit(Op)[1] != 0:
                StrOut = '%' + GetRegisterByOpname16bit(Op)[0].lower() + '<' + str(GetRegisterByOpname16bit(Op)[1]) + '>'
            else:
                StrOut = '%' + GetRegisterByOpname16bit(Op)[0].lower()

    elif Format[0] == '$':

        Hex = Fetch[Format[1]]

        StrOut = '$' + Hex.upper()

    elif Format[0] == '$$':

        Hex = Fetch[Format[1]] + Fetch[Format[2]]

        StrOut = '$' + Hex.upper()

    elif Format[0] == '>':

        StrOut = '<POSSIBLE ERROR>'

    elif Format[0] == '@':

        Data1 = Stringify(Format[1], Reg, RAM, Fetch)
        Data2 = Stringify(Format[2], Reg, RAM, Fetch)

        StrOut = '@[' + Data1 + ':' + Data2 + ']'

    elif Format[0] == '#':

        Data1 = Stringify(Format[1], Reg, RAM, Fetch)
        Data2 = Stringify(Format[2], Reg, RAM, Fetch)

        StrOut = '#[' + Data1 + ':' + Data2 + ']'


    elif Format[0] == 'prt':

        StrOut = Format[1]

    else:
        StrOut = 'UNK_FORMAT'

    return StrOut

def Process(Poi, Reg, RAM, Fetch):

    OutPut = [Poi[0]]

    for l in range(len(Poi[1:])):
        l = l + 1
        OutPut += [Stringify(Poi[l], Reg, RAM, Fetch)]

        if l != len(Poi) - 1:
            OutPut[l] += ','
        else:
            if l != 1:
                OutPut[l] = ' ' * [20 - len(' '.join(OutPut[:l]))][0] + OutPut[l]

    return OutPut

def strdisasm(Fetched, Registers, RAM):


    POI = Fetched[1]

    POIData = GetOparationByPOI(POI)

    POIData = Process(POIData, Registers, RAM, Fetched)

    if Fetched == ['00', '00', '00', '00']:
        POIData = ['SYS_EXIT']

    elif Fetched == ['00', '00', '00', '01']:
        POIData = ['SYS_DISP_REG']

    elif Fetched == ['01', '00', '00', '02']:
        POIData = ['SYS_FLIP']

    OutPut = '' + ''.join(Fetched).upper() + '   ' + ' '.join(POIData) + ' ' * 17

    return OutPut