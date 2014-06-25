from util.plugin import command
from git import Repo


@command(name='update', permission='command.update')
def update_command(chat, message, args, sender):
    repo = Repo()
    git = repo.git
    try:
        pull = git.pull()
    except Exception as e:
        chat.SendMessage(e)
        return
    chat.SendMessage(pull)