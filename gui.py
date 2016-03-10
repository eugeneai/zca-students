import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
from components import Group, Student
from interfaces import *
from zope.component import getMultiAdapter, queryMultiAdapter
from zope.interface import directlyProvides








builder = Gtk.Builder()
directlyProvides(builder, IGroupView)

builder.add_from_file("gui.glade")
button_ok=builder.get_object("button_ok")
group_dialog=builder.get_object("group_dialog")


class GroupDialogController(object):
    """
    """

    widget_names=("group_list")

    def __init__(self, model, builder):
        """
        """
        self.model=model
        self.builder=builder
        builder.connect_signals(self)
        self.setup()
        view.show_all()


    def setup(self):
        pass

    def on_button_ok_activate(self, button):
        print ("Ok pressed")

    def on_dialog_close(self, dialog):
        Gtk.main_quit()



def tests():
    g1=Group("System Engineers")
    assert IGroup.providedBy(g1)
    g2=Group("Knowledge Engineer")
    assert IGroup.providedBy(g2)
    s1=Student("John Doe", 123456, g1)
    assert IStudent.providedBy(s1)
    s2=Student("Cameron Diaz", 123457, g2)
    assert IStudent.providedBy(s2)
    s3=Student("Jim Kerry", 123458, g1)
    assert IStudent.providedBy(s3)

    assert IGroupView.providedBy(builder)

    model=g1
    controller=queryMultiAdapter((model, builder), IMVCListViewController)
    if controller==None:
        raise RuntimeError("not adapted")

if __name__=="__main__":
    tests()
    Gtk.main()
    print ("Ok")
    quit()
