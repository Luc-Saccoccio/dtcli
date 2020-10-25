"""
    File containing the commands
    "Main" File
"""


from sys import exit as sexit # 1) s{ys}exit, and 2) {sex}it, funny right ?
from random import randint # Only import what's needed

from dtcli.process import get_soup, preprocess, process, get_max_number # Get
from dtcli.test import test # All
from dtcli.color import color # The
from dtcli.cmdline import cmd_parser, banner # Functions


def main() -> None:
    """
        Main Function
    """
    args = cmd_parser() # Get the arguments

    if args.website in ['dtc', 'qdb']: # Only those websites are concerned by these options
        if args.lines < -1 or args.lines == 0: # Test if lines option is done properly
            print("Lines must be above or equal 1")
            sexit(1)
        if args.over < -1: # Test if over option is done properly
            print('"over" must be over (hehe) or equal 1')
            sexit(1)
        if args.under < -1 or args.under == 0: # Test if under option is done properly
            print('"under" must be over (wat?) or equal 1')
            sexit(1)
    url = {'dtc': "https://danstonchat.com/{}.html", 'nsf': "https://nuitsansfolie.com/nsf/{}",
           'qdb': "http://www.bash.org/?{}"}[args.website] # URL matrices
    website = {'dtc': 'DTC', 'nsf': 'NSF', 'qdb': 'QDB'}[args.website] # Name to print
    maxi = get_max_number(args.website) # Get max number of allowed posts
    if args.verbose: print(color.CYAN + f'Max allowed number for {website} : {maxi}' + color.END)

    if args.number >= 1: # If a number is specified, just take it
        number = args.number # Simpler to access
        tmp_url = url.format(args.number) # Complete URL (using the matrice and the number provided)
        soup = get_soup(tmp_url, args.ignore, args.verbose) # Get the parsed HTML
        if soup == '': # If soup is empty, print a message
            print("""The number asked returns an error (Empty soup).\n
                    Please report this (number+message) to the issue page :\n
                    https://github.com/Luc-Saccoccio/dtcli/issues""")
            sexit(1)
        lines, title, _ = preprocess(soup, args.number, args.website)
        content = process(lines, number, args.website)
    elif args.website in ['dtc', 'qdb']: # Else, consider the other passed options
        conditions = {'force': (args.force_title and args.website == 'dtc'), 'lines': (args.lines != -1),
                      'over': (args.over != -1), 'under': (args.under != -1)}
        answers = {'force': None, 'lines': None, 'over': None, 'under': None}
        if args.verbose:
            print("Required conditions: ", conditions)
            print(f'Ignoring: {args.ignore}')
        while conditions != answers:
            answers = {'force' : False, 'lines' : False, 'over' : False, 'under': False}
            number = randint(0, maxi)
            tmp_url = url.format(number)
            if args.verbose:
                print(color.YELLOW + f'testing {website} n°{number}, url {tmp_url}' + color.END)
            soup = get_soup(tmp_url, args.ignore, args.verbose)
            if soup != '':
                lines, title, title_exist = preprocess(soup, number, args.website)
                if lines != ['']:
                    content = process(lines, number, args.website)
                    conditions_gen = ((condition, variable) for condition, variable in zip(conditions, [title_exist, args.lines, args.over, args.under]) if conditions[condition])
                    for condition, variable in conditions_gen:
                        if args.verbose: print(color.PURPLE + f'- testing {condition}' + color.END)
                        answers[condition] = test(condition, lines, variable)
                else:
                    answers = {}
    else: # The case of NSF
        soup = None
        while not soup:
            number = randint(0, maxi)
            tmp_url = url.format(number)
            if args.verbose:
                print(color.YELLOW + f'testing {website} n°{number}, url {tmp_url}'+ color.END)
            soup = get_soup(tmp_url, args.ignore, args.verbose)
        lines, title, _ = preprocess(soup, args.number, args.website)
        content = process(lines, number, args.website)

    if not args.hide_banner:
        banner(title, {'dtc': 'DTC', 'nsf': 'NSF', 'qdb': 'QDB'}[args.website], number, tmp_url, args.hide_title)
    print(content)
