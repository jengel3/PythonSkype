import urllib
import json
import HTMLParser


GOOGLE = "http://ajax.googleapis.com/ajax/services/search/{}?v=1.0&q={}"


def get_results(query, query_type):
    parser = HTMLParser.HTMLParser()
    query = urllib.quote(query)
    parsed_url = GOOGLE.format(query_type, query)
    data = json.loads(urllib.urlopen(parsed_url).read())
    results = data['responseData']['results']
    links = {}
    for result in results:
        link = parser.unescape(result['url'])
        title = parser.unescape(result['titleNoFormatting'])
        print link, title
        links.update({link: title})
    try:
        count = data['responseData']['cursor']['resultCount']
    except KeyError:
        count = 0
    return links, count
