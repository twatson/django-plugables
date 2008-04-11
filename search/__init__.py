
from base import *

registry = {}

class AlreadyRegistered(Exception):
    """
    An attempt was made to register a model more than once.
    """
    pass

class ModelSearchOptions(object):
    def __init__(self, model, fields, manager=None):
        self.model = model
        self.fields = fields
        self.manager = manager or model._default_manager

def register(model, *args, **kwargs):
    opts = model._meta
    if str(opts) in registry:
        raise AlreadyRegistered("The model %s has already been registered." % model.__name__)
    registry[str(opts)] = ModelSearchOptions(model, *args, **kwargs)
