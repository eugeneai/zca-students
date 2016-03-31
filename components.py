from interfaces import *
from zope.interface import implementer
from zope.component import adapter, getGlobalSiteManager, getUtility, subscribers

from zope.configuration.xmlconfig import xmlconfig


@implementer(IStudent)
class Student(object):
    """Implements IStudent interface
    """

    def __init__(self, name=None, doc=None, group=None,
        stub=False):
        """Initializes a student data.
        name is a given name and familyname of the student.
        doc is the number of student's document.
        """
        if stub:
            pass
        else:
            self.name=name
            self.doc=doc
            self.group=None
            self.move(group)

    def move(self, group):
        """Transfer the student to new group.

        Arguments:
        - `group`: a Group reference
        """

        self.__rem_group()

        # self.group == None
        group.add_student(self)

    def belongs_to(self, group):
        """Cheks that the student belogs to a group.
        """

        return self.group==group

    def __rem_group(self):
        """
        """
        if not self.group is None:
            self.group.remove_student(self)
            self.group=None

    def send_down(self):
        """Sends down the student from its group and university.
        """

        self.__rem_group()

    def __eq__(self, other):
        if self.doc!=other.doc:
            return False
        if self.name!=other.name:
            return False
        #if self.group!=other.group:
        #    return False

        return True

    def __eq__(self, other):
        if self.name!=other.name or self.doc!=other.doc:
            return False
        return True

    def print(self):
        print ("Student {} doc: {}".format(self.name, self.doc))

@implementer(IGroup)
class Group(object):
    """Implements a group of students
    """

    def __init__(self, name=None, stub=False):
        """Initializes group data
        """
        if stub:
            pass
        else:
            self.name=name
        self.students=[]

    def add_student(self, student):
        """Adds a student to the group

        Arguments:
        - `student`: The student to be added.
        """
        if student.group==None:
            self.students.append(student)
            student.group=self
        else:
            raise ValueError("cannot add a student belonging to another group")

    def remove_student(self, student):
        """Remove a student from the group
        """
        if student.group==self:
            self.students.remove(student)
            student.group=None
        else:
            raise ValueError("student does not belong to the group")

    def size(self):
        """Returns size of the group
        """
        return len(self.students)

    def disperse(self):
        """Remove all the students from the group.
        """

        students=self.students[:]
        for s in students:
            self.remove_student(s)

    def __eq__(self, other):
        if self.name!=other.name:
            return False
        ss=set([(s.name,s.doc) for s in self.students])
        so=set([(s.name,s.doc) for s in other.students])
        if ss!=so:
            return False
        return True

    def print(self):
        print ("-"*20)
        print ("Group: {}".format(self.name))
        print ("its size: {}".format(len(self.students)))
        for s in self.students:
            s.print()


@implementer(IDictionaryStorage)
class DictionaryStorage(object):
    """Stores objects in a dictionary
    """

    def __init__(self, storage):
        """
        """
        self.storage=storage

    def store(self, obj):
        o=IDictionaryStorable(obj)
        return o.store_in(self)

    def get(self, obj_id, class_=None):
        return self.storage[obj_id]

    def get_id(self):
        return len(self.storage)

@implementer(IDictionaryStorable)
@adapter(IGroup)
class IGroupToIDictionaryStorableAdapter(object):
    """This adapter stores groups in a dictionary.
    """

    def __init__(self, group):
        assert IGroup.providedBy(group)
        self.group=group

    def store_in(self, storage):
        """Stores self into a dictionary storage

        Arguments:
        - `storage`: A dictionary storage, where the
        objects to be stored.
        """

        # Store all students
        students=self.group.students
        for s in students:
            s_id=storage.store(s)

        # Store group
        obj_id=storage.get_id()
        storage.storage[obj_id]=self.group
        self.group.dict_id=obj_id
        return obj_id

@implementer(IDictionaryStorable)
@adapter(IStudent)
class IStudentToIDictionaryStorableAdapter(object):
    """
    """

    def __init__(self, student):
        """
        """
        assert IStudent.providedBy(student)
        self.student=student

    def store_in(self, storage):
        obj_id=storage.get_id()
        storage.storage[obj_id]=self.student
        self.student.dict_id=obj_id
        return obj_id

class GroupStorerAndLoader(object):
    def __init__(self, group):
        self.group=group

    def store(self):
        storage=getUtility(IStorage, name="storage")
        return storage.store(self.group)

    def load(self, cls):
        storage=getUtility(IStorage, name="storage")
        return storage.get(self.group.key, Group)

@implementer(IKey)
class Key(object):
    def __init__(self, key):
        self.key=key

def load_object(key, cls, keycls=Key):
    k=keycls(key)
    return subscribers([k],IEventLoad)[0].load(cls)


GSM=getGlobalSiteManager()
GSM.registerAdapter(IGroupToIDictionaryStorableAdapter)
GSM.registerAdapter(IStudentToIDictionaryStorableAdapter)

# provides = обслуживать, оснащать (экземпляры)
# implements = реализует (классы)





def test_students(storage):
    assert IGroup.implementedBy(Group), "This class does not provide IGroup"
    assert IStudent.implementedBy(Student), "This class does not provide IGroup"

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

    assert s3.belongs_to(g1)
    s3.move(g2)
    assert s3.belongs_to(g2)

    assert g2.size()==2
    assert g1.size()==1

    assert s1.belongs_to(g1)
    s1.send_down()
    assert s1.group==None
    assert g1.size()==0

    id_g1=storage.store(g1)
    id_g2=storage.store(g2)
    assert id_g1!=None
    assert id_g2!=None

    _g1=storage.get(id_g1, Group)
    _g2=storage.get(id_g2, Group)
    assert _g1==g1
    assert _g2==g2

    g2.disperse()
    assert g2.size()==0

    g1.disperse()
    assert g1.size()==0


def test_storage():
    assert IStorage.implementedBy(DictionaryStorage)
    assert IDictionaryStorage.implementedBy(DictionaryStorage)
    storage=DictionaryStorage({})
    test_students(storage)

xmlconfig(open("config.zcml","r"))

if __name__=="__main__":
    test_storage()
    print("Ok")
    quit()
