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

    if args.website in ['dtc', 'bash']: # Only those websites are concerned by these options
        if args.lines < -1 or args.lines == 0: # Test if lines option is done properly
            print("Lines must be above or equal 1")
            sexit(1)
        if args.over < -1: # Test if over option is done properly
            print("\"over\" must be over (hehe) or equal 1")
            sexit(1)
        if args.under < -1 or args.under == 0: # Test if under option is done properly
            print("\"under\" must be over (wat?) or equal 1")
            sexit(1)
    url = {'dtc': "https://danstonchat.com/{}.html", 'nsf': "https://nuitsansfolie.com/nsf/{}", 'bash': "http://www.bash.org/?{}"}[args.website] # URL matrice
    website = {'dtc': 'DTC', 'nsf': 'NSF', 'bash': 'QDB'}[args.website] # Name to print

    if args.number >= 1: # If a number is specified, just take it
        number = args.number
        tmp_url = url.format(args.number)
        soup = get_soup(tmp_url, args.ignore, args.verbose)
        if soup == '':
            print("Error : Soup's empty, I need another bowl")
            sexit(1)
        lines, title, _ = preprocess(soup, args.number, args.website)
        content = process(lines, number, website)
        # TODO : Test for NSF if the lines can be printed "as it"
    elif args.website in ['dtc', 'bash']: # Else, consider the other passed options
        conditions = {'force': (args.force_title and args.website == 'dtc'), 'lines': (args.lines != -1),
                      'over': (args.over != -1), 'under': (args.under != -1)}
        answers = {'force': None, 'lines': None, 'over': None, 'under': None}
        if args.verbose:
            print("Required conditions: ", conditions)
        while conditions != answers:
            answers = {'force' : False, 'lines' : False, 'over' : False, 'under': False}
            number = randint(0, 20689) # TODO : Check both max numbers, automate their getting
            tmp_url = url.format(number)
            if args.verbose:
                print(color.YELLOW + "testing {} n°{}, url {}".format(website, number, tmp_url) + color.END)
            soup = get_soup(tmp_url, number, args.ignore)
            if soup != '':
                lines, title, title_exist = preprocess(soup, number, args.website)
                if lines != ['']:
                    content = process(lines, number, args.website)
                    for condition in (c for c in conditions if conditions[c]):
                        if args.verbose: print(color.PURPLE + "- testing {condition}" + color.END)
                        answers[condition] = test(condition, lines, args.lines, args.over,
                                                  args.under, title_exist)
                else:
                    answers = {}
    else:
        soup = None
        while not soup:
            number = randint(0, 20689) # TODO : Check max number
            tmp_url = url.format(number)
            if args.verbose:
                print(color.YELLOW + "testing {} n°{}, url {}".format(website, number, tmp_url) + color.END)
            soup = get_soup(tmp_url, number, args.ignore)
        lines, title, _ = preprocess(soup, args.number, args.website)
        content = process(lines, number, website)

    if not args.hide_banner:
        banner(title, {'dtc': 'DTC', 'nsf': 'NSF', 'bash': 'QDB'}[args.website], number, tmp_url, args.hide_title)
    print(content)
