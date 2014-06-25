import random
import string


def get_args_string(args):
    argstring = ""
    argiterator = iter(args)
    next(argiterator)
    for arg in argiterator:
        argstring += "{0} ".format(arg)
    return argstring


def get_args(args):
    argiterator = iter(args)
    next(argiterator)
    return list(argiterator)


def get_arg(num, args):
    argiterator = iter(get_args(args))
    while num > 0:
        next(argiterator)
        num -= 1
    return list(argiterator)


def get_random_string(length):
    ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(length))
