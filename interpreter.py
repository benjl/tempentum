import utils
import commands

def helpcmd(args):
    """help | Prints information on the usage of a given command."""
    if len(args) == 0:
        print(f'Command list: {", ".join(COMMANDS.keys())}')
        return
    if args[0].lower() in COMMANDS.keys():
        print(COMMANDS[args[0]].__doc__)
        return
    else:
        print('Command not found.')

COMMANDS = {'download': commands.download, 'srank': commands.srank, 'drank': commands.drank,
            'update': commands.update, 'stime': commands.stime, 'dtime': commands.dtime, 
            'rankall': commands.leaderboards, 'points': commands.pts, 'maplist': commands.maplist,
            'dtimeall': commands.dtimeall, 'stimeall': commands.stimeall,
            'sgroups': commands.sgroups, 'dgroups': commands.dgroups, 'id': commands.id,
            'stimes': commands.stimes, 'dtimes': commands.dtimes, 'sgainers': commands.sgainers,
            'dgainers': commands.dgainers, 'help': helpcmd, 'noobs': commands.newplayers}

if __name__ == '__main__':
    print('Tempentum Point System')
    print('======================')
    while True:
        inp = input('>>> ')
        inp = inp.strip()
        tokens = inp.split(' ')
        if tokens[0] in COMMANDS.keys():
            if len(tokens) == 1:
                COMMANDS[tokens[0]]([])
            else:
                COMMANDS[tokens[0]](tokens[1:])
        else:
            print('Unknown command.')