from urllib import urlopen


def get_url_data(url):
    return urlopen(url).read()