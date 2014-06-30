import config

user_permissions = {}  # Skype instance
operators = []  # Skype Handles


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
    if is_operator(user):
        return True
    perms = get_permissions(user)
    if permission in perms:
        return True
    else:
        return False


def add_permission(user, permission, load=False):
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
    if not load:
        conf = config.config()
        users = conf.get('users', {})
        if user not in users:
            users.update({user: {'permissions': []}})
        permissions = users[user]['permissions']
        permissions.append(permission)
        conf.update({'users': users})
        config.save(conf)


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
    conf = config.config()
    users = conf.get('users', {})
    if user not in users:
        return
    permissions = users[user]['permissions']
    permissions.remove(permission)
    users[user]['permissions'] = permissions
    config.save(conf)


def load_permissions():
    print "Loading permissions..."
    conf = config.config()
    users = conf.get('users', {})
    for user in users:
        permissions = users[user]['permissions']
        if not permissions:
            continue
        for permission in permissions:
            add_permission(user, permission, load=True)
    print "Loaded permissions for {} users.".format(len(users))
    print "Loading operators..."
    config_operators = conf.get('operators', [])
    for operator in config_operators:
        operators.append(operator)
    print "Loaded operator status for {} users.".format(len(config_operators))


def add_operator(new_op):
    conf = config.config()
    config_operators = conf.get('operators', [])
    if new_op in config_operators:
        return False
    config_operators.append(new_op)
    conf['operators'] = config_operators
    config.save(conf)
    return True


def remove_operator(remove_op):
    conf = config.config()
    config_operators = conf.get('operators', [])
    if remove_op not in config_operators:
        return False
    config_operators.remove(remove_op)
    conf['operators'] = config_operators
    config.save(conf)
    return True


def is_operator(user):
    return user in operators


def get_operators():
    return operators
