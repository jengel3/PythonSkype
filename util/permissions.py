import config

user_permissions = {}  # Skype instance
operators = []  # Skype Handles


def get_permissions(user):
    if not user in user_permissions:
        return []
    return user_permissions[user]


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
    perms.append(permission)
    user_permissions.update({user: perms})
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
    if permission not in perms:
        return
    perms.remove(permission)
    user_permissions.update({user: perms})
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
