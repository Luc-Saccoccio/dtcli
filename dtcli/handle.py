from sys import exit as sexit
from dtcli.color import color


def handle_nsf():
    """
        Format nsf
    """
    pass


def handle_dtc(lines, website, number):
    """
        Format dtc and bash.org
    """
    try:
        for l in lines:
            if l == '':
                continue
            if l[0] == '*':
                text += color.ITALIC + l + color.END + "\n"
                continue
            if ('<' in l and '>' in l) and l[0] == '<':
                if (':' in l and l.find(':') > l.find('<')) or ':' not in l:
                    l = l.split(">", 1)
                    l[0] = color.BOLD + l[0] + ">" + color.END
                    text += ''.join(l) + "\n"
                elif ':' not in l:
                    text += l + "\n"
            elif ('[' in l and ']' in l) and l[0] == '[':
                l = l.split("]", 1)
                if ':' in l[0]:
                    l[0] = color.BOLD + color.GREEN + l[0] + "]" + color.END
                else:
                    l[0] = color.BOLD + l[0] + "]" + color.END
                if ":" in l[1]:
                    t = l[1].split(":", 1)
                    l[1] = color.BOLD + t[0] + ":" + color.END + t[1]
                elif '<' in l[1] and '>' in l[1]:
                    t = l[1].split(">", 1)
                    l[1] = color.BOLD + t[0] + '>' + color.END + t[1]
                text += ''.join(l) + "\n"
            elif ('(' in l and ')' in l) and l[0] == '(':
                l = l.split(')', 1)
                l[0] = color.BOLD + l[0] + ')' + color.END
                text += ''.join(l) + "\n"
            elif ':' in l:
                l = l.split(":", 1)
                l[0] = color.BOLD + l[0] + ":" + color.END
                text += ''.join(l) + "\n"
            else:
                text += ''.join(l) + "\n"
    except IndexError:
            print("Error while processing %s n°%d, url https://danstonchat.com/%d.html" %
                  (website, number, number))
            sexit(1)

