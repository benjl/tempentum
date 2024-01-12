import utils
import commands

COMMANDS = {'download': commands.download, 'srank': commands.srank, 'drank': commands.drank,
            'update': commands.update, 'stime': commands.stime, 'dtime': commands.dtime, 
            'rankall': commands.leaderboards, 'points': commands.pts, 'maplist': commands.maplist,
            'dtimeall': commands.dtimeall, 'stimeall': commands.stimeall, 'help': commands.help,
            'sgroups': commands.sgroups, 'dgroups': commands.dgroups, 'id': commands.id,
            'stimes': commands.stimes, 'dtimes': commands.dtimes, 'sgainers': commands.sgainers,
            'dgainers': commands.dgainers}

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