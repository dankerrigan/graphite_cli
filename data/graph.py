__author__ = 'dankerrigan'

import os
import sys
from urlparse import urlparse, parse_qs

from user import profile_for_user

for directory in ['/etc/graphite-web', '/etc/graphite']:
    if os.path.isdir(directory):
        graphite_path = directory
        break

sys.path.append(directory)
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "local_settings")

from graphite.account.models import MyGraph

def list_user_graphs(username, name=None):
    profile = profile_for_user(username)
    if profile:
        if not name:
            return MyGraph.objects.filter(profile=profile)
        else:
            return MyGraph.objects.filter(profile=profile, name=name)
    else:
        print 'Could not find profile for user {0}'.format(username)
        return []

def extract_target_from_url(url):
    query = parse_qs(urlparse(url).query)
    target = '|'.join(query['target'])
    return target

def target_exists(username, url):
    targets = set()
    for graph in list_user_graphs(username):
        target = extract_target_from_url(graph.url)
        targets.add(target)

    new_target = extract_target_from_url(url)

    return new_target in targets

def named_graph_exists(username, name):
    return len(list_user_graphs(username, name)) > 0

def save_graph(username, name, url):
    if named_graph_exists(username, name):
        print 'Graph for {0} with name {1} already exists'.format(username, name)
        return False
    if target_exists(username, url):
        print 'Graph for {0} with target {1} already exists'.format(username, extract_target_from_url(url))
        return False

    profile = profile_for_user(username)
    if profile:
        graph = MyGraph(profile=profile, name=name, url=url)

        graph.save()
        return True
    else:
        print 'Could not find profile for user {0}'.format(username)
        return False

if __name__ == '__main__':
    if sys.argv[1] == 'list':
        username = sys.argv[2]

        for graph in list_user_graphs(username):
            target = extract_target_from_url(graph.url)

            print graph.name, graph.url

    elif sys.argv[1] == 'check':
        username = sys.argv[2]
        url = sys.argv[3]

        exists = target_exists(username, url)

        if exists:
            print 'Target Exists'
        else:
            print 'Target does not exist'

    elif sys.argv[1] == 'save':
        username = sys.argv[2]
        name = sys.argv[3]
        url = sys.argv[4]

        success = save_graph(username, name, url)

        if success:
            print 'Saved graph successfully'
        else:
            print 'Unable to save graph'