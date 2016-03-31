import rpyc
from interfaces import *
from zope.interface import implementer
from zope.component import adapter, getGlobalSiteManager, getUtility, subscribers

from zope.configuration.xmlconfig import xmlconfig

conn=rpyc.classic.connect("localhost")
rem_components=conn.modules.components
rem_components.default_config()

class GroupStorerAndLoader(object):
    def __init__(self, group):
        comps=getUtility(IModule, "components")
        self.sl=comps.GroupStorerAndLoader(group)

    def store(self):
        return self.sl.store()

    def load(self, cls):
        return self.sl.load(cls)

def register_components():
    xmlconfig(open("remote.zcml"))
