from sys import exit as sexit
from random import randint

from dtcli.process import get_soup, preprocess, process
from dtcli.test import test
from dtcli.color import color
from dtcli.cmdline import cmd_parser, banner


def main():
    """
    Main Function
    """
    args = cmd_parser()

    if args.website in ['dtc', 'bashorg']:
        if args.lines < -1 or args.lines == 0:
            print("Lines must be above or equal 1")
        if args.over < -1:
            print("\"over\" must be over (hehe) or equal 1")
        if args.under < -1 or args.under == 0:
            print("\"under\" must be over or equal 1")

    if args.number == -1:
        conditions = {'force': args.force_title, 'lines': (args.lines != -1),
                      'over': (args.over != -1), 'under': (args.under != -1)}
        answers = {'force': None, 'lines': None, 'over': None, 'under': False}
        if args.verbose:
            print("Required conditions: ", conditions)

    if args.website == 'dtc':
        if args.number != -1 and args.number >= 1:
            url = "https://danstonchat.com/%d.html" % args.number
            soup = get_soup(url, args.ignore, args.verbose)
            if soup == '':
                sexit(1)
            lines, title, _ = preprocess(soup, args.website, args.number)
            dtc = process(lines, args.number, args.website)
            if not args.hide_banner:
                banner(title, 'DTC', args.number, url, args.hide_title)
            print(dtc[:-1])
        else:
            pass
    elif args.website == 'nsf':
        if args.number != -1 and args.number >= 1:
            url = "https://nuitsansfolie.com/nsf/%d" % args.number
            soup = get_soup(url, args.ignore, args.verbose)
            if soup == '':
                sexit(1)
            lines, _, _ = preprocess(soup, args.website, args.number)
            nsf = '\n'.join(lines)
            if not args.hide_banner:
                banner(title, 'NSF', args.number, url, args.hide_title)
            print(nsf)
        else:
            pass
    else:
        if args.number != -1 and args.number >= 1:
            url = "bash.org/?%d" % args.number
            soup = get_soup(url, args.ignore, args.verbose)
            if soup == '':
                sexit(1)
            lines, _, _ = preprocess(soup, args.website, args.number)
            qdb = process(lines, args.number, args.website)
            if not args.hide_banner:
                banner(title, 'QDB', args.number, url, args.hide_title)
            print(qdb[:-1])
        else:
            pass


    if args.number == -1: # If a number isn't specified
        while conditions != answers:
            answers = {'force' : False, 'lines' : False, 'over' : False, 'under': False}
            number = randint(0, 20689)
            url = "https://danstonchat.com/%d.html" % number
            if args.verbose: print(color.YELLOW + "testing n°%d, url %s" % (number, url) + color.END)
            soup = get_soup(url, number, args.ignore)
            if soup != '':
                lines, title, title_exist = preprocess(soup, number)
                dtc = process(lines, number)
                for l in (c for c in conditions if conditions[c] == True):
                    if args.verbose: print(color.PURPLE + "- testing %s" % l + color.END)
                    answers[l] = test(l, lines, title_exist, args.lines, args.over, args.under)
