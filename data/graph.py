__author__ = 'dankerrigan'

import os
import sys

for directory in ['/etc/graphite-web', '/etc/graphite']:
    if os.path.isdir(directory):
        graphite_path = directory
        break

sys.path.append(directory)
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "local_settings")

from graphite.account.models import MyGraph

if __name__ == '__main__':
    for obj in MyGraph.objects:
        print obj