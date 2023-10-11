import os

menu = '''
            MENU
------------------------------
        PEEK -- PRINT HARD DRIVE VALUE AT LOCATION
        POKE -- WRITE BYTE TO HARD DRIVE
        QUIT -- QUIT  RUN
     IMGPEEK -- PRINT IMAGE FILE VALUE
     IMGPOKE -- WRITE BYTE TO FOCUSED IMAGE
    IMGMOUNT -- FOCUS ON IMAGE FILE
        BURN -- WRITE FOCUSED IMAGE TO HARD DRIVE
'''

IMGMOUNT   = ''
HARD_DRIVE = 'drives\C.drv'

while True:
    os.system('cls')
    print(menu)
    print('    IMGMOUNT -> ' + IMGMOUNT )
    #print('23' * 256)
    UserAction = input()

    ActionCommands = UserAction.split(' ')

    if ActionCommands[0].upper() == 'IMGMOUNT':
        IMGMOUNT = ' '.join(ActionCommands[1:])

    if ActionCommands[0].upper() == 'BURN':

        OldHD = open(HARD_DRIVE, 'rb').read()
        Image = open(IMGMOUNT  , 'rb').read()
        NewHD = Image + OldHD[len(Image):]

        del OldHD
        del Image

        open(HARD_DRIVE, 'wb').write(NewHD)

        del NewHD

    if ActionCommands[0].upper() == 'QUIT':
        quit(0)

