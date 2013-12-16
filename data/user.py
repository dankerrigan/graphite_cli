__author__ = 'dankerrigan'

import os
import sys

for directory in ['/etc/graphite-web', '/etc/graphite']:
    if os.path.isdir(directory):
        graphite_path = directory
        break

sys.path.append(directory)
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "local_settings")


from graphite.account.models import MyGraph, Profile
from django.contrib.auth.models import User

def list_users():
    return User.objects.all()

def get_user(username):
    user = User.objects.get(username=username)
    if user:
        return user
    else:
        return None

def profile_for_user(username):
    user = get_user(username)
    if user:
        profile = Profile.objects.get(user=user)
        return profile
    else:
        return None

if __name__ == '__main__':
    if sys.argv[1] == 'list':
        for user in list_users():
	        print user
    elif sys.argv[1] == 'get':
        print get_user(sys.argv[2])
    elif sys.argv[1] == 'profile':
        print profile_for_user(sys.argv[2])


