import bs4
from util.plugin import command

cached = []


def get_new():
    soup = bs4.BeautifulSoup('http://www.fmylife.com/random', 'lxml')
    for e in soup.find_all('div', {'class': 'post article'}):
        fml_id = int(e['id'])
        text = ''.join(e.find('p').find_all(text=True))
        cached.append((fml_id, text))


@command(name='fml', aliases='fmylife', help='Get a random quote from fmylife.com')
def fml_command(chat, message, args, sender):
    fml_id, text = cached.pop()
    chat.SendMessage("#%s: %s" % (fml_id, text))
    if len(cached) < 3:
        get_new()