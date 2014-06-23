def get(value):
    config = {}
    execfile('config.conf', config)
    return config[value]