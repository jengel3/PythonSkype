from os import path


def get_lines(file_name):
    file_path = path.join("data", file_name)
    if not path.isfile(file_path):
        return None
    lines = []
    for line in open(file_path, 'r'):
        lines.append(line)
    return lines