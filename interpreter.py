import utils
import commands

COMMANDS = {'download': commands.download, 'srank': commands.srank, 'drank': commands.drank,
            'update': commands.update, 'stime': commands.stime, 'dtime': commands.dtime, 
            'rankall': commands.leaderboards, 'lookup': commands.lookup, 'maplist': commands.maplist,
            'dtimeall': commands.dtimeall, 'stimeall': commands.stimeall}

if __name__ == '__main__':
    print('Tempentum Point System')
    print('======================')
    while True:
        inp = input('>>> ')
        tokens = inp.split(' ')
        if tokens[0] in COMMANDS.keys():
            if len(tokens) == 1:
                COMMANDS[tokens[0]]([])
            else:
                COMMANDS[tokens[0]](tokens[1:])
        else:
            print('Unknown command.')