import argparse
from dtcli import __version__
from dtcli.test import test_lang, test_emojis
from dtcli.color import color


def banner(title, website, number, url, hide_title):
    """
        Print banner and joke
    """
    infos = (color.BOLD + color.RED + "%s n°" % website
             + color.DARKCYAN + str(number) + color.RED + ", URL : " + color.END
             + color.UNDERLINE + url + color.END)
    infos_length = len("%s n°" % website + str(number) + ", URL : " + url)
    if hide_title or title is None:
        banner_length = infos_length
        print("┌" + (banner_length + 2)*"─" + "┐")
        print("│ " + infos + " │")
        print("└" + (banner_length + 2)*"─" + "┘")
    else:
        title_length = test_emojis(title)
        banner_length = title_length if title_length >= infos_length else infos_length
        print("┌" + (banner_length + 2)*"─" + "┐")
        print("│ " + infos + (banner_length - infos_length)*" " + " │")
        print("├" + (banner_length + 2)*"─" + "┤")
        print("│ " + title + (banner_length - title_length)*" " + " │")
        print("└" + (banner_length + 2)*"─" + "┘")


def cmd_parser():
    """
        Argument Parser
    """
    # Argument parser creation
    ap = argparse.ArgumentParser(usage='%(prog)s [options]',
                                 description='A DTC querying tool',
                                 epilog='Please refer to dtcli(1) for more informations')

    # Group to avoid having force-title and hide-title at the same time
    gr = ap.add_mutually_exclusive_group()

    # Basic utilities
    ap.add_argument('--verbose', '-v', dest='verbose', action='store_true',
                    default=False, help="Increase output verbosity")
    ap.add_argument("--ignore", "-i", dest='ignore', action='store_true',
                    default=False, help="Don't stop on retreiving errors")
    ap.add_argument('--version', action='version', version='%(prog)s ' + __version__)

    ap.add_argument("--number", "-n", type=int, dest='number', action='store',
                    default=-1, metavar="INT", help="Specify a number")
    ap.add_argument("--hide-banner", "-b", dest='hide_banner', action='store_true',
                    default=False, help="Hide the informations")

    # Title Control
    gr.add_argument("--hide-title", "-t", dest='hide_title', action='store_true',
                    default=False, help="Hide the title of the joke")
    gr.add_argument("--force-title", "-f", dest='force_title', action='store_true',
                    default=False, help="Force the search for the joke with title")

    # Conditions
    ap.add_argument("--lines", "-l", type=int, dest='lines', action='store',
                    default=-1, metavar="INT", help="Search for a specific number of lines")
    ap.add_argument("--over", "-o", type=int, dest='over', action='store',
                    default=-1, metavar="INT", help="Search for a number of lines above specified")
    ap.add_argument("--under", "-u", type=int, dest='under', action='store',
                    default=-1, metavar="INT", help="Search for a number of lines below specified")

    ap.add_argument("--website", '-w', type=str, dest='website', action='store',
                    default=test_lang(), metavar='NAME', help="Get the joke from that website",
                    choices=['dtc', 'nsf', 'bash'])

    args = ap.parse_args()
    return args
