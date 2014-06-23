import praw

from util.plugin import event
from util.plugin import command


def get_reddit():
    return praw.Reddit("SkypeBot Reddit Scraper by Jake0oo0")


@event(name="reddit-post", regex="(www\.reddit\.com/r/[A-Za-z0-9-_]+/[A-Za-z0-9-/_]+|redd\.it/[A-Za-z0-9-]+)")
def post(chat, message, args, sender, found):
    r = get_reddit()
    if found.endswith('/'):
        found = found[:-1]
    try:
        submission = r.get_submission(url='http://' + found)
        chat.SendMessage('{} - by /u/{} - {}'.format(submission.title, submission.author, submission.short_link))
    except praw.requests.exceptions.HTTPError:
        pass


@command(name="reddit", help="Display information about a Reddit user.")
def reddit_user(chat, message, args, sender):
    if len(args) != 1:
        chat.SendMessage("Provide a redditor to gather information from.")
        return
    username = args[0]
    r = get_reddit()
    try:
        redditor = r.get_redditor(username)
    except praw.requests.exceptions.HTTPError:
        chat.SendMessage("User not found.")
        return
    if not redditor:
        chat.SendMessage("User not found.")
        return
    comment_karma = redditor.comment_karma
    link_karma = redditor.link_karma
    user_name = redditor.name
    page_link = redditor._url
    msg = '{} - Comment Karma: {} - Link Karma: {} - {}'.format(user_name, comment_karma, link_karma, page_link)
    chat.SendMessage(msg)
