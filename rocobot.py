import rosettacode
import argparse
from random import choice as pick

def atLeastVersion(*args):
    from sys import version_info
    ver = version_info.major, version_info.minor, version_info.micro
    args = list(args)
    while len(args) < 3:
        args += [0]
    for i in zip(ver, args):
        if i[0] > i[1]:
            return True
        if i[0] < i[1]:
            return False
    return True

options = { 'prog': 'waste' }
if atLeastVersion(3, 14):
    options['color'] = False
parser = argparse.ArgumentParser(**options)

sp = parser.add_subparsers(dest='command')

sp_lang = sp.add_parser('lang', help='gimme a random language')
sp_lang.add_argument('--doesnt-have', help="give a language that this task isn't completed in", dest='task')
sp_lang.add_argument('--list', help='list all languages', dest='list', action='store_true')

sp_task = sp.add_parser('task', help='gimme a random uncompleted task')
sp_task.add_argument('lang', nargs='?', help='give a task not yet implemented in this language')
sp_task.add_argument('--list', help='list all tasks', dest='list', action='store_true')
sp_task.add_argument('-i', help='give a task that *is* implemented', dest='implemented', action='store_true')

args = parser.parse_args()

match args.command:
    case 'lang':
        if args.task == None:
            langs = rosettacode.languages()
        else:
            try:
                taskLangs = [x.title() for x in rosettacode.pageCategories(args.task)
                             if x in rosettacode.languages()]
            except rosettacode.PageDoesntExist:
                print(f"‘{args.task}’ doesn't seem to actually exist ಠ_ಠ")
                exit()
            langsNotInTask = [x for x in rosettacode.languages()
                              if x.title() not in taskLangs]
            langs = langsNotInTask

        if args.list:
            for i in langs:
                print(rosettacode.languageName(i))
        else:
            lang = pick(langs)
            print(rosettacode.languageName(lang))
            print(lang.full_url())

    case 'task':
        if args.implemented:
            tasks = rosettacode.tasks(args.lang)
        else:
            if args.lang != None:
                lang = rosettacode.language(args.lang)
            else:
                lang = pick(rosettacode.languages())
            tasks = rosettacode.tasksNotDoneInLanguage(lang)

        if args.list:
            for i in tasks:
                print(i.title())
        else:
            if args.lang == None:
                lang = pick(rosettacode.languages())
            else:
                lang = rosettacode.language(args.lang)

            try:
                task = pick(list(tasks))
                print('Language :', rosettacode.languageName(lang))
                print('Task     :', task.title())
                print(lang.full_url())
                print(task.full_url())
            except IndexError:
                print(f"Every task is already implemented in {rosettacode.languageName(lang)}!")

    case _:
        parser.print_help()
