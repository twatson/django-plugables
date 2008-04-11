from django.db import models


class LiveEntryManager(models.Manager):
    """
    Custom manager that only returns entries marked ``Live``.
    """
    
    def get_query_set(self):
        return super(LiveEntryManager, self).get_query_set().filter(status__exact=self.model.LIVE_STATUS)
    

