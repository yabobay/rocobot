import pywikibot
from pywikibot import pagegenerators

class PageDoesntExist(Exception): pass

site_ = None
def site():
    global site_
    if site_ == None:
        site_ = pywikibot.Site()
    return site_

def pageCategories(name):
    page = pywikibot.Page(site(), name)
    if not page.exists():
        raise PageDoesntExist()
    return page.categories()

languagesMemo = None
def languages():
    global languagesMemo
    if languagesMemo != None:
        return languagesMemo
    cat = pywikibot.Category(site(), 'Programming Languages')
    languagesMemo = list(cat.subcategories())
    return languagesMemo

def language(language):
    if languagesMemo != None:
        for i in languagesMemo:
            if language == i.title() or language == i.title().replace('Category:', ''):
                return i
    return pywikibot.Category(site(), language)

tasksMemo = {}
def tasks(lang=None):
    if lang in tasksMemo:
        return tasksMemo[lang]
    match lang:
        case None:
            cat = pywikibot.Category(site(), 'Category:Programming Tasks')
            tasksMemo[None] = list(cat.articles())
        case str():
            return tasks(language(lang))
        case pywikibot.page._category.Category():
            tasksMemo[lang] = lang.articles()
        case _:
            raise TypeError('Argument needs to be a Category')
    return tasksMemo[lang]

def languageName(lang):
    if type(lang) != pywikibot.page._category.Category:
        raise TypeError('Argument needs to be a Category')
    return lang.title().replace('Category:', '')

def tasksNotDoneInLanguage(lang):
    match lang:
        case pywikibot.page._category.Category():
            tasksInThisLang = [x.title() for x in tasks(lang)]
            return (x for x in tasks()
                    if x.title() not in tasksInThisLang)
        case str():
            return tasksNotDoneInLanguage(language(lang))
        case _:
            raise TypeError('Argument needs to be a Category')
