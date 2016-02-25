from zope.interface import Interface, Attribute

class IStudent(Interface):
    """This interface defines schema for student
    component.
    """

    name=Attribute("Name of the student")
    doc=Attribute("Number of document")
    group=Attribute("A group of the student")

    def move(group):
        """Add the student to a group."""

    def send_down():
        """Send down the student from the university."""

    def belongs_to(group):
        """Checks wether the student belongs to a group"""

class IGroup(Interface):
    """Defines shcema and methods for student group
    """

    name=Attribute("Name of the group")
    students=Attribute("List of the students belonging to the group")

    def add_student(student):
        """Adds a student to the group"""

    def remove_student(student):
        """Removes a student from the group"""

    def disperse():
        """Remove all the student from the group"""

class IStorage(Interface):
    """Defines interface for components that
    store objects in a pistent media.
    """

    def store(obj):
        """Store an obj[ect] into self"""

    def get(obj_id):
        """Retrieve an object from self.
        The object identified by obj_id.
        """

class IDictionaryStorage(IStorage):
    """Defines storage implemented with a python dictionary.
    """

    def get_id():
        """Allocates an id for a storable object."""

class IDictionaryStorable(Interface):
    """
    """

    def store_in(storage):
        """Stores itself into a storage
        """

class ISQLiteStorage(Interface):
    """Denote SQLite storage
    """

class ISQLiteStorable(Interface):
    """
    """
