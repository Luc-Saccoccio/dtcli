from sys import exit as sexit
import locale
import emoji

def test(ttype, lines, lines_number, over, under):
    """
        Test each conditions the user
        asked for
    """
    if ttype == 'lines':
        result = len(lines) == lines_number
    elif ttype == 'over':
        result = len(lines) >= over
    elif ttype == 'under':
        result = len(lines) <= under
    else:
        print("Error while parsing arguments")
        sexit(1)
    return result

def test_emojis(title):
    """
        Test for emojis in the title
        of the DTC. If there is, add
        one to the length : An emoji
        count as one character but is
        displayed as two
    """
    title_length = len(title)
    emojis = [c for c in title if (c in emoji.UNICODE_EMOJI) or (c in ['︵', '）'])]
    return title_length + len(emojis)

def test_lang():
    """
        Test for website to use according
        to the system default language
    """
    lang = locale.getdefaultlocale()[0][0:2]
    if lang == 'fr':
        return 'dtc'
    return 'bashorg'
