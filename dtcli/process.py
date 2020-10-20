from sys import exit as sexit
from bs4 import BeautifulSoup
import requests
from dtcli.color import color


def get_soup(url, ignore, verbose):
    """
        Return parsed HTMl
    """
    result = requests.get(url)
    if result.status_code != 200:
        print(color.BOLD + color.YELLOW + "Retrieiving failed : url %s" % url + color.UNDERLINE
              + url + color.END)
        if verbose:
            print("Error %s, reason : %s" % (result.status_code, result.reason))
        if not ignore:
            sexit(1)
        else:
            return ''
    return BeautifulSoup(result.content, 'html.parser')

def preprocess(soup, number, website):
    """
        Preprocess parsed HTML
        Return lines or complete text
        Title if DTC
    """
    if website == 'dtc':
        base = soup.find('meta', attrs={'name': 'description'})
        title = str(soup.find('title'))
        if title[0:9] != '<title> #':
            title = title.split(' #%d' % number)[0]
            title = title[7:]
        else:
            title = None
        title_exist = (title is not None)
        message = base['content']
    elif website == 'nsf':
        base = soup.find('meta', attrs={'property': 'og:description'})
        title, title_exist = None, False
        message = base['content']
    else:
        base = soup.find('p', attrs={'class': 'qt'})
        title, title_exist = None, False
        message = base.text

    lines = message.split("\n")
    return lines, title, title_exist

def process(lines, number, website): # Process the lines : format them, highlight and stuff
    """
        Process the lines :
        Highlight and stuff
    """
    text = ""
    if website == 'nsf':
        return '\n'.join(lines)
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
        print("Error while processing {} n°{}, url {}".format(website, number, {'dtc': "https://danstonchat.com/{}.html", 'bash': "bash.org/?{}"}[website].format(number)))
        sexit(1)
    return text[:-1]
