from vmlib.VGA import *
import sys as s


def wrap1(str):

    i = []

    for l in str:
        i += [l]

    return i

inp_ = open(s.argv[1], 'r').read()
tabs = False

print(inp_)

inp_ = wrap1(inp_)

px = 0
py = 0
def message(VGA, inp, pos, event):

    global inp_, tabs, px, py

    if px <= 0:
        px = 0

    if event.type != KEYDOWN:
        return 0

    if inp == K_RIGHT:
        if len(inp_) <= px:
            inp_ += [' ']
        px += 1
        return 0

    if inp == K_LEFT:
        px -= 1
        return 0

    if inp == K_CAPSLOCK:
        tabs = not tabs
        return 0

    x = 20
    y = 0

    if inp == 8:
        try:
            del inp_[px]
            px -= 1
        except:
            return 0

    if inp != 0:
        if inp != 8:
            try:
                if tabs:
                    inp_[px] = chr(inp).upper()
                else:
                    inp_[px] = chr(inp)
                px += 1
                if len(inp_) <= px:
                    inp_ += [' ']
            except IndexError:
                inp_ += [' '] * [len(inp_) - px + 10][0]
            except Exception as e:
                print(repr(e))

    inpp = ''.join(inp_).replace('\n', '\r').replace('\r', ' ' * 100 + '\r')
    xx = 0
    for l in inpp:
        xx += 1
        if l == '\r':
            x = 20
            y += VGA.gletlen(1, 2.5)[1]

        elif l == '\t':
            x += VGA.gletlen(1, 2.5)[0] * 4

            x += VGA.gletlen(1, 2.5)[0]

        else:

            VGA.putlet(l, x, y, 1, 2.5, (0, 0, 255), (255, 255, 255))

            x += VGA.gletlen(1, 2.5)[0]

    x = 0
    y = 0

    inpp = ''.join(inp_).replace('\n', '\r')
    xx = 0
    for l in inpp:
        xx += 1
        if l == '\r':
            x = 20
            y += VGA.gletlen(1, 2.5)[1]

        elif l == '\t':
            x += VGA.gletlen(1, 2.5)[0] * 4

        elif xx == px:
            VGA.putlet(l, x, y, 1, 2.5, (255, 255, 255), (0, 0, 0))

            x += VGA.gletlen(1, 2.5)[0]

        else:

            VGA.putlet(l, x, y, 1, 2.5, (0, 0, 255), (255, 255, 255))

            x += VGA.gletlen(1, 2.5)[0]

    aa = '  ' * len(str(x) + ' ' + str(y) + ' ' + str(px))

    x = 560 * 1.5
    y = 470 * 1.5

    for l in aa:

        VGA.putlet(l, x, y, 1, 2.5, (0, 0, 255), (255, 255, 255))

        x += VGA.gletlen(1, 2.5)[0]

    aa = str(x) + ' ' + str(y) + ' ' + str(px)

    x = 560 * 1.5
    y = 470 * 1.5

    for l in aa:

        VGA.putlet(l, x, y, 1, 2.5, (0, 0, 255), (255, 255, 255))

        x += VGA.gletlen(1, 2.5)[0]

a = VGAscreen()

try:

    a.mainloop([message], [])

except Exception as e:
    print(repr(e))

print(inp_)
print(''.join(inp_))