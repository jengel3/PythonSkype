import bs4
from util.plugin import command
import util.http as http


cached = []


def get_new():
    soup = bs4.BeautifulSoup(http.get_url_data('http://www.fmylife.com/random'))
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


get_new()