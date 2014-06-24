import config

user_permissions = {}  # Skype instance


def get_permissions(user):
    listed = []
    if not user in user_permissions:
        return listed
    perms = user_permissions[user]
    perm_string = perms.split(", ")
    for perm in perm_string:
        listed.append(perm)
    return listed


def has_permission(user, permission):
    perms = get_permissions(user)
    if permission in perms:
        return True
    else:
        return False


def add_permission(user, permission):
    perms = get_permissions(user)
    new_perms = []
    if len(perms) != 0:
        for perm in perms:
            new_perms.append(perm)
    new_perms.append(permission)
    perm_string = ''
    for perm in new_perms:
        perm_string += "%s, " % perm
    if len(perm_string) > 2:
        perm_string = perm_string[:-2]
    user_permissions.update({user: perm_string})


def remove_permission(user, permission):
    perms = get_permissions(user)
    new_perms = []
    if len(perms) != 0:
        for perm in perms:
            new_perms.append(perm)
    new_perms.remove(permission)
    perm_string = ''
    for perm in new_perms:
        perm_string += "%s, " % perm
    if len(perm_string) > 2:
        perm_string = perm_string[:-2]
    user_permissions.update({user: perm_string})


def load_permissions():
    print "Loading permissions.."
    conf = config.config()
    users = conf.get('users', [])
    for user in users:
        permissions = users[user]['permissions']
        if not permissions:
            continue
        for permission in permissions:
            add_permission(user, permission)
    print "Loaded permissions for {} users.".format(len(users))
