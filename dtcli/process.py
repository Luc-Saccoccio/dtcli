"""
    File containing all the
    functions processing
    the informations retrieved
"""

from sys import exit as sexit
from bs4 import BeautifulSoup
from textwrap3 import wrap
import requests
from re import findall
from dtcli.color import color

def get_max_number(website: str) -> int:
    """
        Getting the max number of dtc/qdb/nsf
    """
    if website == 'dtc':
        latest = requests.get('https://danstonchat.com/latest.html')
        soup = BeautifulSoup(latest.content, 'html.parser')
        items = soup.find('div', {'class': 'items'})
        result = items.findChildren()
        nums = findall(r'\d+', str(result[1]))
        return int(nums[1])
    elif website == 'qdb':
        latest = requests.get('http://bash.org/?latest')
        soup = BeautifulSoup(latest.content, 'html.parser')
        result = soup.find('p', {'class': 'quote'})
        nums = findall(r'\d+', str(result))
        return int(nums[0])
    elif website == 'nsf':
        latest = requests.get('https://nuitsansfolie.com/slider')
        soup = BeautifulSoup(latest.content, 'html.parser')
        result = soup.find('h1', {'class': 'anecdote-title'})
        nums = findall(r'\d+', str(result))
        return int(nums[1])

def get_soup(url: str, ignore: bool, verbose: bool) -> BeautifulSoup:
    """
        Return parsed HTMl
    """
    while True:
        try:
            result = requests.get(url)
            break
        except requests.ConnectionError as error:
            if verbose:
                print(f'Error while handling NSF : {error}')
    if result.status_code != 200:
        print(color.BOLD + color.YELLOW + "Retrieiving failed : url %s" % url
              + color.UNDERLINE + color.END)
        if verbose:
            print("Error %s, reason : %s" % (result.status_code, result.reason))
        if not ignore:
            sexit(1)
        else:
            return ''
    return BeautifulSoup(result.content, 'html.parser')

def preprocess(soup: BeautifulSoup, number: int, website: str) -> tuple:
    """
        Preprocess parsed HTML
        Return lines or complete text
        Title if DTC
    """
    title, title_exist = None, False
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
        message = base['content']
    else:
        base = soup.find('p', attrs={'class': 'qt'})
        message = base.text if base else ''

    lines = message.split("\n")
    return lines, title, title_exist

def process(lines: list, number: int, website: str) -> str: # Process the lines : format them, highlight and stuff
    """
        Process the lines :
        Highlight and stuff
    """
    text = ""
    if website == 'nsf':
        text = wrap(''.join(lines), 54)
        return '\n'.join((line.center(54, " ") for line in text))
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
        print(f'Error while processing {website} n°{number}, url {{}}'.format(
            {'dtc': "https://danstonchat.com/{}.html", 'qdb': "bash.org/?{}"}[website].format(
                number)))
        sexit(1)
    return text[:-1]
