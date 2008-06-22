#!/usr/bin/env python

# Setup the paths.
import sys, os
sys.path.append('/var/www/djangoplugables/applications')
sys.path.append('/var/www/djangoplugables/applications/core')
sys.path.append('/var/www/djangoplugables/applications/projects')

# Setup the enviornment.
from django.core.management import setup_environ
import settings

setup_environ(settings)

# Now start the script.
from applications.projects.providers.svn import RepositorySyncr

rs = RepositorySyncr()
rs.syncRepositories()
