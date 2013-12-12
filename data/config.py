__author__ = 'dankerrigan'

import sys

from yaml import load, dump

try:
    from yaml import CLoader as Loader, CDumper as Dumper
except ImportError:
    from yaml import Loader, Dumper


def load_config(filename):
    data = None
    with open(filename, 'rb') as yaml_file:
        data = load(yaml_file, Loader=Loader)
    return data


if __name__ == '__main__':
    print load_config(sys.argv[1])