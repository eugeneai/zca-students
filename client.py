import xmlrpc.client
from zope.interface import implementer
from interfaces import *

class RemoteObjectAccess(object):
    def __init__(self, obj):
        self.obj=obj
    def store(self):
        pass
    def load(self,cls):
        pass

@implementer(IStudent)
class StudentProxy(object):
    pass

@implementer(IGroup)
class GroupProxy(object):
    pass
