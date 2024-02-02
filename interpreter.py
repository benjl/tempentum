import utils
import commands

if __name__ == '__main__':
    cmd = commands.Commands()
    print('Tempentum Point System')
    print('======================')
    while True:
        inp = input('>>> ')
        inp = inp.strip()
        tokens = inp.split(' ')
        if tokens[0] in cmd.cmdnames:
            if len(tokens) == 1:
                cmd.cmdnames[tokens[0]]([])
            else:
                cmd.cmdnames[tokens[0]](tokens[1:])
        else:
            print('Unknown command.')