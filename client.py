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
    def __init__(self, sobj):
        """sobj is a server proxy object"""
        self.sobj=sobj

    def set_name(self, name):
        return self.sobj.set_name(name)

    def get_name(self):
        return self.sobj.get_name()

@implementer(IGroup)
class GroupProxy(object):
    pass
