import rosettacode
import argparse
from random import choice as pick

parser = argparse.ArgumentParser(
    prog='waste',
    color=False,
)
sp = parser.add_subparsers(dest='command')
sp_lang = sp.add_parser('lang', help='gimme a random language')
sp_lang.add_argument('--doesnt-have', help="give a language that this task isn't completed in", dest='task')
sp_task = sp.add_parser('task', help='gimme a random uncompleted task')
sp_task.add_argument('lang', nargs='?', help='give a task not yet completed in this language')

args = parser.parse_args()
match args.command:
    case 'lang':
        if args.task == None:
            lang = pick(rosettacode.languages())
        else:
            try:
                taskLangs = [x.title() for x in rosettacode.pageCategories(args.task)
                             if x in rosettacode.languages()]
            except rosettacode.PageDoesntExist:
                print(f"‘{args.task}’ doesn't seem to actually exist ಠ_ಠ")
                exit()
            langsNotInTask = [x for x in rosettacode.languages()
                              if x.title() not in taskLangs]
            lang = pick(langsNotInTask)
        print(rosettacode.languageName(lang))
        print(lang.full_url())
    case 'task':
        if args.lang != None:
            lang = rosettacode.language(args.lang)
        else:
            lang = pick(rosettacode.languages())
        try:
            task = pick(list(rosettacode.tasksNotDoneInLanguage(lang)))
            print('Language :', rosettacode.languageName(lang))
            print('Task     :', task.title())
            print(lang.full_url())
            print(task.full_url())
        except IndexError:
            print(f"Every task is already implemented in {rosettacode.languageName(lang)}!")
    case _:
        parser.print_help()
