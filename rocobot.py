import rosettacode
import argparse
from random import choice as pick

parser = argparse.ArgumentParser(
    prog='waste',
    color=False,
)
sp = parser.add_subparsers(dest='command')
sp.add_parser('lang', help='gimme a random language')
sp_task = sp.add_parser('task', help='gimme a random uncompleted task')
sp_task.add_argument('lang', nargs='?', help='give a task not yet completed in this language')

args = parser.parse_args()
match args.command:
    case 'lang':
        lang = pick(rosettacode.languages())
        print(rosettacode.languageName(lang))
    case 'task':
        if args.lang != None:
            lang = rosettacode.language(args.lang)
        else:
            lang = pick(rosettacode.languages())
        try:
            task = pick(list(rosettacode.tasksNotDoneInLanguage(lang)))
            print('Language :', rosettacode.languageName(lang))
            print('Task     :', task.title())
        except IndexError:
            print(f"Every task is already implemented in {rosettacode.languageName(lang)}!")
    case _:
        parser.print_help()
