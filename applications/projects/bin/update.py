#!/usr/bin/env python

# Setup the paths.
import sys, os
sys.path.append('/home/plugables/applications')
sys.path.append('/home/plugables/applications/core')
sys.path.append('/home/plugables/applications/projects')

# Setup the enviornment.
from django.core.management import setup_environ
import settings

setup_environ(settings)

# Now start the script.
from projects.providers.svn import RepositorySyncr

rs = RepositorySyncr()
rs.syncRepositories()
