import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
from components import Group, Student, load_object
from interfaces import *
from zope.component import getMultiAdapter, queryMultiAdapter, getUtility, subscribers
from zope.interface import directlyProvides, implementer


builder = Gtk.Builder()
directlyProvides(builder, IGroupView)

builder.add_from_file("gui.glade")
button_ok=builder.get_object("button_ok")
group_dialog=builder.get_object("group_dialog")

class Ui(object):
    pass

class GroupDialogController(object):
    """
    """

    widget_names=("app_window", "group_list", "group_name")

    def __init__(self, model, builder):
        """
        """
        self.model=model
        self.builder=builder
        builder.connect_signals(self)
        self.ui=Ui()
        wn=self.__class__.widget_names
        for name in wn:
            setattr(self.ui, name, builder.get_object(name))
        self.ui._main=builder.get_object(wn[0])

        self.setup()
        self.ui._main.show_all()
        print (self.ui.app_window)

    def setup(self):
        self.ui.group_name.set_text(self.model.name)
        model=self.model
        gl=self.ui.group_list     # GTK "model"
        gl.clear()
        for i,s in enumerate(model.students):
            # gl.append([i+1, s.name, s.doc])
            gl.append([i+1, s.name, s.doc, True, False])

    def on_button_ok_pressed(self, button):
        self.model.name=self.ui.group_name.get_text().strip()
        key=subscribers([self.model], IEventStore)[0].store()
        print ("Key:", key)

    def on_app_window_delete_event(self, window, data):
        Gtk.main_quit()

    def on_cellrenderertext_name_edited(self, r, path, text):
        gl=self.ui.group_list[path][1]=text
        path=int(path)
        self.model.students[path].name=text

    def on_cellrenderertext_doc_edited(self, r, path, text):
        try:
            t=int(text)
        except ValueError:
            t=0
        gl=self.ui.group_list[path][2]=t
        path=int(path)
        self.model.students[path].doc=t

    def on_delete_clicked(self, button):
        print ("Try to delete")

    def on_add_clicked(self, button):
        s=Student(name="", doc=0, group=self.model)
        self.setup()

    def on_group_name_changed(self, editable):
        pass
        #print (editable)
        #self.model.name=text.strip()
        #self.ui.group_name.set_text(self.model.name)
        #self.model.print()

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

@implementer(IRemoteKey)
class RemoteKey(object):
    def __init__(self, key):
        self.key=key

def real():
    group=load_object(5, Group)
    edit(group)

def edit(group):
    controller=queryMultiAdapter((group, builder), IMVCListViewController)
    if controller==None:
        raise RuntimeError("not adapted")

def remote():
    group=load_object("http://127.0.0.1:8080/5",Group,RemoteKey)
    edit(group)

if __name__=="__main__":
    #tests()
    real()
    #remote()
    Gtk.main()
    print ("Ok")
    quit()
