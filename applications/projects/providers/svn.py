import time
import logging
import datetime

try:
    import pysvn
except ImportError:
    pysvn = None

from django.db import transaction
from django.utils.encoding import smart_unicode

from applications.core.models import Item
from applications.projects.models import Repository, Changeset


class RepositorySyncr:
    """
    SVNUpdater syncs a set of subversion repositories. It will go through each
    repository listed and create a ``Changeset`` object for each of the
    repository's commits.
    
    This app requires pysvn which is available at:
    http://pysvn.tigris.org/
    """
    
    log = logging.getLogger("projects.providers.svn")
    
    def _update_repository(self, repository):
        source_identifier = '%s:%s' % (__name__, repository.url)
        last_update_date = Item.objects.get_last_update_of_model(Changeset, source=source_identifier)
        self.log.info('Updating changes from %s since %s', repository.url, last_update_date)
        rev = pysvn.Revision(pysvn.opt_revision_kind.date, time.mktime(last_update_date.timetuple()))
        c = pysvn.Client()
        for revision in reversed(c.log(repository.url, revision_end=rev)):
            self._handle_revision(repository, revision)
    
    @transaction.commit_on_success
    def _handle_revision(self, repository, r):
        self.log.debug("Handling [%s] from %s" % (r.revision.number, repository.url))
        ci, created = Changeset.objects.get_or_create(
            revision = r.revision.number,
            repository = repository,
            committed = datetime.datetime.fromtimestamp(r.date),
            defaults = {"message": smart_unicode(r.message)}
        )
        return Item.objects.create_or_update(
            instance = ci, 
            timestamp = datetime.datetime.fromtimestamp(r.date),
            source = "%s:%s" % (__name__, repository.url),
        )
    
    def syncRepositories(self):
        """
        Loops through all given repositories in ``Repository`` and updates
        any ``Changeset`` objects missing since the previous update.
        """
        
        repositories = Repository.objects.filter(type='svn')
        
        for repository in repositories:
            self._update_repository(repository)
    

